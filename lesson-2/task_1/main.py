"""
1. Задание на закрепление знаний по модулю CSV. Написать скрипт,
осуществляющий выборку определенных данных из файлов info_1.txt, info_2.txt,
info_3.txt и формирующий новый «отчетный» файл в формате CSV.

Для этого:

Создать функцию get_data(), в которой в цикле осуществляется перебор файлов
с данными, их открытие и считывание данных. В этой функции из считанных данных
необходимо с помощью регулярных выражений или другого инструмента извлечь значения параметров
«Изготовитель системы», «Название ОС», «Код продукта», «Тип системы».
Значения каждого параметра поместить в соответствующий список. Должно
получиться четыре списка — например, os_prod_list, os_name_list,
os_code_list, os_type_list. В этой же функции создать главный список
для хранения данных отчета — например, main_data — и поместить в него
названия столбцов отчета в виде списка: «Изготовитель системы»,
«Название ОС», «Код продукта», «Тип системы». Значения для этих
столбцов также оформить в виде списка и поместить в файл main_data
(также для каждого файла);

Создать функцию write_to_csv(), в которую передавать ссылку на CSV-файл.
В этой функции реализовать получение данных через вызов функции get_data(),
а также сохранение подготовленных данных в соответствующий CSV-файл;

Пример того, что должно получиться:

Изготовитель системы,Название ОС,Код продукта,Тип системы

1,LENOVO,Windows 7,00971-OEM-1982661-00231,x64-based

2,ACER,Windows 10,00971-OEM-1982661-00231,x64-based

3,DELL,Windows 8.1,00971-OEM-1982661-00231,x86-based

Обязательно проверьте, что у вас получается примерно то же самое.

ПРОШУ ВАС НЕ УДАЛЯТЬ СЛУЖЕБНЫЕ ФАЙЛЫ TXT И ИТОГОВЫЙ ФАЙЛ CSV!!!
"""
import csv
import re


def get_data():
    param_1 = 'Изготовитель системы:'
    param_2 = 'Название ОС:'
    param_3 = 'Код продукта:'
    param_4 = 'Тип системы:'
    os_prod_list = list()
    os_name_list = list()
    os_code_list = list()
    os_type_list = list()
    main_data = ['Изготовитель системы', 'Название ОС', 'Код продукта',
                 'Тип системы']

    result = list()
    result.append(main_data)

    for file in ['info_1.txt', 'info_2.txt', 'info_3.txt']:
        with open(file, 'r', encoding='utf-8') as f:
            for i in f:
                if param_1 in i:
                    new_i = i.replace(param_1, '').strip()
                    os_prod_list.append(new_i)
                elif param_2 in i:
                    new_i = i.replace(param_2, '').strip()
                    new_i_reg = re.search('Windows\s\d\.*\d*', new_i)
                    os_name_list.append(new_i_reg[0])
                elif param_3 in i:
                    new_i = i.replace(param_3, '').strip()
                    os_code_list.append(new_i)
                elif param_4 in i:
                    new_i = i.replace(param_4, '').strip()
                    new_i_reg = re.search('[^A-Z]*', new_i)
                    os_type_list.append(new_i_reg[0])

    res = list(zip(os_prod_list, os_name_list, os_code_list, os_type_list))
    new_res = list(map(list, res))
    for i, lst in enumerate(new_res, start=1):
        lst.insert(0, i)
    result.extend(new_res)
    return result


def write_to_csv(file):
    data = get_data()
    with open(file, 'w+', encoding='utf-8') as f:
        f_writer = csv.writer(f)
        f_writer.writerows(data)

write_to_csv('new_data.csv')
