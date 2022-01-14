
class ExceptionSendMessage(Exception):
    """Исключение возникает при сбое отправки сообщения в Telegram."""


class ExceptionEndpointAvailability(Exception):
    """Исключение возникает из-за недоступности эндпоинта API-сервиса."""


class ExceptionNoHomeworksKey(Exception):
    """
    Исключение возникает из-за отсутсвия ключа 'homeworks' в ответе API.
    """


class ExceptionNoCurrentDateKey(Exception):
    """
    Исключение возникает из-за отсутсвия ключа 'current_date' в ответе API.
    """


class ExceptionNotCorrectType(Exception):
    """
    Исключение возникает из-за некорректного типа данных ответа API.
    """


class ExceptionHomeworkNotListType(Exception):
    """
    Исключение возникает из-за домашки не в виде спика в ответе от API.
    """


class ExceptionEmptyDict(Exception):
    """
    Исключение возникает из-за пустого словаря в ответе от API.
    """


class ExceptionHomeworkNameKeyNotFound(Exception):
    """
    Исключение возникает из-за отсутствия ключа 'homework_key' списке ДЗ.
    """


class ExceptionHomeworkStatusKeyNotFound(Exception):
    """
    Исключение возникает из-за отсутствия ключа 'homework_status' списке ДЗ.
    """
