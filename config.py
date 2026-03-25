# ============================================================
#  config.py  —  Saari settings yahan hain
#  Railway pe Environment Variables mein daalenge (safe!)
# ============================================================
import os

class Config:

    # 1. GROQ API KEY — https://console.groq.com
    GROQ_API_KEY      = os.getenv("GROQ_API_KEY", "")

    # 2. PEXELS API KEY (free) — https://www.pexels.com/api/
    PEXELS_API_KEY    = os.getenv("PEXELS_API_KEY", "")

    # 3. BLOGGER BLOG ID
    #    Blogger dashboard > apna blog kholo > URL mein number hoga
    #    Example: blogger.com/blog/posts/1234567890  ==>  "1234567890"
    BLOG_ID           = os.getenv("BLOG_ID", "")

    # 4. GOOGLE OAuth token (Railway pe env var mein daalenge)
    GOOGLE_TOKEN_JSON = os.getenv("GOOGLE_TOKEN_JSON", "")

    # ── AUTOMATION SETTINGS ────────────────────────────────
    TOPICS_PER_RUN    = 2           # Har run mein kitne articles
    TREND_GEO         = "india"     # Kis desh ke trends
    DELAY_BETWEEN     = 40          # 2 articles ke beech gap (seconds)
    ARTICLE_LANGUAGE  = "english"   # "english" / "hindi" / "hinglish"
    PUBLISH_LIVE      = True        # False = draft mein save hoga
    RUN_EVERY_HOURS   = 1           # Har kitne ghante mein chalega
