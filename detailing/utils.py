import requests
from dotenv import load_dotenv
from os import getenv

load_dotenv()

INSTANCE_ID = getenv('INSTANCE_ID')
API_TOKEN = getenv('API_TOKEN')
BASE_URL = f'https://api.green-api.com/waInstance{INSTANCE_ID}'

def send_whatsapp_message(phone_number, message):
    url = f'{BASE_URL}/SendMessage/{API_TOKEN}'
    data = {
        "chatId": f"{phone_number}@c.us",
        "message": message
    }
    response = requests.post(url, json=data)
    if response.status_code == 200:
        print("Сообщение успешно отправлено")
    else:
        print(f"Ошибка отправки: {response.status_code}, {response.text}")
