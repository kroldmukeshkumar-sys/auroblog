# ============================================================
#  SETUP_GUIDE.md  —  Poora Setup Step by Step
# ============================================================

## Kya kya chahiye?
- ✅ Groq API Key (aapke paas hai)
- 🔲 Pexels API Key (free, 2 min mein milti hai)
- 🔲 Google Cloud OAuth Setup (Blogger ke liye)
- 🔲 Railway account (free deployment)


## ══════════════════════════════════════════
## STEP 1 — Pexels API Key lena (2 min)
## ══════════════════════════════════════════

1. https://www.pexels.com/api/ jaao
2. "Get Started for Free" click karo
3. Register karo (ya Google se login)
4. Dashboard mein API Key copy kar lo
5. Kahin save kar lo — baad mein Railway mein daalenge


## ══════════════════════════════════════════
## STEP 2 — Google Cloud Setup (Blogger ke liye)
## ══════════════════════════════════════════

### 2a. Google Cloud Project banao

1. https://console.cloud.google.com jaao
2. Upar "Select a project" > "New Project" click karo
3. Name: "AutoBlog" → Create

### 2b. Blogger API enable karo

1. Left menu > "APIs & Services" > "Library"
2. Search: "Blogger API v3"
3. Click karo > "Enable"

### 2c. OAuth Credentials banao

1. Left menu > "APIs & Services" > "Credentials"
2. "+ Create Credentials" > "OAuth client ID"
3. Pehli baar puchega "Configure consent screen":
   - User Type: External → Create
   - App name: "AutoBlog"
   - User support email: apni email
   - Save and Continue (baaki sab skip)
   - Test users mein apni email daalo
   - Back to Dashboard
4. Dobara "+ Create Credentials" > "OAuth client ID"
5. Application type: "Desktop app"
6. Name: "AutoBlog Desktop"
7. Create → "Download JSON" button click karo
8. Downloaded file ka naam: credentials.json karo
9. Yeh file project folder mein daalo


## ══════════════════════════════════════════
## STEP 3 — Blogger Blog ID nikalna
## ══════════════════════════════════════════

1. https://www.blogger.com jaao
2. Apna blog select karo
3. URL dekho: https://www.blogger.com/blog/posts/1234567890123456789
4. Woh number hi Blog ID hai → copy karo


## ══════════════════════════════════════════
## STEP 4 — Local pe pehli baar run karo
##           (Google Token generate karne ke liye)
## ══════════════════════════════════════════

### Python packages install karo:
```
pip install groq pytrends requests google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

### config.py mein temporary keys daalo:
```python
GROQ_API_KEY   = "aapki_groq_key"
PEXELS_API_KEY = "aapki_pexels_key"
BLOG_ID        = "aapka_blog_id"
PUBLISH_LIVE   = False   # pehle draft mode mein test karo!
```

### Run karo:
```
python main.py
```

### Kya hoga:
- Browser khulega → Google account se login karo
- Permission do (Blogger access)
- Terminal mein ek bada JSON print hoga — woh copy kar lo!
  (GOOGLE_TOKEN_JSON ke liye chahiye hoga)
- Blog pe ek draft post bani hogi — check karo

### Sab theek hai? Toh config.py mein:
```python
PUBLISH_LIVE = True   # ab live publish hoga
```


## ══════════════════════════════════════════
## STEP 5 — Railway pe Deploy karna
## ══════════════════════════════════════════

### 5a. GitHub pe code daalo

1. https://github.com jaao → New repository banao
2. Naam: "auto-blog"
3. Apne saare files upload karo:
   - config.py, main.py, trends.py
   - article_generator.py, image_fetcher.py
   - blogger_poster.py, requirements.txt, Procfile
   ⚠️  credentials.json aur token.pickle mat daalna (private hain!)

### 5b. Railway account banao

1. https://railway.app jaao
2. "Start a New Project" → GitHub se login karo
3. "Deploy from GitHub repo" → apna "auto-blog" repo select karo

### 5c. Environment Variables daalo

Railway dashboard > apna project > "Variables" tab:
```
GROQ_API_KEY       = sk-...aapki groq key...
PEXELS_API_KEY     = ...aapki pexels key...
BLOG_ID            = ...aapka blog id...
GOOGLE_TOKEN_JSON  = {...woh JSON jo terminal mein print hua tha...}
```

### 5d. Deploy!

1. Railway automatically deploy karega
2. Logs mein dekho — "AUTO BLOG RUN SHURU" dikhna chahiye
3. Har ghante 2 articles publish honge ✅


## ══════════════════════════════════════════
## TROUBLESHOOTING
## ══════════════════════════════════════════

❓ "Token expired" error Railway pe?
→ Local pe dobara python main.py run karo
→ Naya token JSON copy karo
→ Railway mein GOOGLE_TOKEN_JSON update karo

❓ Pytrends error?
→ Google Trends ka rate limit hit ho gaya
→ config.py mein RUN_EVERY_HOURS = 2 kar do

❓ Article mein image nahi aa rahi?
→ PEXELS_API_KEY check karo

❓ "Blog ID not found" error?
→ BLOG_ID sirf numbers hona chahiye, koi extra character nahi
