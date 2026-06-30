"""
Accuracy test: 50 labeled samples (25 AI, 25 human) across short/medium/long sizes.
Calls signal functions directly to bypass the rate limiter.
"""

from signals.llm_signal import get_llm_score
from signals.stylometric import get_structural_score

def compute_confidence(llm, structural):
    if structural is None:
        return round(llm, 4)
    return round(0.7 * llm + 0.3 * structural, 4)

def get_label(confidence):
    if confidence >= 0.70:
        return "likely_ai"
    elif confidence >= 0.40:
        return "uncertain"
    return "likely_human"

# ── Test cases ─────────────────────────────────────────────────────────────────
# Each entry: (true_label, size, text)
SAMPLES = [

    # ── AI SHORT (1–3 sentences) ───────────────────────────────────────────────
    ("ai", "short",
     "Artificial intelligence represents a transformative paradigm shift in modern society, "
     "offering unprecedented opportunities for innovation across diverse sectors."),

    ("ai", "short",
     "It is important to note that effective organizational leadership requires a nuanced "
     "understanding of both interpersonal dynamics and strategic objectives. Furthermore, "
     "leaders must remain adaptive to an ever-evolving business landscape."),

    ("ai", "short",
     "The integration of renewable energy technologies into existing grid infrastructure "
     "presents significant technical and regulatory challenges that must be carefully addressed."),

    ("ai", "short",
     "Mental health awareness has become an increasingly important topic in contemporary "
     "discourse, as societies grapple with rising rates of anxiety and depression among "
     "various demographic groups."),

    ("ai", "short",
     "Blockchain technology offers a decentralized and immutable ledger system that has "
     "the potential to revolutionize supply chain management and financial transactions."),

    # ── AI MEDIUM (1–2 paragraphs) ─────────────────────────────────────────────
    ("ai", "medium",
     "The rapid advancement of large language models has fundamentally altered the landscape "
     "of natural language processing. These systems, trained on vast corpora of text data, "
     "demonstrate remarkable capabilities in tasks ranging from translation to code generation. "
     "It is essential, however, to critically evaluate the ethical implications of deploying "
     "such systems at scale, particularly with respect to issues of bias and misinformation."),

    ("ai", "medium",
     "Climate change represents one of the most pressing existential challenges of the "
     "twenty-first century. The scientific consensus is unambiguous: human activities, "
     "primarily the combustion of fossil fuels, are driving unprecedented increases in "
     "global average temperatures. Addressing this crisis requires coordinated international "
     "action and a fundamental transformation of energy systems worldwide."),

    ("ai", "medium",
     "The gig economy has introduced a new paradigm of labor characterized by flexibility "
     "and autonomy, yet it simultaneously raises important questions about worker protections "
     "and income stability. Policymakers must therefore develop regulatory frameworks that "
     "balance innovation with the need to ensure adequate social protections for all workers. "
     "This is particularly important given the disproportionate impact on lower-income populations."),

    ("ai", "medium",
     "Educational equity remains a persistent challenge in many developed and developing "
     "nations alike. Disparities in resource allocation, teacher quality, and access to "
     "technology continue to produce significant variation in educational outcomes across "
     "socioeconomic lines. It is therefore essential that governments prioritize targeted "
     "investment in underserved communities to address these structural inequalities."),

    ("ai", "medium",
     "The pharmaceutical industry plays a critical role in advancing public health through "
     "the development of novel therapeutics and vaccines. However, the high cost of drug "
     "development, combined with the profit motives of private corporations, frequently "
     "results in pricing structures that limit access for vulnerable populations. "
     "Furthermore, intellectual property protections can inhibit the production of "
     "affordable generic alternatives in low-income markets."),

    ("ai", "medium",
     "Social media platforms have fundamentally reshaped the way individuals consume and "
     "share information. While these technologies offer unprecedented connectivity and "
     "democratize access to information, they also facilitate the rapid spread of "
     "misinformation and contribute to increasing political polarization. "
     "It is therefore imperative that platforms invest in robust content moderation "
     "systems and algorithmic transparency measures."),

    ("ai", "medium",
     "Urban housing affordability has emerged as a critical policy challenge in many "
     "major metropolitan areas. Rapidly rising property values, driven by a combination "
     "of supply constraints and strong demand, have displaced lower-income residents from "
     "central urban neighborhoods. Consequently, policymakers must explore a range of "
     "interventions, including inclusionary zoning and community land trusts, to preserve "
     "housing affordability."),

    ("ai", "medium",
     "The increasing prevalence of remote work arrangements has significant implications "
     "for urban planning, transportation infrastructure, and commercial real estate markets. "
     "As workers gain greater flexibility in choosing their place of residence, many are "
     "opting to relocate from high-cost urban centers to more affordable suburban or rural "
     "areas. This trend is reshaping demand patterns and necessitating a fundamental "
     "rethinking of how cities are planned and governed."),

    ("ai", "medium",
     "Cybersecurity threats have grown in both sophistication and frequency in recent years, "
     "posing significant risks to critical infrastructure, financial systems, and personal "
     "data. Organizations must therefore adopt a proactive and multilayered approach to "
     "security that encompasses technical controls, employee training, and robust incident "
     "response planning. Furthermore, international cooperation is essential to address "
     "the cross-border nature of many cyber threats."),

    ("ai", "medium",
     "The aging demographic profile of many developed nations presents substantial fiscal "
     "challenges for public pension and healthcare systems. As the ratio of working-age "
     "adults to retirees continues to decline, governments must consider a range of "
     "policy responses, including adjustments to retirement ages, increased immigration, "
     "and structural reforms to entitlement programs. It is essential that these "
     "decisions be made with careful attention to issues of intergenerational equity."),

    # ── AI LONG (3–5 paragraphs) ───────────────────────────────────────────────
    ("ai", "long",
     "Artificial intelligence is fundamentally reshaping the nature of work across virtually "
     "every sector of the global economy. Automation technologies, powered by increasingly "
     "sophisticated machine learning algorithms, are displacing routine cognitive tasks that "
     "were once the exclusive domain of human workers. It is important to acknowledge that "
     "while this transformation creates significant economic disruption, it also generates "
     "new categories of employment that require higher-order skills.\n\n"
     "The educational implications of this technological shift are profound and far-reaching. "
     "Traditional pedagogical models, which prioritized the transmission of factual knowledge, "
     "are becoming increasingly inadequate in preparing students for an AI-driven labor market. "
     "Educational institutions must therefore undergo substantial reform to emphasize critical "
     "thinking and the capacity for continuous learning.\n\n"
     "Furthermore, the distributional consequences of AI-driven automation are likely to "
     "exacerbate existing socioeconomic inequalities if left unaddressed by policy interventions. "
     "Policymakers must develop targeted support mechanisms, including robust retraining programs "
     "and expanded social safety nets. In conclusion, the responsible development of artificial "
     "intelligence requires a holistic approach that addresses economic, educational, and "
     "governance dimensions simultaneously."),

    ("ai", "long",
     "The governance of data in the digital economy raises fundamental questions about "
     "privacy, ownership, and the distribution of economic value. As individuals generate "
     "ever-increasing volumes of data through their online activities, large technology "
     "companies have accumulated unprecedented concentrations of data wealth. It is important "
     "to note that current regulatory frameworks were largely designed for an earlier era and "
     "are inadequate to address the unique challenges posed by the data economy.\n\n"
     "The European Union's General Data Protection Regulation represents a significant attempt "
     "to reassert individual rights over personal data. However, the effectiveness of this "
     "framework has been limited by enforcement challenges and the global nature of data flows. "
     "Furthermore, the regulation places significant compliance burdens on smaller organizations "
     "while leaving the fundamental business models of large platforms largely intact.\n\n"
     "A more comprehensive approach to data governance would necessarily address the structural "
     "power imbalances between platform companies and both individual users and smaller competitors. "
     "This might include requirements for data portability and interoperability, as well as "
     "limitations on the use of data for targeted advertising. It is therefore essential that "
     "policymakers engage seriously with these structural questions rather than focusing solely "
     "on incremental reforms to existing frameworks."),

    ("ai", "long",
     "Global supply chains have undergone significant disruption in recent years as a result "
     "of the COVID-19 pandemic, geopolitical tensions, and extreme weather events associated "
     "with climate change. These disruptions have exposed the vulnerabilities of highly "
     "optimized but fragile just-in-time production systems that prioritize efficiency "
     "over resilience. It is consequently essential that firms and governments undertake "
     "a fundamental reassessment of supply chain strategy.\n\n"
     "The concept of supply chain resilience encompasses several distinct dimensions, including "
     "geographic diversification of suppliers, the maintenance of strategic inventory buffers, "
     "and investment in supply chain visibility technologies. Furthermore, firms must develop "
     "more robust risk assessment frameworks that account for low-probability but high-impact "
     "disruption scenarios.\n\n"
     "From a policy perspective, governments have increasingly sought to promote supply chain "
     "resilience through industrial policy measures, including subsidies for domestic production "
     "of critical goods and requirements for strategic stockpiling. While these measures can "
     "enhance national security, they also risk increasing costs and reducing the efficiency "
     "gains that have historically driven economic growth through international trade. "
     "It is therefore necessary to strike a careful balance between resilience and efficiency "
     "in the design of supply chain policy."),

    ("ai", "long",
     "The mental health crisis affecting contemporary societies demands urgent and "
     "comprehensive policy responses at multiple levels of governance. Rising rates of "
     "anxiety, depression, and other mental health conditions among both adolescent and "
     "adult populations represent a significant burden on individuals, families, and "
     "healthcare systems. It is important to note that these trends predate the COVID-19 "
     "pandemic, though the pandemic has significantly accelerated them.\n\n"
     "Access to mental health services remains profoundly inequitable, with significant "
     "disparities across socioeconomic, racial, and geographic dimensions. Rural populations "
     "in particular face acute shortages of mental health professionals, while cost barriers "
     "prevent many individuals from accessing needed care. Consequently, innovative service "
     "delivery models, including telehealth platforms and community-based interventions, "
     "must be more aggressively scaled.\n\n"
     "Furthermore, the social determinants of mental health, including housing instability, "
     "economic insecurity, and social isolation, must be addressed through cross-sectoral "
     "policy approaches. Mental health cannot be treated in isolation from broader social "
     "and economic conditions. In conclusion, achieving meaningful improvement in population "
     "mental health will require sustained political commitment and significant investment "
     "in both the mental health system and the social infrastructure that supports wellbeing."),

    ("ai", "long",
     "The transition to a net-zero carbon economy represents one of the most significant "
     "economic transformations in human history, requiring fundamental changes to energy "
     "production, transportation, industrial processes, and land use patterns. The scale "
     "and pace of investment required to achieve this transition within the timeframe "
     "necessary to limit warming to 1.5 degrees Celsius is unprecedented. It is therefore "
     "essential that both public and private capital be mobilized at scale.\n\n"
     "Carbon pricing mechanisms, including both carbon taxes and cap-and-trade systems, "
     "represent a critical tool for incentivizing emissions reductions across the economy. "
     "However, the political economy of carbon pricing is complex, and poorly designed "
     "systems risk placing disproportionate burdens on lower-income households. "
     "Furthermore, carbon leakage, whereby production shifts to jurisdictions with less "
     "stringent climate policies, remains a significant challenge for unilateral action.\n\n"
     "International climate finance is therefore essential to support developing nations "
     "in pursuing low-carbon development pathways. The commitments made at successive "
     "Conference of the Parties meetings have consistently fallen short of what is "
     "necessary. It is consequently imperative that developed nations fulfill their "
     "obligations and provide additional resources to support the climate transition "
     "in the Global South."),

    # ── HUMAN SHORT (1–3 sentences) ────────────────────────────────────────────
    ("human", "short",
     "just remembered i have a dentist appointment tomorrow and i am NOT ready for that"),

    ("human", "short",
     "three hours into this essay and i genuinely cannot remember what my thesis was supposed to be. "
     "starting over i guess"),

    ("human", "short",
     "my coworker microwaved fish again. we have discussed this. there is a sign. "
     "the sign is very clear."),

    ("human", "short",
     "why does my dog know when im sad but also bark at the same corner of the room "
     "every single night like something is there"),

    ("human", "short",
     "finally cleaned my room and now i genuinely cannot find anything because "
     "i put it all somewhere logical"),

    # ── HUMAN MEDIUM (1–2 paragraphs) ──────────────────────────────────────────
    ("human", "medium",
     "ok so i've been trying to get into running for like three years now and every time "
     "i start i make it about two weeks before something happens and i stop. last time it was "
     "because i bought the wrong shoes and got a blister. before that it was because it got cold. "
     "this time i told myself i'd go even when i don't want to and honestly? it's been six weeks "
     "and i've only skipped twice. not sure what changed but i'll take it."),

    ("human", "medium",
     "had the weirdest conversation with my dad last night. he called to ask how i was doing "
     "which is already unusual and then just. kept talking. for like 45 minutes. about his garden, "
     "his neighbor's dog, a podcast he heard about crows. i don't think he needed anything from me "
     "specifically, i think he just wanted to talk. it was kind of nice actually. sad that i found "
     "it so surprising."),

    ("human", "medium",
     "i've been trying to figure out why i hate networking events so much and i think i finally "
     "got it. it's not the talking to strangers part, i can do that. it's that everyone is trying "
     "to be the best version of themselves at the same time and the room ends up feeling fake "
     "in this specific way. like everyone's wearing the same face. coffee one on one with someone "
     "is completely different. same information exchange, way less exhausting."),

    ("human", "medium",
     "the apartment above me has been doing something that sounds like rolling a bowling ball "
     "across the floor every night between 11pm and midnight. not continuously. just. roll. "
     "silence. roll. silence. i've been here eight months and i have never once figured out "
     "what this could possibly be. i'm not even annoyed anymore, i'm just genuinely curious."),

    ("human", "medium",
     "started learning to make bread last month and the thing nobody tells you is that "
     "it is both incredibly forgiving and incredibly unforgiving at the same time. "
     "you can mess up a lot of steps and still get something edible. but if you rush "
     "the proof or the oven is even slightly off the whole thing just doesn't work. "
     "it's taught me more about patience than anything i've deliberately tried to learn patience from."),

    ("human", "medium",
     "watched a documentary about deep sea creatures last week and i genuinely cannot stop "
     "thinking about the anglerfish. the male bites into the female and their circulatory "
     "systems fuse together and he just. lives there. as part of her. forever. biologists "
     "called it 'sexual parasitism' which feels both accurate and not nearly enough. "
     "anyway i'm fine, why do you ask."),

    ("human", "medium",
     "got feedback on my writing today that was somehow both really useful and kind of crushing. "
     "the person was not wrong about any of it. the structure IS loose and the ending DOES trail off. "
     "but there's something about hearing accurate criticism that's harder to take than unfair criticism. "
     "unfair criticism you can dismiss. accurate criticism you just have to sit with."),

    ("human", "medium",
     "my grandmother used to say that the secret to a long marriage was to never stop "
     "being curious about the other person. i used to think that was kind of cheesy. "
     "now i think it's maybe the most practically useful piece of relationship advice "
     "i've ever heard. boredom is a choice you make about someone, not a thing that happens to you."),

    ("human", "medium",
     "there's a specific kind of tired that comes from a day where you were technically "
     "productive but nothing felt meaningful. checked every box, answered every email, "
     "was present in every meeting. and now it's 7pm and i feel like i spent the day "
     "doing things to avoid doing things. not sure what i wanted the day to look like "
     "but it wasn't this."),

    ("human", "medium",
     "i spent an embarrassing amount of time this weekend trying to remember the name "
     "of a song from a commercial i saw maybe fifteen years ago. i could hum the melody "
     "perfectly. i knew it had a female vocalist. that's it. that's all my brain kept. "
     "eventually found it by humming it to my phone. we live in a miraculous and also "
     "deeply weird time."),

    # ── HUMAN LONG (3–5 paragraphs) ────────────────────────────────────────────
    ("human", "long",
     "i keep starting journals and abandoning them after like two weeks. not because "
     "i run out of things to say but because i reread what i wrote and it sounds nothing "
     "like how i actually think. written me is always somehow more composed and boring "
     "than real me, which is frustrating because the whole point was to capture something true.\n\n"
     "maybe the problem is that writing forces you to finish your thoughts. when im just "
     "thinking i can trail off, backtrack, hold two contradictory things at once without "
     "resolving them. but the moment i write a sentence it has to go somewhere. it has to end. "
     "and the ending always feels like a lie because nothing in my head ever actually ends cleanly.\n\n"
     "theres something almost embarrassing about how much i want to document my own life. "
     "like who do i think is going to read this. nobody. not even future me, probably, "
     "because future me will have moved on to new anxieties and wont care what current me "
     "was worried about. and yet here i am, again, starting another document, fully aware "
     "it will go exactly the same way as all the others."),

    ("human", "long",
     "my grandmother made the best pierogi I have ever eaten in my life and I am convinced "
     "no restaurant will ever come close. She never used a recipe. She just knew. I watched "
     "her make them maybe a hundred times growing up and I still cant replicate whatever "
     "she was doing with the dough. Mine always come out a little too thick.\n\n"
     "She passed away three years ago and last Thanksgiving I tried to make them for the "
     "first time without her there to course correct me. My mom sat in the kitchen and "
     "tried to remember the details but neither of us really knew. We kept second guessing "
     "ourselves on the potato filling. Too much butter? Not enough onion? The ones we "
     "ended up with were fine but they tasted like a memory of a memory, you know?\n\n"
     "I think about that a lot when I cook now. How much knowledge just lives in a persons "
     "hands and nowhere else. She never wrote anything down because she never needed to. "
     "I wish I had just filmed her making them once, just once, instead of assuming "
     "she would always be there to show me."),

    ("human", "long",
     "took a solo trip last month for the first time in my life, just four days, nothing "
     "dramatic. flew somewhere i'd never been, had no plans, let myself wander. "
     "everyone said it would be this transformative experience of self-discovery. "
     "it was actually mostly just eating alone and walking a lot.\n\n"
     "but here's the thing. eating alone in a foreign city is genuinely underrated. "
     "no one to talk to means you actually pay attention to the food, the room, the people "
     "at other tables. i had a meal by myself at a small place on the second night that "
     "was maybe the most present i've felt in years. not happy exactly. just there.\n\n"
     "i don't know if i came back different. my friends keep asking what i learned about "
     "myself and the honest answer is not much, but i think that's okay. "
     "sometimes you go somewhere just to go somewhere. the point doesn't have to be "
     "the lesson. the point can just be that you did the thing."),

    ("human", "long",
     "i've been thinking a lot about the advice i give versus the advice i actually take. "
     "like if a friend told me they were exhausted and overwhelmed and not sleeping well, "
     "i would say slow down, say no to things, protect your energy. but when i'm the one "
     "who's exhausted and overwhelmed and not sleeping well i sign up for two more things "
     "and tell myself i'll rest when it calms down.\n\n"
     "it never calms down. that's not how it works and i know that. "
     "the pace doesn't decrease because you earn it, it decreases because you choose it. "
     "i know this. i've known this for years. i still don't do it.\n\n"
     "i think there's something in me that doesn't quite believe i deserve to rest "
     "unless i've done enough first. and i can't figure out how to define enough "
     "in a way that's actually reachable. it keeps moving. i think that's probably "
     "the thing i need to look at, but i'm going to finish this project first."),

    ("human", "long",
     "i grew up in a house where we didn't talk about money. not in a 'we're rich' way, "
     "in a 'this isn't discussed' way. i didn't know what my parents made, didn't know "
     "if we were struggling, didn't know anything. i just knew some things were possible "
     "and some weren't and you didn't ask why.\n\n"
     "i'm realizing now, in my thirties, how many of my assumptions about money came "
     "from that silence. i assumed debt was shameful. i assumed wanting things was "
     "embarrassing. i assumed that talking about financial stress was worse than "
     "experiencing it alone. none of those things are true but they feel true in a "
     "way that takes a lot of work to undo.\n\n"
     "my partner grew up in a family where money was discussed openly and practically, "
     "like any other household resource. watching them talk about it without shame or "
     "drama has been genuinely revelatory. not that their family had more, "
     "they didn't. just that they treated it like a fact instead of a secret. "
     "that's the thing i'm still trying to learn."),
]

