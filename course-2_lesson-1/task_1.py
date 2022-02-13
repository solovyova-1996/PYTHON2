# 1.Написать функцию host_ping(), в которой с помощью утилиты ping будет
# проверяться доступность сетевых узлов. Аргументом функции является список,
# в котором каждый сетевой узел должен быть представлен именем хоста или ip-адресом.
# В функции необходимо перебирать ip-адреса и проверять их доступность с выводом
# соответствующего сообщения («Узел доступен», «Узел недоступен»).
# При этом ip-адрес сетевого узла должен создаваться с помощью функции ip_address().

from ipaddress import ip_address
from pprint import pprint
from socket import gethostbyname
from subprocess import Popen, PIPE


def host_ping(lst_network_node):
    # Словарь для записи результатов (доступные узлы/ недоступные узлы)
    result = {'available_nodes': [], 'not_available_nodes': []}
    for network_node in lst_network_node:
        try:
            # создаем  IPv4-адреса
            network_node_ip = ip_address(network_node)
        except ValueError:
            # если сетевой адрес представлен в виде домена, то возникает исключение
            # преобразуем домен в ip
            network_node_ip = gethostbyname(network_node)
            # создаем  IPv4-адреса
            network_node_ip = ip_address(network_node_ip)
        # пингуем IP -адрес
        process = Popen(f'ping {network_node_ip} -w 500 -n 1', stdout=PIPE,
                        encoding='utf-8')
        process.wait()
        if process.returncode == 0:
            # print(f'{network_node_ip} - доступен')
            # если адрес доступен, добавляем его в список словаря результатов по ключу 'available_nodes'
            result['available_nodes'].append(network_node_ip)
        else:
            # print(f'{network_node_ip} - не доступен')
            # если адрес не доступен, добавляем его в список словаря результатов по ключу 'not_available_nodes'
            result['not_available_nodes'].append(network_node_ip)
    return result


if __name__ == '__main__':
    lst_network_node = ['192.168.0.101', '127.0.0.1', '1.1.1.1', 'google.ru']
    res = host_ping(lst_network_node)
    pprint(res)
