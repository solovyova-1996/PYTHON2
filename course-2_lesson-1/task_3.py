# 3.Написать функцию host_range_ping_tab(), возможности которой основаны на функции
# из примера 2.
# Но в данном случае результат должен быть итоговым по всем ip-адресам,
# представленным в табличном формате (использовать модуль tabulate).
# Таблица должна состоять из двух колонок и выглядеть примерно так:
from tabulate import tabulate

from task_1 import host_ping
from task_2 import host_range_ping
def host_range_ping_tab(res):
    print(tabulate(res, headers='keys', tablefmt="pretty"))

lst_network_node = ['192.168.0.101', '127.0.0.1', '1.1.1.1', 'google.ru']
ip_array = host_ping(lst_network_node)
res= host_range_ping(ip_array)
host_range_ping_tab(res)