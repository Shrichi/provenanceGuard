import os
import uuid
import sqlite3
from datetime import datetime, timezone

from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from dotenv import load_dotenv

from signals.llm_signal import get_llm_score
from signals.stylometric import get_structural_score

load_dotenv()

app = Flask(__name__)

# ── Rate limiting ──────────────────────────────────────────────────────────────
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=[],
    storage_uri="memory://",
)

# ── Database setup ─────────────────────────────────────────────────────────────
DB_PATH = "provenance.db"


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS submissions (
                content_id       TEXT PRIMARY KEY,
                creator_id       TEXT NOT NULL,
                submitted_text   TEXT NOT NULL,
                timestamp        TEXT NOT NULL,
                llm_score        REAL,
                structural_score REAL,
                confidence       REAL,
                attribution      TEXT,
                label            TEXT,
                status           TEXT DEFAULT 'classified',
                appeal_reasoning TEXT,
                appeal_timestamp TEXT
            )
        """)
        conn.commit()


# ── Confidence scoring ─────────────────────────────────────────────────────────
def compute_confidence(llm_score: float, structural_score: float) -> float:
    return round((llm_score + structural_score) / 2, 4)


# ── Label generation ───────────────────────────────────────────────────────────
def get_label(confidence: float) -> tuple[str, str]:
    if confidence >= 0.70:
        return "likely_ai", "This content is likely AI-generated"
    elif confidence >= 0.40:
        return "uncertain", "We're not confident enough to label this content as AI or human-created"
    else:
        return "likely_human", "This content is likely human-created"


# ── Audit log helpers ──────────────────────────────────────────────────────────
def log_submission(content_id, creator_id, text, llm_score, structural_score,
                   confidence, attribution, label):
    with get_db() as conn:
        conn.execute("""
            INSERT INTO submissions
                (content_id, creator_id, submitted_text, timestamp,
                 llm_score, structural_score, confidence,
                 attribution, label, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'classified')
        """, (
            content_id,
            creator_id,
            text,
            datetime.now(timezone.utc).isoformat(),
            llm_score,
            structural_score,
            confidence,
            attribution,
            label,
        ))
        conn.commit()


def get_log_entries(limit: int = 50):
    with get_db() as conn:
        rows = conn.execute("""
            SELECT content_id, creator_id, timestamp, llm_score,
                   structural_score, confidence, attribution, label,
                   status, appeal_reasoning, appeal_timestamp
            FROM submissions
            ORDER BY timestamp DESC
            LIMIT ?
        """, (limit,)).fetchall()
    return [dict(row) for row in rows]


# ── Routes ─────────────────────────────────────────────────────────────────────
@app.route("/submit", methods=["POST"])
@limiter.limit("10 per minute;100 per day")
def submit():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400

    text = data.get("text", "").strip()
    creator_id = data.get("creator_id", "").strip()

    if not text:
        return jsonify({"error": "Missing required field: text"}), 400
    if not creator_id:
        return jsonify({"error": "Missing required field: creator_id"}), 400

    content_id = str(uuid.uuid4())

    llm_score = get_llm_score(text)
    structural_score = get_structural_score(text)

    confidence = compute_confidence(llm_score, structural_score)
    attribution, label = get_label(confidence)

    log_submission(
        content_id=content_id,
        creator_id=creator_id,
        text=text,
        llm_score=llm_score,
        structural_score=structural_score,
        confidence=confidence,
        attribution=attribution,
        label=label,
    )

    return jsonify({
        "content_id": content_id,
        "attribution": attribution,
        "confidence": confidence,
        "label": label,
        "llm_score": llm_score,
        "structural_score": structural_score,
    }), 200


@app.route("/log", methods=["GET"])
def log():
    entries = get_log_entries()
    return jsonify({"entries": entries}), 200


# ── Startup ────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    init_db()
    app.run(debug=True, port=5001)
