import json
import sys
from argparse import ArgumentParser
from json import JSONDecodeError
from logging import getLogger
from socket import socket, AF_INET, SOCK_STREAM
from time import time

from errors import ServerError, ReqFieldMissingError
from general.utils import send_mesages, get_messages
from decorators_log import log_func, LogClass
from general.variables import ACTION, GREETINGS, TIME, USER, ACCOUNT_NAME, \
    RESPONSE, ERROR, DEFAULT_IP_ADDRESS, DEFAULT_PORT, MESSAGE_TEXT, MESSAGE, \
    SENDER

from config import client_log_config

log = getLogger('client')


@log_func
def handler_message_from_users(message):
    if ACTION in message and message[
        ACTION] == MESSAGE and SENDER in message and MESSAGE_TEXT in message:
        print(
            f'Получено сообщение от пользователя {message[SENDER]}:\n{message[MESSAGE_TEXT]}')
        log.info(
            f'Получено сообщение от пользователя {message[SENDER]}:\n{message[MESSAGE_TEXT]}')
    else:
        log.error(f'От сервера получено некорректное сообщение : {message}')


@log_func
def create_message(sock, account_name='Guest'):
    message = input('Введите сообщение, для завершения работы введите - stop: ')
    if message == 'stop':
        sock.close()
        log.info('Пользователь завершил работу')
        sys.exit(0)
    message_create = {ACTION: MESSAGE, TIME: time(), ACCOUNT_NAME: account_name,
                      MESSAGE_TEXT: message}
    log.debug(f'Создано сообщение {message_create}')
    return message_create


@log_func
def create_greetings(account_name='Guest'):
    # генерация запроса о присутствии клиента
    return {ACTION: GREETINGS, TIME: time(), USER: {ACCOUNT_NAME: account_name}}


@LogClass()
def handler_response_from_server(message):
    # print(message)
    log.debug(f'Разбор приветственного сообщения от сервера: {message}')
    if RESPONSE in message:
        if message[RESPONSE] == 200:
            return '200 : OK'
        elif message[RESPONSE] == 400:
            raise ServerError(f'400 : {message[ERROR]}')
    raise ReqFieldMissingError(RESPONSE)


@log_func
def argv_parser():
    # создаем парсер командной строки
    argv_pars = ArgumentParser()
    # создаем аргументы парсера - порт
    argv_pars.add_argument('port', default=DEFAULT_PORT,
                           help='port on which to run', type=int, nargs='?')
    # создаем аргумент парсера ip адресс
    argv_pars.add_argument('addr', default=DEFAULT_IP_ADDRESS, nargs='?')
    # создаем аргумент парсера mode (listen or send)
    argv_pars.add_argument('-m', '--mode', default='listen', nargs='?')
    # передаем парсеру параметры командной строки
    IP_and_port_and_mode = argv_pars.parse_args(sys.argv[1:])
    server_port = IP_and_port_and_mode.port
    server_ip_addr = IP_and_port_and_mode.addr
    client_mode = IP_and_port_and_mode.mode

    if server_port < 1024 or server_port > 65535:
        param = {'server_port': server_port}
        log.critical(
            'Номер порта не удовлетворяет условию -от 1024 до 65535.Переданный порт- %(server_port)d.Process finished with exit code 1',
            param)
        sys.exit(1)
    if client_mode not in ('listen', 'send'):
        log.critical(
            f'В параметре mode указан несуществующий режим работы {client_mode}, список существующих режимов: "listen","send" ')

    return server_ip_addr, server_port, client_mode


def main():
    server_ip_addr, server_port, client_mode = argv_parser()
    log.info(
        f'Запущен клиент с ip-адресом{server_ip_addr}, порт:{server_port}, с режимом работы:{client_mode}')
    try:
        # создаем сетевой потоковый сокет
        sock_1 = socket(AF_INET, SOCK_STREAM)
        # устанавливаем соединение с сокетом
        # print(server_ip_addr, server_port)
        sock_1.connect((server_ip_addr, server_port))
        # создаем сообщение о присутствии клмента на сервере
        messages_to_server = create_greetings()

        # кодируем данные в байты и отправляем на сервер
        send_mesages(sock_1, messages_to_server)
        answer = handler_response_from_server(get_messages(sock_1))
        log.info(
            f'Установлено соединение с сервером. Ответ от сервера {answer}')
        print('Соединение с сервером установлено')
    except json.JSONDecodeError:
        log.error('Не удалось декодировать полученную Json строку.')
        sys.exit(1)
    except ServerError as error:
        log.error(
            f'При установке соединения сервер вернул ошибку: {error.text}')
        sys.exit(1)
    except ReqFieldMissingError as missing_error:
        log.error(
            f'В ответе сервера отсутствует необходимое поле {missing_error.missing_field}')
        sys.exit(1)
    except ConnectionRefusedError:
        log.critical(
            f'Не удалось подключиться к серверу {server_ip_addr}:{server_port}, '
            f'конечный компьютер отверг запрос на подключение.')
        sys.exit(1)
    else:
        # Если соединение с сервером установлено корректно,
        # начинаем обмен с ним, согласно требуемому режиму.
        # основной цикл прогрммы:
        if client_mode == 'send':
            print('Режим работы - отправка сообщений.')
        else:
            print('Режим работы - приём сообщений.')
        while True:
            # режим работы - отправка сообщений
            if client_mode == 'send':
                try:
                    send_mesages(sock_1, create_message(sock_1))
                except (
                ConnectionResetError, ConnectionError, ConnectionAbortedError):
                    log.error(
                        f'Соединение с сервером {server_ip_addr} было потеряно.')
                    sys.exit(1)

            # Режим работы приём:
            if client_mode == 'listen':
                try:
                    handler_message_from_users(get_messages(sock_1))
                except (
                ConnectionResetError, ConnectionError, ConnectionAbortedError):
                    log.error(
                        f'Соединение с сервером {server_ip_addr} было потеряно.')
                    sys.exit(1)


if __name__ == '__main__':
    main()
