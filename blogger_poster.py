# ============================================================
#  blogger_poster.py  —  Google Blogger pe post karta hai
# ============================================================
import os, json, logging, pickle
from datetime import datetime
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from config import Config

log = logging.getLogger(__name__)
SCOPES = ["https://www.googleapis.com/auth/blogger"]
TOKEN_FILE  = "token.pickle"
CREDS_FILE  = "credentials.json"


def _get_credentials():
    """
    Google OAuth credentials lo.
    Local mein: browser se login karega (pehli baar).
    Railway pe: GOOGLE_TOKEN_JSON env var se load karega.
    """
    creds = None

    # ── Railway / server: env var se token load karo ──────
    if Config.GOOGLE_TOKEN_JSON:
        try:
            token_data = json.loads(Config.GOOGLE_TOKEN_JSON)
            creds = Credentials.from_authorized_user_info(token_data, SCOPES)
            log.info("   Token env var se load hua")
        except Exception as e:
            log.error(f"   Env token load error: {e}")

    # ── Local: pickle file se ──────────────────────────────
    elif os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "rb") as f:
            creds = pickle.load(f)
        log.info("   Token pickle se load hua")

    # ── Refresh karo agar expire ho gaya ──────────────────
    if creds and creds.expired and creds.refresh_token:
        try:
            creds.refresh(Request())
            log.info("   Token refresh hua ✅")
            _save_token(creds)
        except Exception as e:
            log.error(f"   Token refresh failed: {e}")
            creds = None

    # ── Pehli baar login (sirf local pe kaam karega) ───────
    if not creds or not creds.valid:
        if not os.path.exists(CREDS_FILE):
            raise FileNotFoundError(
                "credentials.json nahi mili!\n"
                "Google Cloud Console se download karo.\n"
                "SETUP_GUIDE.md mein poori guide hai."
            )
        flow  = InstalledAppFlow.from_client_secrets_file(CREDS_FILE, SCOPES)
        creds = flow.run_local_server(port=0)
        log.info("   Browser se login hua ✅")
        _save_token(creds)

    return creds


def _save_token(creds):
    """Token save karo — local + Railway ke liye print karo"""
    with open(TOKEN_FILE, "wb") as f:
        pickle.dump(creds, f)

    # Railway ke liye JSON format mein bhi print karo
    token_json = creds.to_json()
    log.info("\n" + "="*60)
    log.info("📋  GOOGLE_TOKEN_JSON (Railway mein daalo):")
    log.info(token_json)
    log.info("="*60 + "\n")


def post_to_blogger(article: dict, topic: str) -> str | None:
    """
    Article ko Blogger pe publish karo.
    Returns: published post URL ya None (error pe)
    """
    log.info(f"📤  Blogger pe post kar raha hoon: '{article['title']}'")

    try:
        creds   = _get_credentials()
        service = build("blogger", "v3", credentials=creds)

        # Article ke neeche footer add karo
        footer = f"""
<hr style="margin:40px 0;border:none;border-top:1px solid #eee;"/>
<div style="background:#f8f9fa;padding:16px 20px;border-radius:8px;
            font-size:13px;color:#666;line-height:1.8;">
  <strong>📌 Trending Topic:</strong> {topic}<br/>
  <strong>🕐 Published:</strong> {datetime.now().strftime("%d %B %Y — %I:%M %p IST")}<br/>
  <em>Auto-generated article based on trending Google searches in India.</em>
</div>"""

        body = {
            "kind":    "blogger#post",
            "title":   article["title"],
            "content": article["content_html"] + footer,
            "labels":  article.get("tags", [topic]),
        }

        result = service.posts().insert(
            blogId=Config.BLOG_ID,
            body=body,
            isDraft=not Config.PUBLISH_LIVE,
        ).execute()

        url = result.get("url", "N/A")
        log.info(f"   ✅ Post live: {url}")
        return url

    except Exception as e:
        log.error(f"   ❌ Blogger error: {e}")
        return None
