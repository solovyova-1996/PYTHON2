import os
from datetime import datetime

from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, \
    Text, DateTime
from sqlalchemy.orm import mapper, sessionmaker


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
        users = Table('know_users', self.metadata,
                      Column('id', Integer, primary_key=True),
                      Column('username', String))
        history = Table('messages_history', self.metadata,
                        Column('id', Integer, primary_key=True),
                        Column('contact', String), Column('direction', String),
                        Column('message', Text), Column('date', DateTime))
        contacts = Table('contacts', self.metadata,
                         Column('id', Integer, primary_key=True),
                         Column('name', String, unique=True))
        self.metadata.create_all(self.database)

        mapper(self.KnowUsers, users)
        mapper(self.MessagesHistory, history)
        mapper(self.Contacts, contacts)

        Session = sessionmaker(bind=self.database)
        self.session = Session()

        self.session.query(self.Contacts).delete()
        self.session.commit()

    def add_contact(self, contact):
        if not self.session.query(self.Contacts).filter_by(
                name=contact).count():
            new_contact = self.Contacts(contact)
            self.session.add(new_contact)
            self.session.commit()

    def del_contact(self, contact):
        self.session.query(self.Contacts).filter_by(name=contact).delete()

    def add_users(self, users_list):
        self.session.query(self.KnowUsers).delete()
        for user in users_list:
            new_user = self.KnowUsers(user)
            self.session.add(new_user)
        self.session.commit()

    def save_message(self, contact, direction, message):
        new_message = self.MessagesHistory(contact, direction, message)
        self.session.add(new_message)
        self.session.commit()

    def get_contacts(self):
        return [contact[0] for contact in
                self.session.query(self.Contacts.name).all()]

    def get_users(self):
        return [user[0] for user in
                self.session.query(self.KnowUsers.username).all()]

    def check_user(self, user):
        if self.session.query(self.KnowUsers).filter_by(username=user).count():
            return True
        else:
            return False

    def check_contact(self, contact):
        if self.session.query(self.Contacts).filter_by(name=contact).count():
            return True
        else:
            return False

    def get_history(self, contact):
        query = self.session.query(self.MessagesHistory).filter_by(
            contact=contact)
        return [(
                history_row.contact, history_row.direction, history_row.message,
                history_row.date) for history_row in query.all()]
