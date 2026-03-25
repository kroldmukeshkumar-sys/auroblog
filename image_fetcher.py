# ============================================================
#  image_fetcher.py  —  Pexels se free HD image laata hai
# ============================================================
import logging, requests
from config import Config

log = logging.getLogger(__name__)


def get_image(query: str):
    """
    Pexels API se topic ke liye best image dhundho.
    Returns: (image_url, photographer_name) ya (None, None)
    """
    log.info(f"🖼️  Image dhundh raha hoon: '{query}'")

    if not Config.PEXELS_API_KEY:
        log.warning("   ⚠️  Pexels key nahi hai — image skip")
        return None, None

    try:
        resp = requests.get(
            "https://api.pexels.com/v1/search",
            headers={"Authorization": Config.PEXELS_API_KEY},
            params={
                "query": query,
                "per_page": 3,
                "orientation": "landscape",
                "size": "large",
            },
            timeout=10,
        )
        resp.raise_for_status()
        photos = resp.json().get("photos", [])

        if photos:
            photo = photos[0]
            url   = photo["src"]["large2x"]
            name  = photo["photographer"]
            log.info(f"   ✅ Image mili — by {name}")
            return url, name

        log.warning("   ⚠️  Koi photo nahi mili is query mein")
        return None, None

    except Exception as e:
        log.error(f"   ❌ Pexels error: {e}")
        return None, None


def build_image_html(img_url: str, photographer: str, topic: str) -> str:
    """Image ke liye clean HTML block banao"""
    if not img_url:
        return ""

    return f"""
<div style="margin:32px 0;text-align:center;">
  <img src="{img_url}"
       alt="{topic}"
       style="max-width:100%;height:auto;border-radius:12px;
              box-shadow:0 6px 20px rgba(0,0,0,0.15);" />
  <p style="margin-top:8px;font-size:12px;color:#999;">
    Photo by <strong>{photographer}</strong> on Pexels
  </p>
</div>
"""


def inject_image_into_article(html: str, img_url: str,
                               photographer: str, topic: str) -> str:
    """Image ko article mein pehle <h2> ke baad daalo"""
    img_html = build_image_html(img_url, photographer, topic)
    if not img_html:
        return html

    lower = html.lower()
    pos = lower.find("</h2>")      # pehla h2 closing tag
    if pos == -1:
        pos = lower.find("</h1>")  # fallback: h1 ke baad
    if pos == -1:
        return img_html + html     # koi heading nahi mili

    insert_at = pos + len("</h2>") if "</h2>" in lower else pos + len("</h1>")
    return html[:insert_at] + img_html + html[insert_at:]
