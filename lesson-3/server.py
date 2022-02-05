import sys
import time
from logging import getLogger
from socket import socket, AF_INET, SOCK_STREAM
from argparse import ArgumentParser

from select import select

from general.utils import get_messages, send_mesages
from general.variables import ACTION, GREETINGS, TIME, USER, ACCOUNT_NAME, \
    RESPONSE, ERROR, PORT_ARGV, DEFAULT_PORT, IP_ARGV, MAX_CONNECTIONS, MESSAGE, \
    MESSAGE_TEXT, SENDER

from config import server_log_config
from decorators_log import log_func

log = getLogger('server')


@log_func
def handler_client_messages(messages, messages_list, client):
    # проверка есть ли в сообщении(словаре) ключи: 'action', 'time', 'user' и что находиться в этих полях
    if ACTION in messages and messages[
        ACTION] == GREETINGS and TIME in messages and USER in messages and \
            messages[USER][ACCOUNT_NAME] == 'Guest':
        log.info(
            'Клиент- %(account_name)s подключился к серверу(отправил корректный запрос)',
            messages[USER])
        send_mesages(client, {RESPONSE: 200})  # return {RESPONSE: 200}
    elif ACTION in messages and messages[
        ACTION] == MESSAGE and TIME in messages and MESSAGE_TEXT in messages:
        messages_list.append((messages[ACCOUNT_NAME], messages[MESSAGE_TEXT]))
    else:
        send_mesages(client, {RESPONSE: 400, ERROR: 'Bad Request'})
        log.error(
            'Клиент отправил некорректный запрос на подключение')  # return {RESPONSE: 400, ERROR: 'Bad Request'}


def argv_parser():
    # создаем парсер командной строки
    argv_pars = ArgumentParser()
    # создаем аргументы парсера - порт
    argv_pars.add_argument('-p', default=DEFAULT_PORT, type=int)
    # создаем аргумент парсера ip адресс
    argv_pars.add_argument('-a', default='')
    # передаем парсеру параметры командной строки
    IP_and_port = argv_pars.parse_args(sys.argv[1:])
    listen_port = IP_and_port.p
    listen_ip_addr = IP_and_port.a
    if not 1023 < listen_port < 65536:
        param = {'listen_port': listen_port}
        log.critical(
            'Номер порта не удовлетворяет условию -от 1024 до 65535.Переданный порт- %(listen_port)d.Process finished with exit code 1',
            param)
        sys.exit(1)
    return listen_ip_addr, listen_port


def main():
    # print(argv_parser())
    listen_ip_addr, listen_port = argv_parser()
    log.info(
        f'Запущен сервер, порт для подключения:{listen_port}, IP-адресс для подключения: {listen_ip_addr}')

    # создаем сокет AF_INET-сетевой, SOCK_STREAM - тип сокета потоковый
    sock_1 = socket(AF_INET, SOCK_STREAM)
    # привязываем сокет к ip адресу и порту машины
    sock_1.bind((listen_ip_addr, listen_port))
    sock_1.settimeout(0.5)
    clients_list = list()
    messages_list = list()
    # сигнализируем о готовности принимать соединение MAX_CONNECTIONS - количество одновременно обслуживаемых запросов
    sock_1.listen(MAX_CONNECTIONS)
    while True:
        # accept - принимает запрос на соединение
        try:
            client, client_ip_addr = sock_1.accept()
        except OSError:
            pass
        else:
            log.info(f'Установлено соединение с {client_ip_addr}')
            clients_list.append(client)
        # создаем переменные для принятия данных от select
        recv_lst = list()
        send_lst = list()
        err_lst = list()
        try:
            if clients_list:
                # recv_lst-список клиентов, отправивших сообщение,send_lst- список клиентов,ждущих сообщение
                recv_lst, send_lst, err_lst = select(clients_list, clients_list,
                                                     [], 0)
        except OSError:
            pass

        if recv_lst:
            for client_with_messages in recv_lst:
                try:
                    handler_client_messages(get_messages(client_with_messages),
                                            messages_list, client_with_messages)
                except:
                    # getpeername() - возвращает удаленный Ip-addr
                    log.info(f'Клиент {client_with_messages.getpeername()} '
                             f'отключился от сервера.')
                    clients_list.remove(client_with_messages)
        if messages_list and send_lst:
            message = {ACTION: MESSAGE, SENDER: messages_list[0][0],
                       TIME: time.time(), MESSAGE_TEXT: messages_list[0][1]}
            del messages_list[0]
            for expect_client in send_lst:
                try:
                    send_mesages(expect_client, message)
                except:
                    log.info(f'Клиент {expect_client.getpeername()} отключился')
                    clients_list.remove(expect_client)


if __name__ == '__main__':
    main()
