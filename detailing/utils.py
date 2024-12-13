import requests
from dotenv import load_dotenv
from os import getenv

load_dotenv()

INSTANCE_ID = getenv('INSTANCE_ID')
API_TOKEN = getenv('API_TOKEN')
BASE_URL = f'https://api.green-api.com/waInstance{INSTANCE_ID}/SendMessage/{API_TOKEN}'


def send_whatsapp_message(phone_number, message):
    if "+" in phone_number:
        phone_number = phone_number.replace('+', '')

    data = {
        "chatId": f"{phone_number}@c.us",
        "message": message
    }

    response = requests.post(BASE_URL, json=data)

    if response.status_code == 200:
        print("Сообщение успешно отправлено")
    else:
        print(f"Ошибка отправки: {response.status_code}, {response.text}")

