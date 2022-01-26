import json
from .variables import MAX_PACKAGE_SIZE, ENCODING


def get_messages(client):
    # получение данных размером 1024
    encoded_response = client.recv(MAX_PACKAGE_SIZE)

    # проверяем какой тип данных получен
    if isinstance(encoded_response, bytes):
        # если байты - декодируем в utf-8
        # print(chardet.detect(encoded_response))
        decode_response = encoded_response.decode(ENCODING)
        # print(decode_response)
        # десериализуем даннные из json
        response = json.loads(decode_response)
        print(response)
        if isinstance(response, dict):
            return response
        raise ValueError
    raise ValueError


def send_mesages(sock, messages):
    # сериализуем данные переданные в сообщении в json
    json_messages = json.dumps(messages)
    # кодируем данные в байты
    encoded_messages = json_messages.encode(ENCODING)
    # передача данных
    sock.send(encoded_messages)
