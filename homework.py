import logging
import os
import requests
import sys
import time

from http import HTTPStatus
from dotenv import load_dotenv
from telegram import Bot

from exceptions import ResponseError, EndpointError, RequestError, StatusError


load_dotenv()


PRACTICUM_TOKEN = os.getenv('PRACTICUM_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

RETRY_PERIOD = 600
ENDPOINT = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
HEADERS = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}


HOMEWORK_VERDICTS = {
    'approved': 'Работа проверена: ревьюеру всё понравилось. Ура!',
    'reviewing': 'Работа взята на проверку ревьюером.',
    'rejected': 'Работа проверена: у ревьюера есть замечания.'
}

logger = logging.getLogger(__name__)


def check_tokens():
    """Проверка наличия необходимых переменных."""
    tokens = PRACTICUM_TOKEN and TELEGRAM_CHAT_ID and TELEGRAM_TOKEN
    if tokens:
        return tokens
    return False


def send_message(bot, message):
    """Отправка сообщения в чат телеграм."""
    try:
        logger.debug('В чат отправлено сообщение')
        bot.send_message(TELEGRAM_CHAT_ID, message)
        logger.debug('Сообщение доставлено успешно')

    except Exception as error:
        logger.error(f'Не получилось отправить сообщение: {error}')


def get_api_answer(timestamp):
    """Запрос к эндпойнту возвращается ответ API в формате JSON."""
    try:
        homework_statuses = requests.get(
            ENDPOINT,
            headers=HEADERS,
            params={'from_date': timestamp}
        )

    except requests.RequestException as error:
        raise RequestError(f'Произошел сбой при обращении к серверу: {error}')

    if homework_statuses.status_code != HTTPStatus.OK:
        raise ResponseError('Ошибка при запросе сервиса Практикум.Домашка')

    if homework_statuses.status_code == HTTPStatus.NOT_FOUND:
        raise EndpointError('Эндпойнт недоступен')
    return homework_statuses.json()


def check_response(response):
    """Проверка ответа API на соответствие документации."""
    print(response)
    if not isinstance(response, dict):
        raise TypeError(f'Ответ не словарь. Ответ {response}')

    if not response.get('current_date'):
        raise KeyError('В ответе нет ключа current_date')

    if not response.get('homeworks'):
        raise KeyError('В ответе нет ключа homeworks')

    homeworks = response.get('homeworks')
    if not isinstance(homeworks, list):
        raise TypeError('Значение по ключу homework не является списком')

    return homeworks


def parse_status(homework):
    """Извлекаем статус домашней работы."""
    homework_name = homework.get('homework_name')
    status = homework.get('status')

    if not homework_name:
        raise KeyError('В ответе нет ключа имени')

    if not status:
        raise KeyError('В ответе нет статуса работы')

    if status not in HOMEWORK_VERDICTS:
        raise StatusError('Статус работы является некорректным')

    verdict = HOMEWORK_VERDICTS.get(status)
    return f'Изменился статус проверки работы "{homework_name}". {verdict}'


def main():
    """Основная логика работы бота."""
    if not check_tokens():
        logger.critical('Проверьте наличие всех переменных')
        sys.exit()
    bot = Bot(token=TELEGRAM_TOKEN)
    timestamp = 0
    prev_report = {}
    prev_message = ''
    check_send_mes = False
    while True:
        try:
            response = get_api_answer(timestamp)
            report = check_response(response)[0]
            if prev_report != report:
                logger.info('Статус работы изменился')
                send_message(bot, parse_status(report))
                prev_report = report.copy()
                timestamp = response.get('current_date')
            else:
                logger.info('Статус работы не изменен')

        except ResponseError as error:
            logger.error(error)
            message = f'Сбой в работе программы: {error}'
            if message != prev_message:
                send_message(bot, message)
                check_send_mes = True
                if check_send_mes is True:
                    prev_message = message

        finally:
            time.sleep(RETRY_PERIOD)


if __name__ == '__main__':
    logger.setLevel(logging.INFO)
    logger.setLevel(logging.ERROR)
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    main()
