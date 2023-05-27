class ResponseError(Exception):
    """Исключение ошибки сервиса Практикум.Домашка (код != 200)."""

    pass


class EndpointError(Exception):
    """Исключение недоступности сервиса Практикум.Домашка (код 404)."""

    pass


class RequestError(Exception):
    """Исключение при сбои сервиса Практикум.Домашка."""

    pass


class StatusError(Exception):
    """Исключение непредусмотренного статуса работы."""

    pass
