import telebot
from bs4 import BeautifulSoup
import requests


def Parser():
    url = "https://freelance.habr.com/tasks?only_with_price=true&categories=development_bots"
    headers = {
        'Accept': '*/*',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
    }
    req = requests.get(url, headers=headers)
    with open('index.html', 'w', encoding='utf-8') as file:
        file.write(req.text)
    with open('index.html', 'r', encoding='utf-8') as file:
        src = file.read()
    soup = BeautifulSoup(src, "lxml")
    items = soup.find_all(class_='task task_list')
    black_list = " .запроектчасруб"
    INFO = list()
    with open('INDO.txt', 'w', encoding='utf-8') as file_txt:
        for item in items:
            price = item.find('span', class_='count').text
            for letter in black_list:
                price = price.replace(letter, '')
            title = item.find('div', class_='task__title').text.strip()
            time = item.find('span', class_='params__published-at icon_task_publish_at').text.strip()
            url = 'https://freelance.habr.com' + item.find('div', class_='task__title').find('a').get('href')
            INFO.append({
                "Title": title,
                "Price": price,
                "Time": time,
                "URL": url
            })
            file_txt.write(f"Title: {title}\nPrice: {price}\nTime: {time}\nURL: {url}\n\n")


token = "6818553818:AAFOEhrZ7erWav1SXuRUVfccNVH6pApbXms"
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def start_message(message):
    Parser()
    s = open("INDO.txt", "r", encoding="utf-8").read()
    bot.send_message(message.chat.id, s)
    bot.infinity_polling()