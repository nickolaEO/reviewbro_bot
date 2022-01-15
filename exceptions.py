class ExceptionEndpointAvailability(Exception):
    """Исключение возникает из-за недоступности эндпоинта API-сервиса."""
    ...


class ExceptionNotCorrectType(Exception):
    """
    Исключение возникает из-за некорректного типа данных ответа API.
    """
    ...


class ExceptionHomeworkNotListType(Exception):
    """
    Исключение возникает из-за домашки не в виде спика в ответе от API.
    """
    ...


class ExceptionEmptyDict(Exception):
    """
    Исключение возникает из-за пустого словаря в ответе от API.
    """
    ...
