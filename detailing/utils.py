import requests
from constance import config

BASE_URL = f'https://api.green-api.com/waInstance{config.GREEN_API_INSTANCE_ID}/SendMessage/{config.GREEN_API_TOKEN}'




def send_whatsapp_message(phone_number, message):
    if "+" in phone_number:
        phone_number = phone_number.replace('+', '')

    data = {
        "chatId": f"{phone_number}@c.us",
        "message": message
    }

    response = requests.post(BASE_URL, json=data)

    if response.status_code == 200:
        print("Сообщение успешно отправлено", phone_number, message)
    else:
        print(f"Ошибка отправки: {response.status_code}, {response.text}")

