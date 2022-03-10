import logging

from PyQt5.QtWidgets import QMainWindow, qApp

from client.general_window_conf import Ui_MainClientWindow
from errors import ServerError
logger = logging.getLogger('client')

class ClientGeneralWindow(QMainWindow):
    def __init__(self,database,transport):
        super().__init__()
        # база данных
        self.database = database
        # сокет
        self.transport = transport
        self.ui = Ui_MainClientWindow()
        self.ui.setupUi(self)

        # кнопка выхода
        self.ui.menu_exit.triggered.connect(qApp.exit)

        # кнопка отправки сообщения
        self.ui.btn_send.clicked.connect(self.send_message)

        # добавление контакта
        self.ui.btn_add_contact.clicked.connect(self.add_contact_window)
        self.ui.menu_add_contact.triggered.connect(self.add_contact_window)

        # удаление контакта
        self.ui.btn_remove_contact.clicked.connect(self.delete_contact_window)
        self.ui.btn_remove_contact.triggered.connect(self.delete_contact_window)
    def add_contact_window(self):
        pass
    def delete_contact_window(self):
        pass
    def send_message(self):
        message_text = self.ui.text_message.toPlainText()
        self.ui.text_message.close()
        if not message_text:
            return
        try:
            self.transport.send_message(self.current_chat,message_text)
        except ServerError as err:
            self.messages.critical(self,'Ошибка', err.text)
        except OSError as err:
            if err.errno:
                self.messages.critical(self,'Ошибка', 'Потеряно соединение с сервером!')
                self.close()
            self.messages.critical(self, 'Ошибка', 'Таймаут соединения!')
        except (ConnectionResetError, ConnectionAbortedError):
            self.messages.critical(self,'Ошибка', 'Потеряно соединение с сервером!')
            self.close()
        else:
            self.database.save_message(self.current_chat,'out',message_text)
            logger.debug(f'Отправлено сообщение для {self.current_chat}: {message_text}')