"""
3. Задание на закрепление знаний по модулю yaml.
 Написать скрипт, автоматизирующий сохранение данных
 в файле YAML-формата.
Для этого:

Подготовить данные для записи в виде словаря, в котором
первому ключу соответствует список, второму — целое число,
третьему — вложенный словарь, где значение каждого ключа —
это целое число с юникод-символом, отсутствующим в кодировке
ASCII(например, €);

Реализовать сохранение данных в файл формата YAML — например,
в файл file.yaml. При этом обеспечить стилизацию файла с помощью
параметра default_flow_style, а также установить возможность работы
с юникодом: allow_unicode = True;

Реализовать считывание данных из созданного файла и проверить,
совпадают ли они с исходными.
"""
import yaml

data = {
    'items': ['computer', 'printer', 'keyboard', 'mouse'],
    'items_price': {
        'computer': '\u0032\u0030\u0030\u20ac\u002d\u0031\u0030\u0030\u0030\u20ac',
        'keyboard': '\u0035\u20ac\u002d\u0035\u0030\u20ac',
        'mouse': '\u0034\u20ac\u002d\u0037\u20ac',
        'printer': '\u0031\u0030\u0030\u20ac\u002d\u0033\u0030\u0030\u20ac'
    },
    'items_quantity': 4
}

with open('new.yaml', 'w', encoding='utf-8') as f:
    yaml.dump(data, f, default_flow_style=False, allow_unicode=True)
with open('new.yaml', encoding='utf-8') as f:
    new_yaml = f.read()
with open('file.yaml', encoding='utf-8') as f:
    file_yaml = f.read()
# проверка на совпадение данных из исходного файла с данными из файла созданного по условиям задания
print(new_yaml == file_yaml)
