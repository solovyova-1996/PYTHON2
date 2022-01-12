"""
Задание 5.

Выполнить пинг веб-ресурсов yandex.ru, youtube.com и
преобразовать результаты из байтовового в строковый тип на кириллице.

Подсказки:
--- используйте модуль chardet, иначе задание не засчитается!!!
"""
import subprocess
import chardet

args1 = ['ping', 'yandex.ru']
args2 = ['ping', 'youtube.com']
subprocess_ping_yandex = subprocess.Popen(args1, stdout=subprocess.PIPE)
for line in subprocess_ping_yandex.stdout:
    type_of_encoding = chardet.detect(line)
    line_bytes = line.decode(type_of_encoding['encoding'])
    print(line_bytes)

subprocess_ping_youtube = subprocess.Popen(args2, stdout=subprocess.PIPE)
for line in subprocess_ping_youtube.stdout:
    type_of_encoding = chardet.detect(line)
    line_bytes = line.decode(type_of_encoding['encoding'])
    print(line_bytes)
