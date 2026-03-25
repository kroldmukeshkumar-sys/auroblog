# ============================================================
#  main.py  —  GitHub Actions Version (No Loop)
# ============================================================
import logging, time
from datetime import datetime
from config import Config
from trends import get_trending_topics
from article_generator import generate_article
from image_fetcher import get_image, inject_image_into_article
from blogger_poster import post_to_blogger

# ── Logging setup ──────────────────────────────────────────
# GitHub Actions ke liye StreamHandler zaroori hai
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s %(message)s",
    datefmt="%d-%b %H:%M",
    handlers=[
        logging.StreamHandler(), 
    ],
)
log = logging.getLogger(__name__)


# ============================================================
#  EK FULL RUN — Trends → Article → Image → Post
# ============================================================
def run_once():
    log.info("")
    log.info("=" * 58)
    log.info(f"🚀  AUTO BLOG RUN SHURU — {datetime.now().strftime('%d %b %Y  %H:%M')}")
    log.info("=" * 58)

    topics  = get_trending_topics()
    results = []

    for i, topic in enumerate(topics, 1):
        log.info(f"\n── Topic {i}/{len(topics)}: {topic} ──")
        try:
            # Step 1: Article likhao
            article = generate_article(topic)

            # Step 2: Image lo
            img_url, photographer = get_image(article.get("image_query", topic))

            # Step 3: Image article mein daalo
            article["content_html"] = inject_image_into_article(
                article["content_html"], img_url, photographer, topic
            )

            # Step 4: Blogger pe post karo
            url = post_to_blogger(article, topic)

            results.append({
                "topic":  topic,
                "title":  article["title"],
                "url":    url,
                "status": "✅ success" if url else "❌ failed",
            })

        except Exception as e:
            log.error(f"   ❌ Topic '{topic}' mein error: {e}")
            results.append({"topic": topic, "status": f"❌ error: {e}"})

        # Dono topics ke beech thoda wait (API safety ke liye)
        if i < len(topics):
            log.info(f"   ⏳ {Config.DELAY_BETWEEN}s wait kar raha hoon...")
            time.sleep(Config.DELAY_BETWEEN)

    # ── Summary ───────────────────────────────────────────
    log.info("")
    log.info("─" * 58)
    log.info("📊  SESSION SUMMARY")
    log.info("─" * 58)
    for r in results:
        log.info(f"  {r['status']}  {r.get('title', r['topic'])}")
        if r.get("url"):
            log.info(f"           🔗 {r['url']}")
    log.info("─" * 58)


# ============================================================
#  MAIN EXECUTION — GitHub isse trigger karega
# ============================================================
def main():
    log.info("🤖  Auto Blog Bot (GitHub Mode) start ho gaya!")
    log.info(f"   Language: {Config.ARTICLE_LANGUAGE} | Live: {Config.PUBLISH_LIVE}")

    # GitHub Actions mein hum loop nahi chalate kyunki 
    # GitHub khud har ghante script ko fresh start karta hai.
    run_once()

    log.info("✅ Run complete. GitHub will trigger this again in 1 hour.")

if __name__ == "__main__":
    main()
