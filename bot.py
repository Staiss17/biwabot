import requests
from bs4 import BeautifulSoup
import telebot
import time

# === Налаштування ===
TELEGRAM_TOKEN = '7877454485:AAEcvCQPhE8zCUQYuwh9q0zIVLFEPW8aew4'
CHAT_ID = '375363349'
NITTER_URL = 'https://nitter.net/BinanceWallet'

bot = telebot.TeleBot(TELEGRAM_TOKEN)
last_post = None

while True:
    print("🔄 Перевірка нових постів...")

    try:
        response = requests.get(NITTER_URL, headers={"User-Agent": "Mozilla/5.0"})
        print(f"Статус код запиту: {response.status_code}")
        
        if response.status_code != 200:
            print("❌ Помилка при запиті на сайт. Статус код:", response.status_code)
            time.sleep(60)
            continue

        soup = BeautifulSoup(response.text, 'html.parser')
        tweet = soup.find('div', {'class': 'timeline-item'})
        if tweet:
            link_tag = tweet.find('a', href=True)
            if link_tag:
                post_link = link_tag['href']
                full_link = "https://nitter.net" + post_link

                if full_link != last_post:
                    last_post = full_link
                    bot.send_message(CHAT_ID, f"🟡 Нова публікація BinanceWallet:\n{full_link}")
                    print(f"✅ Надіслано нову публікацію: {full_link}")
                else:
                    print("🕓 Нових постів немає.")
            else:
                print("❌ Посилання не знайдено.")
        else:
            print("❌ Не знайдено пости.")
    except Exception as e:
        print("⚠️ Виникла помилка:", e)

    time.sleep(60)
