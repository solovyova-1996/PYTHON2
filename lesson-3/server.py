import sys
from json import JSONDecodeError
from logging import getLogger
from socket import socket, AF_INET, SOCK_STREAM

from general.utils import get_messages, send_mesages
from general.variables import ACTION, GREETINGS, TIME, USER, ACCOUNT_NAME, \
    RESPONSE, ERROR, PORT_ARGV, DEFAULT_PORT, IP_ARGV, MAX_CONNECTIONS

from config import server_log_config
from decorators_log import log_func

log = getLogger('server')


@log_func
def handler_client_messages(messages):
    # проверка есть ли в сообщении(словаре) ключи: 'action', 'time', 'user' и что находиться в этих полях
    if ACTION in messages and messages[
        ACTION] == GREETINGS and TIME in messages and USER in messages and \
            messages[USER][ACCOUNT_NAME] == 'Guest':
        log.info(
            'Клиент- %(account_name)s подключился к серверу(отправил корректный запрос)',
            messages[USER])
        return {RESPONSE: 200}
    log.error('Клиент отправил некорректный запрос на подключение')
    return {RESPONSE: 400, ERROR: 'Bad Request'}


def main():
    try:
        # если указан параметр порта в командной строке
        # print(sys.argv)
        # если порт передан в командной строке то выставляем его если нет,то выставляем порт по default
        listen_port = int(sys.argv[sys.argv.index(
            PORT_ARGV) + 1]) if PORT_ARGV in sys.argv else DEFAULT_PORT
        # если указан служебный порт или несуществующий вызываем ошибку
        if listen_port < 1024 or listen_port > 65535:
            raise ValueError
    except IndexError:
        log.critical(
            'Указаны неверные параметры при запуске сервера.После параметра -\'p\' необходимо указать номер порта.Process finished with exit code 1')
        # print('После параметра -\'p\' необходимо указать номер порта.')
        sys.exit(1)
    except ValueError:
        param = {'listen_port': listen_port}
        log.critical(
            'Номер порта не удовлетворяет условию -от 1024 до 65535.Переданный порт- %(listen_port)d.Process finished with exit code 1',
            param)
        # print('В качастве порта может быть указано только число в диапазоне от 1024 до 65535.')
        sys.exit(1)

    try:
        # узнаем какой адрес слушать
        listen_ip_addr = sys.argv[
            sys.argv.index(IP_ARGV) + 1] if IP_ARGV in sys.argv else ''
    except IndexError:
        log.critical(
            'Указаны неверные параметры при запуске сервера.После параметра \'a\'- необходимо указать адрес, который будет слушать сервер.Process finished with exit code 1')
        # print('После параметра \'a\'- необходимо указать адрес, который будет слушать сервер.')
        sys.exit(1)
    # создаем сокет AF_INET-сетевой, SOCK_STREAM - тип сокета потоковый
    sock_1 = socket(AF_INET, SOCK_STREAM)
    # привязываем сокет к ip адресу и порту машины
    sock_1.bind((listen_ip_addr, listen_port))
    # сигнализируем о готовности принимать соединение MAX_CONNECTIONS - количество одновременно обслуживаемых запросов
    sock_1.listen(MAX_CONNECTIONS)
    while True:
        # accept - принимает запрос на соединение
        client, client_ip_addr = sock_1.accept()
        # print(f'client:{client}\nclient_ip_addr:{client_ip_addr}')
        try:
            # client-тот кто подключился к серверу, get_messages -получает данные от сервера если данные переданы корректно декодирует и возвращает их
            messages_from_client = get_messages(client)
            # print(f'messages_from_client:{messages_from_client}')
            #  код ответа 200 или 400
            response = handler_client_messages(messages_from_client)
            # отпра правляет данные
            send_mesages(client, response)
            client.close()
        except (JSONDecodeError, TypeError, ValueError):

            log.warning('Принято некорретное сообщение от клиента.')
            # print('Принято некорретное сообщение от клиента.')
            client.close()


if __name__ == '__main__':
    main()
