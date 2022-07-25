import os
import json
import time

import requests
import telegram

from dotenv import load_dotenv

def send_message(bot_token, tg_chat_id, text):
    bot = telegram.Bot(token=bot_token)
    bot.send_message(chat_id=tg_chat_id, text=text)

def main():
    load_dotenv()
    bot_token = os.getenv("TG_TOKEN")
    token = os.getenv("DVMN_TOKEN")
    tg_chat_id = os.getenv("TG_CHAT_ID")
    long_polling_url = "https://dvmn.org/api/long_polling/"
    headers = {
        "Authorization" : f"Token {token}"
    }
    params = {
        "timestamp": time.time()
    }           
    while True:
        try:
            response = requests.get(long_polling_url, params=params, headers=headers)
            response.raise_for_status()
            reviews = response.json()
            if reviews['status'] == "found":
                params = {
                    "timestamp": reviews['last_attempt_timestamp']
                }
                new_attempts = reviews['new_attempts'][0]
                if new_attempts['is_negative'] == True:
                    text = f"""У вас проверили работу "{new_attempts['lesson_title']}". К сожалению, в работе нашлись ошибки. Ссылка - {new_attempts['lesson_url']}"""
                    send_message(bot_token, tg_chat_id, text)
                else:
                    text = f"""У вас проверили работу "{new_attempts['lesson_title']}". Преподавателю всё понравилось, можно приступать к следующему уроку! Ссылка - {new_attempts['lesson_url']}"""

                    send_message(bot_token, tg_chat_id, text)
            if reviews['status'] == "timeout":
                params = {
                    "timestamp": reviews['timestamp_to_request']
                }
        except requests.exceptions.ReadTimeout:
            print("ReadTimeout")
        except requests.exceptions.ConnectionError:
            print("ConnectionError")

if __name__ == '__main__':
    main()