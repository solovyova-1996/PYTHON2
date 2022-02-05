# import subprocess
#
# process_list = list()
# while True:
#     command = input('Выберите действие: q - выход, '
#                     's - запустить сервер и клиенты, x - закрыть все окна: ')
#     if command == 'q':
#         break
#     elif command == 's':
#         process = subprocess.Popen('python server.py',
#                                    creationflags=subprocess.CREATE_NEW_CONSOLE)
#         process_list.append(process)
#         for i in range(2):
#             process_list.append(subprocess.Popen('python client.py -m send',
#                                                  creationflags=subprocess.CREATE_NEW_CONSOLE))
#         for i in range(5):
#             process_list.append(subprocess.Popen('python client.py -m listen',
#                                                  creationflags=subprocess.CREATE_NEW_CONSOLE))
#     elif command == 'x':
#         while process_list:
#             process_kill = process_list.pop()
#             process_kill.kill()

import subprocess

PROCESS = []

while True:
    ACTION = input('Выберите действие: q - выход, '
                   's - запустить сервер и клиенты, x - закрыть все окна: ')

    if ACTION == 'q':
        break
    elif ACTION == 's':
        PROCESS.append(subprocess.Popen('python server.py',
                                        creationflags=subprocess.CREATE_NEW_CONSOLE))
        for i in range(2):
            PROCESS.append(subprocess.Popen('python client.py -m send',
                                            creationflags=subprocess.CREATE_NEW_CONSOLE))
        for i in range(3):
            PROCESS.append(subprocess.Popen('python client.py -m listen',
                                            creationflags=subprocess.CREATE_NEW_CONSOLE))
    elif ACTION == 'x':
        while PROCESS:
            VICTIM = PROCESS.pop()
            VICTIM.kill()
