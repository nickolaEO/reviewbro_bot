import logging
import os
import sys
import time
from http import HTTPStatus

import requests
import telegram
from dotenv import load_dotenv

from exceptions import (ExceptionEmptyDict,
                        ExceptionEndpointAvailability,
                        ExceptionHomeworkNotListType,
                        ExceptionNotCorrectType)

load_dotenv()

PRACTICUM_TOKEN = os.getenv('PRACTICUM_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

RETRY_TIME = 600
ENDPOINT = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
HEADERS = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}

HOMEWORK_STATUSES = {
    'approved': 'Работа проверена: ревьюеру всё понравилось. Ура!',
    'reviewing': 'Работа взята на проверку ревьюером.',
    'rejected': 'Работа проверена: у ревьюера есть замечания.'
}

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(stream=sys.stdout)
formatter = logging.Formatter(
    '%(asctime)s - %(levelname)s - %(message)s'
)
handler.setFormatter(formatter)
logger.addHandler(handler)


def send_message(bot, message):
    """Отправка сообщения в Telegram чат."""
    try:
        bot.send_message(
            chat_id=TELEGRAM_CHAT_ID,
            text=message,
        )
        logger.info(f'Сообщение отправлено в Telegram: {message}')
    except telegram.TelegramError as error:
        logger.error(f'Сбой при отправке сообщения: {error}')


def get_api_answer(current_timestamp):
    """Запрос к эндпоинту API-сервиса Практикум.Домашка."""
    timestamp = current_timestamp or int(time.time())
    params = {'from_date': timestamp}
    try:
        response = requests.get(
            ENDPOINT,
            headers=HEADERS,
            params=params
        )
        if response.status_code != HTTPStatus.OK:
            message = (
                f'Сбой в работе программы: Эндпоинт {ENDPOINT} недоступен. '
                f'Код ответа API: {response.status_code}'
            )
            logger.error(message)
            raise ExceptionEndpointAvailability(message)
        response = response.json()
        return response
    except ValueError as error:
        logger.error(error)
        raise
    except requests.RequestException as error:
        logger.error(f'Ошибка при запросе к эндпоинту: {error}')
        raise


def check_response(response):
    """Проверка ответа API-сервиса на корректность."""
    try:
        homeworks = response['homeworks']
        if not isinstance(response, dict):
            message = 'Ответ от API имеет некорректный тип'
            logger.error(message)
            raise ExceptionNotCorrectType(
                'Ответ от API имеет некорректный тип'
            )
        if not isinstance(homeworks, list):
            message = 'Домашки приходят не в виде списка в ответ от API'
            logger.error(message)
            raise ExceptionHomeworkNotListType(message)
        if not response:
            message = 'Ответ от API содержит пустой словарь'
            logger.error(message)
            raise ExceptionEmptyDict(message)
        return homeworks
    except KeyError as error:
        logger.error(
            f'Ответ от API не содержит ключа {error} в словаре {response}'
        )
        raise


def parse_status(homework):
    """Извлечение из списка конкретного ДЗ статуса работы."""
    try:
        homework_name = homework.get('homework_name')
        homework_status = homework.get('status')
        verdict = HOMEWORK_STATUSES[homework_status]
        return (
            f'Изменился статус проверки работы "{homework_name}". '
            f'{verdict}'
        )
    except KeyError as error:
        logger.error(
            f'Ответ от API не содержит ключа {error} в словаре {homework}'
        )
        raise


def check_tokens():
    """Проверка доступности переменных окружения, необходимых для работы."""
    message = 'Отсутствует обязательная переменная окружения'
    token_exists = True
    if PRACTICUM_TOKEN is None:
        token_exists = False
        logger.critical(
            f'{message} PRACTICUM_TOKEN'
        )
    if TELEGRAM_TOKEN is None:
        token_exists = False
        logger.critical(
            f'{message} TELEGRAM_TOKEN'
        )
    if TELEGRAM_CHAT_ID is None:
        token_exists = False
        logger.critical(
            f'{message} TELEGRAM_CHAT_ID'
        )
    return token_exists


def main():
    """Основная логика работы бота."""
    is_token_ok = check_tokens()
    if not is_token_ok:
        exit()
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    current_timestamp = int(time.time())
    current_status = ''
    while True:
        try:
            response = get_api_answer(current_timestamp)
            homework_list = check_response(response)
            for homework in homework_list:
                if (homework_list
                        and current_status != homework['status']):
                    current_status = homework['status']
                    message = parse_status(homework)
                    send_message(bot, message)
            current_timestamp = int(time.time())
            logger.info(
                'Изменения статуса отсутствуют, через 10 минут проверим API')
            time.sleep(RETRY_TIME)
        except Exception as error:
            message = f'Сбой в работе программы: {error}'
            logger.error(message)
            send_message(bot, message)
            time.sleep(RETRY_TIME)


if __name__ == '__main__':
    main()
