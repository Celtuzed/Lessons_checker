import os
import json
import time
import logging

import requests
import telegram

from dotenv import load_dotenv

TIMEOUT = 5
logger = logging.getLogger("tg_logger")

class TelegramLogsHandler(logging.Handler):

    def __init__(self, tg_bot, tg_chat_id):
        super().__init__()
        self.chat_id = tg_chat_id
        self.tg_bot = tg_bot

    def emit(self, record):
        log_entry = self.format(record)
        self.tg_bot.send_message(chat_id=self.chat_id, text=log_entry)


def main():
    load_dotenv()
    tg_token = os.getenv("TG_TOKEN")
    token = os.getenv("DVMN_TOKEN")
    tg_chat_id = os.getenv("TG_CHAT_ID")
    long_polling_url = "https://dvmn.org/api/long_polling/"
    tg_bot = telegram.Bot(token=tg_token)

    logging.basicConfig(format="%(message)s")
    logger.setLevel(logging.INFO)
    handler = TelegramLogsHandler(tg_bot, tg_chat_id)
    logger.addHandler(handler)

    logger.info('Запуск бота')
 
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
                new_attempt = reviews['new_attempts'][0]

                if new_attempt['is_negative']:
                    text = f"""У вас проверили работу "{new_attempt['lesson_title']}". К сожалению, в работе нашлись ошибки. Ссылка - {new_attempt['lesson_url']}"""
                    bot = telegram.Bot(token=tg_token)
                    bot.send_message(chat_id=tg_chat_id, text=text)

                else:
                    text = f"""У вас проверили работу "{new_attempt['lesson_title']}". Преподавателю всё понравилось, можно приступать к следующему уроку! Ссылка - {new_attempt['lesson_url']}"""
                    bot = telegram.Bot(token=tg_token)
                    bot.send_message(chat_id=tg_chat_id, text=text)

            elif reviews['status'] == "timeout":
                params = {
                    "timestamp": reviews['timestamp_to_request']
                }

        except requests.exceptions.ReadTimeout:
            pass
        except requests.exceptions.ConnectionError as error:
            logger.exception(error, exc_info=True)
            time.sleep(TIMEOUT)

if __name__ == '__main__':
    main()
    