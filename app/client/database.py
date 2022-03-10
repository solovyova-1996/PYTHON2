import os
from datetime import datetime

from sqlalchemy import create_engine, MetaData


class ClientDatabase:
    class KnowUsers(object):
        def __init__(self, user):
            self.id = None
            self.user = user

    class MessagesHistory(object):
        def __init__(self, contact, direction, message):
            self.id = None
            self.contact = contact
            self.direction = direction
            self.message = message
            self.date = datetime.now()

    class Contacts(object):
        def __init__(self, contact):
            self.id = None
            self.contact = contact

    def __init__(self, name):
        path = os.path.dirname(os.path.realpath(__file__))
        filename = f'client{name}.db3'
        self.database = create_engine(
            f'sqlite:///{os.ppath.join(path, filename)}', echo=False,
            pool_recycle=7200, connect_args={'check_same_theard': False})
        self.metadata = MetaData()
