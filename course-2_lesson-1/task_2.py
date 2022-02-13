# 2.Написать функцию host_range_ping() для перебора ip-адресов из заданного
# диапазона. Меняться должен только последний октет каждого адреса.
# По результатам проверки должно выводиться соответствующее сообщение.

from subprocess import Popen, PIPE

from task_1 import host_ping


# диапазон в 10 адресов
def host_range_ping(ip_array):
    # словарь для результатов
    result = {'available_nodes': [], 'not_available_nodes': []}
    not_available_nodes_lst = ip_array['not_available_nodes']
    ip_array_lst = ip_array['available_nodes']
    # добавляем в результирующий словарь доступные и недоступные адреса
    result['available_nodes'].extend(ip_array_lst)
    result['not_available_nodes'].extend(ip_array_lst)
    # словарь, полученный на вход превращаем в список
    ip_array_lst.extend(not_available_nodes_lst)
    for ip_addr in ip_array_lst:
        # получаем последний октет ip адреса для проверки, чтобы не получить число более 255
        last_oktet = int(str(ip_addr).split('.')[-1])
        for i in range(1, 11):
            new_ip = ip_addr + i if last_oktet < 245 else ip_addr - i
            process = Popen(f'ping {new_ip} -w 500 -n 1', stdout=PIPE,
                            encoding='utf-8')
            process.wait()
            if process.returncode == 0:
                result['available_nodes'].append(new_ip)
            else:
                result['not_available_nodes'].append(new_ip)
    return result


if __name__ == '__main__':
    lst_network_node = ['192.168.0.101', '127.0.0.1', '1.1.1.1', 'google.ru']
    ip_array = host_ping(lst_network_node)
    res = host_range_ping(ip_array)
    print(res)
