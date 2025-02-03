import requests
from constance import config
import logging


BASE_URL = f'https://api.green-api.com/waInstance{config.GREEN_API_INSTANCE_ID}/SendMessage/{config.GREEN_API_TOKEN}'

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ])

def send_whatsapp_message(phone_number, message):
    if "+" in phone_number:
        phone_number = phone_number.replace('+', '')
    if phone_number.startswith('8'):
        phone_number = phone_number.replace('8', '7', 1)

    data = {
        "chatId": f"{phone_number}@c.us",
        "message": message
    }

    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.post(BASE_URL, json=data, headers=headers)
    if response.status_code == 200:

        logging.info("Сообщение успешно отправлено")
    else:
        logging.info(f"Ошибка отправки: {response.status_code}, {response.text}")

