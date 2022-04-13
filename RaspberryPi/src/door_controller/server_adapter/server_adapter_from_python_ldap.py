"""
Dieses Modul deint als Schnittstelle zwischen Python Code und einem LDAP-Server.
Classes:
    ServerAdapterFromPythonLDAP: Ist eine Adapter-Klasse als Schnittstelle zu einem LDAP-Server.
@author Lukas Wittenzellner
@version 1.0
"""

import sys
sys.path.append('/home/pi/src-Building-Security-System')

from RaspberryPi.src.data_model.key_token import Token
from ldap3 import Server, Connection, ALL
from RaspberryPi.src.door_controller.server_adapter import server_adapter
from RaspberryPi.src.exceptions.exception import NotImplementedException
from RaspberryPi.src.data_model.user import UnauthenticatedUser


USER_DN = "dc=example,dc=com"  # Ist der Suchzweig im LDAP
SERVER_TOKEN_FILTER = "mail=*"  # Ist der Filter für das Finden von Tokens
SERVER_IP_ADRESS = "ldap.forumsys.com"  # Ist die IP-Adresse bzw. der hostname des LDAP-Servers

ADMIN_NAME = ''  # Ist der Login-Name des Nutzers, über den die Verbindung zum Server aufgebaut werden soll
ADMIN_PASSWORD = ''  # Ist des Login-Passwort des Nutzers, über den die Verbindung zum Server aufgebaut werden soll

SERVER = Server(SERVER_IP_ADRESS, get_info=ALL)
CONNECTION = Connection(SERVER, user=ADMIN_NAME, password=ADMIN_PASSWORD, auto_bind=True)


class ServerAdapterFromPythonLDAP(server_adapter):

    def add_token_to_user(self, user: UnauthenticatedUser, token: Token):
        raise NotImplementedException("LDAP-Methoden werden aktuell noch nicht unterstützt!")

    def delete_token_from_user(self, admin: UnauthenticatedUser, user: UnauthenticatedUser, token: Token):
        raise NotImplementedException("LDAP-Methoden werden aktuell noch nicht unterstützt!")

    def delete_all_tokens_from_user(self, admin: UnauthenticatedUser, user: UnauthenticatedUser):
        raise NotImplementedException("LDAP-Methoden werden aktuell noch nicht unterstützt!")

    def get_user(self, admin: UnauthenticatedUser, user: UnauthenticatedUser):
        raise NotImplementedException("LDAP-Methoden werden aktuell noch nicht unterstützt!")

    def get_all_valid_tokens(self, admin: UnauthenticatedUser):
        raise NotImplementedException("LDAP-Methoden werden aktuell noch nicht unterstützt!")

