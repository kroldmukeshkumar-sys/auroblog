# ============================================================
#  trends.py  —  Google Trends se trending topics laata hai
#  Method: trends.google.com/trending?geo=IN  (RSS feed)
# ============================================================
import logging
import urllib.request
import xml.etree.ElementTree as ET
from config import Config

log = logging.getLogger(__name__)

# Google Trends RSS feed — India
TRENDS_RSS_URL = "https://trends.google.com/trending/rss?geo=IN"


def get_trending_topics():
    """India ke top trending topics fetch karo (Google Trends RSS)"""
    log.info("📈 Google Trends se topics fetch kar raha hoon...")
    try:
        req = urllib.request.Request(
            TRENDS_RSS_URL,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/123.0.0.0 Safari/537.36"
                )
            },
        )
        with urllib.request.urlopen(req, timeout=15) as resp:
            xml_data = resp.read()

        root = ET.fromstring(xml_data)
        # RSS: <item><title>Topic</title>...</item>
        topics = []
        for item in root.findall(".//item"):
            title_el = item.find("title")
            if title_el is not None and title_el.text:
                topics.append(title_el.text.strip())
            if len(topics) >= Config.TOPICS_PER_RUN:
                break

        if topics:
            log.info(f"   ✅ Topics mile: {topics}")
            return topics
        else:
            raise ValueError("RSS mein koi topic nahi mila")

    except Exception as e:
        log.error(f"   ❌ Trends error: {e}")
        # Fallback — agar trends nahi mile
        fallback = ["India News Today", "Technology India"]
        log.info(f"   ↩️  Fallback topics use kar raha hoon: {fallback}")
        return fallback
