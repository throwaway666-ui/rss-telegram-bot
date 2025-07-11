import os
import feedparser
import google.generativeai as genai
import telebot

# Load env vars
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
RSS_FEED_URL = os.getenv("RSS_FEED_URL", "https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml")

# Setup APIs
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-pro")
bot = telebot.TeleBot(TELEGRAM_TOKEN)

def fetch_and_summarize():
    feed = feedparser.parse(RSS_FEED_URL)
    summaries = []

    for entry in feed.entries[:5]:  # Limit to top 5
        title = entry.title
        link = entry.link
        description = entry.summary

        try:
            prompt = f"Summarize this news article for a Telegram update:\n\nTitle: {title}\n\nDescription: {description}"
            response = model.generate_content(prompt)
            summary = response.text.strip()
            summaries.append(f"📰 *{title}*\n{summary}\n[Read more]({link})\n")
        except Exception as e:
            summaries.append(f"❌ Error summarizing: {title}\n{str(e)}")

    return summaries

def send_to_telegram(messages):
    for msg in messages:
        bot.send_message(TELEGRAM_CHAT_ID, msg, parse_mode='Markdown')

if __name__ == "__main__":
    summaries = fetch_and_summarize()
    send_to_telegram(summaries)