# ── Run tests ─────────────────────────────────────────────────────────────────
print(f"Running {len(SAMPLES)} samples...\n")

results = []
for i, (true_label, size, text) in enumerate(SAMPLES):
    llm = get_llm_score(text)
    structural = get_structural_score(text)
    confidence = compute_confidence(llm, structural)
    prediction = get_label(confidence)
    correct = (
        (true_label == "ai"    and prediction == "likely_ai")    or
        (true_label == "human" and prediction == "likely_human")
    )
    wrong = (
        (true_label == "ai"    and prediction == "likely_human") or
        (true_label == "human" and prediction == "likely_ai")
    )
    results.append({
        "i": i + 1,
        "true": true_label,
        "size": size,
        "prediction": prediction,
        "confidence": confidence,
        "llm": llm,
        "structural": structural,
        "correct": correct,
        "wrong": wrong,
    })
    status = "✓" if correct else ("✗" if wrong else "~")
    print(f"[{i+1:02d}] {status} true={true_label:<6} size={size:<7} pred={prediction:<12} conf={confidence:.3f}  llm={llm:.2f}  struct={structural if structural is not None else 'N/A'}")

# ── Aggregate stats ────────────────────────────────────────────────────────────
print("\n" + "="*65)
print("AGGREGATE RESULTS")
print("="*65)

