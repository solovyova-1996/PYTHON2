import sys
from json import JSONDecodeError
from logging import getLogger
from socket import socket, AF_INET, SOCK_STREAM
from time import time
from general.utils import send_mesages, get_messages

from general.variables import ACTION, GREETINGS, TIME, USER, ACCOUNT_NAME, \
    RESPONSE, ERROR, DEFAULT_IP_ADDRESS, DEFAULT_PORT

from config import client_log_config

log = getLogger('client')


def create_greetings(account_name='Guest'):
    # генерация запроса о присутствии клиента
    return {ACTION: GREETINGS, TIME: time(), USER: {ACCOUNT_NAME: account_name}}


def handler_response_from_server(message):
    if RESPONSE in message:
        if message[RESPONSE] == 200:
            log.info('Клиент присоединился к серверу')
            return 'Код ответа:200 - "ОК"'
        log.error('Клиент не присоединился к серверу')
        try:
            return f'Код ответа:400 : {message[ERROR]}'
        except KeyError:
            log.error(
                'Некоректный ответ от сервера при попытке клиета подключиться')
    log.error('Некоректный ответ от сервера при попытке клиета подключиться')
    raise ValueError


def main():
    try:
        # получаем параметры из командной строки
        # print(sys.argv)
        server_ip_addr = sys.argv[2]
        server_port = int(sys.argv[3])
        if server_port < 1024 or server_port > 65535:
            raise ValueError
    except IndexError:

        # если параметры не переданы то устанавливаем значения по default
        server_ip_addr = DEFAULT_IP_ADDRESS
        server_port = DEFAULT_PORT
        params = {'ip': DEFAULT_IP_ADDRESS, 'port': DEFAULT_PORT}
        log.warning(
            "Параметры IP-адреса и порта не переданы и установлены по default: IP-%(ip)s , PORT-%(port)d",
            params)

    except ValueError:
        log.error(
            'В качестве порта может быть указано только число от 1024 до 65535.Process finished with exit code 1 ')
        # print('В качестве порта может быть указано только число в диапазоне от 1024 до 65535.')
        sys.exit(1)
    # создаем сетевой потоковый сокет
    sock_1 = socket(AF_INET, SOCK_STREAM)
    # устанавливаем соединение с сокетом
    # print(server_ip_addr, server_port)
    sock_1.connect((server_ip_addr, server_port))
    # создаем сообщение о присутствии клмента на сервере
    messages_to_server = create_greetings()
    # print(f'messages_to_server:{messages_to_server}')
    # кодируем данные в байты и отправляем на сервер
    send_mesages(sock_1, messages_to_server)
    try:
        # получаем данные
        message = get_messages(sock_1)
        # print(f'message:{message}')
        # печатаем код ответа
        response = handler_response_from_server(message)  # print(response)
    except (ValueError, JSONDecodeError):
        log.error(
            'Не удалось декодировать сообщение сервера.')  # print('Не удалось декодировать сообщение сервера.')


if __name__ == '__main__':
    main()
