# ============================================================
#  article_generator.py  —  Groq AI se article likhwata hai
# ============================================================
import json, logging
from groq import Groq
from config import Config

log = logging.getLogger(__name__)

# Language instructions
LANG_MAP = {
    "english":  "Write the entire article in English.",
    "hindi":    "पूरा आर्टिकल हिंदी में लिखो। Roman script use mat karo।",
    "hinglish": (
        "Write in Hinglish — base language is English but naturally mix "
        "Hindi words and phrases like 'matlab', 'yani ki', 'lekin', "
        "'aur bhi', 'samjhe?', 'bilkul'. Make it feel like a "
        "smart Indian friend explaining something. Don't force Hindi — "
        "use it where it feels natural."
    ),
}


def generate_article(topic: str) -> dict:
    """
    Groq se ek poora blog article generate karo.
    Returns dict: title, meta_description, content_html, tags, image_query
    """
    log.info(f"✍️  Article likh raha hoon topic: '{topic}'")

    lang_instruction = LANG_MAP.get(Config.ARTICLE_LANGUAGE, LANG_MAP["hinglish"])

    system_prompt = """You are an expert blog writer for an Indian audience. 
You write engaging, informative articles that rank well on Google.
You always return ONLY valid JSON — no markdown, no backticks, no extra text."""

    user_prompt = f"""Write a complete blog post about this trending topic: "{topic}"

Language: {lang_instruction}

Requirements:
- Length: 750-950 words
- Catchy, SEO-friendly title
- Structure: Strong intro → 3-4 sections with <h2> subheadings → engaging conclusion
- Tone: Informative yet conversational, like explaining to a smart friend
- Include real facts, numbers, or examples where possible
- End with: "Aapka kya khayal hai? Neeche comment karein!" (or English equivalent)
- Use <strong> for important keywords

Return ONLY this JSON (no extra text, no markdown fences):
{{
  "title": "Your catchy article title here",
  "meta_description": "SEO description — under 155 characters, includes main keyword",
  "content_html": "<h1>Title</h1><p>intro...</p><h2>Section 1</h2><p>...</p>... full article HTML",
  "tags": ["tag1", "tag2", "tag3", "tag4", "tag5"],
  "image_query": "3-5 word English phrase to find a relevant stock photo"
}}"""

    client = Groq(api_key=Config.GROQ_API_KEY)

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",   # Groq ka best free model
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": user_prompt},
        ],
        temperature=0.75,
        max_tokens=2500,
    )

    raw = response.choices[0].message.content.strip()

    # Safety cleanup — agar model ne backticks daale ho
    if raw.startswith("```"):
        raw = raw.split("```", 1)[1]
        if raw.startswith("json"):
            raw = raw[4:]
        raw = raw.rsplit("```", 1)[0]

    article = json.loads(raw.strip())
    log.info(f"   ✅ Article ready: '{article['title']}'")
    return article
