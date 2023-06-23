from database.controller import ClientMessages
from database.models import CBase

import typing

from json import dumps, loads
from config import ENCODING


class DbInterfaceMixin:
    def __init__(self, db_path):
        self._cm = ClientMessages(db_path, CBase, echo=False)

    def add_client(self, username, info=None):
        return self._cm.add_client(username, info)

    def get_client_by_username(self, username):
        return self._cm.get_client_by_username(username)

    def add_client_history(self, client_username, ip_addr='8.8.8.8'):
        return self._cm.add_client_history(client_username, ip_addr)

    def set_user_online(self, client_username):
        return self._cm.set_user_online(client_username)

    def add_contact(self, client_username, contact_username):
        return self._cm.add_contact(client_username, contact_username)

    def del_contact(self, client_username, contact_username):
        return self._cm.del_contact(client_username, contact_username)

    def get_contacts(self, client_username):
        return self._cm.get_contacts(client_username)

    def get_all_clients(self):
        return self._cm.get_all_clients()

    def get_client_history(self, client_username):
        return self._cm.get_client_history(client_username)

    def get_client_messages(self, client_username):
        return self._cm.get_client_messages(client_username)

    def set_user_offline(self, client_username):
        return self._cm.set_user_offline(client_username)

    def get_user_status(self, client_username):
        return self._cm.get_user_status(client_username)


class ConvertMixin:

    def _dict_to_bytes(self, msg_dict: typing.Dict) -> typing.ByteString:
        """
        Преобразование словаря в байты
        :param msg_dict: словарь
        :return: bytes
        """
        if isinstance(msg_dict, typing.Dict):
            jmessage = dumps(msg_dict)
            bmessage = jmessage.encode(ENCODING)
            return bmessage
        else:
            raise TypeError

    def _bytes_to_dict(self, msg_bytes: typing.ByteString) -> typing.Dict:
        """
        Получение словаря из байтов
        :param msg_bytes: сообщение в виде байтов
        :return: словарь сообщения
        """
        if isinstance(msg_bytes, typing.ByteString):

            jmessage = msg_bytes.decode(ENCODING)
            message = loads(jmessage)

            if isinstance(message, typing.Dict):
                return message
            else:
                raise TypeError
        else:
            raise TypeError