total       = len(results)
ai_samples  = [r for r in results if r["true"] == "ai"]
hum_samples = [r for r in results if r["true"] == "human"]

def stats(group, label):
    correct   = sum(1 for r in group if r["correct"])
    wrong     = sum(1 for r in group if r["wrong"])
    uncertain = sum(1 for r in group if not r["correct"] and not r["wrong"])
    print(f"\n{label} ({len(group)} samples)")
    print(f"  Correct   : {correct:>2} / {len(group)}  ({100*correct/len(group):.0f}%)")
    print(f"  Uncertain : {uncertain:>2} / {len(group)}  ({100*uncertain/len(group):.0f}%)")
    print(f"  Wrong     : {wrong:>2} / {len(group)}  ({100*wrong/len(group):.0f}%)")

stats(results,     "OVERALL")
stats(ai_samples,  "AI SAMPLES")
stats(hum_samples, "HUMAN SAMPLES")

# By size
for size in ("short", "medium", "long"):
    group = [r for r in results if r["size"] == size]
    if group:
        stats(group, f"SIZE: {size.upper()}")

# ── Outliers ──────────────────────────────────────────────────────────────────
print("\n" + "="*65)
print("NOTABLE OUTLIERS")
print("="*65)

for r in results:
    flag = None
    if r["wrong"]:
        flag = "WRONG LABEL"
    elif r["true"] == "ai" and r["confidence"] < 0.45:
        flag = "AI missed badly (confidence very low)"
    elif r["true"] == "human" and r["confidence"] > 0.55:
        flag = "Human flagged high (false positive risk)"
    if flag:
        print(f"\n[{r['i']:02d}] {flag}")
        print(f"     true={r['true']}  pred={r['prediction']}  conf={r['confidence']:.3f}  llm={r['llm']:.2f}  struct={r['structural']}")
        snippet = SAMPLES[r['i']-1][2][:120].replace('\n', ' ')
        print(f"     text: \"{snippet}...\"")
