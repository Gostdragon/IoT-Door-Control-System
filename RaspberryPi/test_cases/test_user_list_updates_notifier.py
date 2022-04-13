import sys

sys.path.append('/home/pi/src-Building-Security-System')
import os
import unittest
from RaspberryPi.src.data_model.identifier import Identifier
from RaspberryPi.src.data_model.key_token import UnauthorizedNFCToken
from RaspberryPi.src.door_controller.door_control_handler.user_list_updates_notifier import UserListUpdatesNotifier
from RaspberryPi.src.door_controller.door_control_handler.token_updater import TokenUpdater
from RaspberryPi.src.data_model.door import DoorDataStorage
from RaspberryPi.src.door_controller.server_adapter.server_adapter_from_python_filemanager import ServerAdapterFromPythonFilemanager


"""
Dieses Modul ist zum Testen des Moduls user_list_updates_notifier.
Classes:
    TestUserListUpdatesNotifier(unittest.TestCase): Diese Klasse implementiert Test Methoden für die Klasse UserListUpdatesNotifier
        
@author Lukas Wittenzellner
@version 1.0
"""


class TestUserListUpdatesNotifier(unittest.TestCase):
    """
    Diese Klasse testet die Methoden der Klasse TestUserListUpdatesNotifier.

    Methods:
        setUp: Bereitet einige nötige Variablen für die Testmethoden vor.
        test_init: Testet den Konstruktor der Klasse TokenUpdater.
        test_addObserver: Testet das Hinzufügen eines Observers zu dem Subjekt.
        test_deleteObserver: Testet das Löschen eines bereits hinzugefügten Observers.
        test_setState: Testet das Aktualisieren der Token Liste bei einer Änderung in der Datei.
    """

    def setUp(self) -> None:
        """
        Bereitet einige nötige Variablen für die Testmethoden vor.
        """
        self.notifier = UserListUpdatesNotifier()
        self.door_data_storage = DoorDataStorage()
        self.server_adapter = ServerAdapterFromPythonFilemanager()
        self.observer = TokenUpdater(self.door_data_storage, self.server_adapter)
        self.path = "/home/pi/src-Building-Security-System/src/ValidTokens.txt"
        self.temp_path = "/home/pi/src-Building-Security-System/src/temp_file.txt"

    def test_init(self):
        """
        Testet den Kontruktor der Klasse.
        """
        self.assertIsInstance(self.notifier, UserListUpdatesNotifier)

    def test_addObserver(self):
        """
        Testet das Hinzufügen eines Observers zu dem Subjekt.
        """""
        self.notifier.addObserver(self.observer)
        self.assertTrue(self.notifier.observers.__contains__(self.observer))

    def test_deleteObserver(self):
        """
        Testet das Löschen eines bereits hinzugefügten Observers.
        """
        self.notifier.addObserver(self.observer)
        self.notifier.deleteObserver(self.observer)
        self.assertFalse(self.notifier.observers.__contains__(self.observer))

    def test_setState(self):
        """
        Testet das Aktualisieren der Token Liste bei einer Änderung in der Datei.
        """
        # Erstellt ein Backup der Datei der Tokenliste und fügt der temporären Datei einen Nutzer hinzu
        with open(self.temp_path, "w") as temp_file, open(self.path, "r+") as file:
            for line in file:
                temp_file.write(line)
            file.truncate(0)
            file.write("admin,admin;admin;admin:test_admin_token")

        test_token = UnauthorizedNFCToken(Identifier("test_admin_token"))
        self.notifier.setState()
        self.assertTrue(self.door_data_storage.doorTokens.__contains__(test_token))

        # Läd das gespeicherte Backup wieder in die Datei
        with open(self.path, "w") as file, open(self.temp_path, "r") as temp_file:
            for line in temp_file:
                file.write(line)
        os.remove(self.temp_path)


