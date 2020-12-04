import os
import requests
import time

from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()


def get_status(user_id):
    vk_token = os.getenv('VK_TOKEN')
    request = 'https://api.vk.com/method/users.get'
    params = {
        'user_ids': user_id,
        'fields': 'online',
        'access_token': vk_token,
        'v': '5.92'
    }
    response = requests.post(request, params=params)
    return response.json()['response'][0]['online']


def sms_sender(sms_text):
    twilio_client = Client(
        os.getenv('ACCOUNT_SID'),
        os.getenv('AUTH_TOKEN')
    )
    message = twilio_client.messages.create(
        body=sms_text,
        from_=os.getenv('NUMBER_FROM'),
        to=os.getenv('NUMBER_TO'),
    )
    return message.sid


if __name__ == '__main__':
    vk_id = input('Введите id ')
    get_status(vk_id)
    while True:
        if get_status(vk_id) == 1:
            sms_sender(
                f'{vk_id} сейчас онлайн!'
            )
            break
        time.sleep(5)
