import sys

sys.path.append('/home/pi/src-Building-Security-System')
import os
import unittest
from RaspberryPi.src.data_model.key_token import UnauthorizedNFCToken
from RaspberryPi.src.data_model.name import Name, FirstName, LastName
from RaspberryPi.src.data_model.password import Password
from RaspberryPi.src.data_model.user import AuthenticatedUser
from RaspberryPi.src.door_controller.door_control_handler.oberver import Observer
from RaspberryPi.src.door_controller.door_control_handler.token_updater import TokenUpdater
from RaspberryPi.src.door_controller.server_adapter.server_adapter_from_python_filemanager import ServerAdapterFromPythonFilemanager
import RaspberryPi.src.door_controller.server_adapter.server_adapter_from_python_filemanager
from RaspberryPi.src.data_model.door import DoorDataStorage
from RaspberryPi.src.data_model.identifier import Identifier
from RaspberryPi.src.data_model.configuration import PiConfiguration

"""
Dieses Modul ist zum Testen des Moduls token_updater
Classes:
    TestTokenUpdater(unittest.TestCase): Diese Klasse implementiert Test Methoden für die Klasse TokenUpdater
        
@author Lukas Wittenzellner
@version 1.0
"""


class TestTokenUpdater(unittest.TestCase):
    """
    Diese Klasse testet die Methoden der Klasse TokenUpdater.

    Methods:
        setUp: Bereitet einige nötige Variablen für die Testmethoden vor.
        test_init: Testet den Konstruktor der Klasse TokenUpdater.
        test_getValidTokens: Testet das Bekommen der Liste aller gültigen Token.
    """

    def setUp(self) -> None:
        """
        Bereitet einige nötige Variablen für die Testmethoden vor.
        """
        self.path = "/home/pi/src-Building-Security-System/src/ValidTokens.txt"
        self.temp_path = "/home/pi/src-Building-Security-System/src/temp_file.txt"
        self.serverAdapter = ServerAdapterFromPythonFilemanager()
        self.doorDataStorage = DoorDataStorage()
        self.token_updater = TokenUpdater(self.doorDataStorage, self.serverAdapter)
        self.admin = AuthenticatedUser(Name(FirstName("admin"), LastName("admin")),
                                       Identifier("admin"), Password("admin"))
        self.config = PiConfiguration(1, 2, 3, 4, 2, self.admin)

    def test_init(self):
        """
        Testet den Konstruktor der Klasse TokenUpdater.
        """
        self.assertIsInstance(self.token_updater, TokenUpdater)

    def test_getValidTokens(self):
        """
        Testet das Bekommen der Liste aller gültigen Token.
        """
        # Erstellt ein Backup der Datei der Tokenliste und fügt der temporären Datei einen Nutzer hinzu
        with open(self.temp_path, "w") as temp_file, open(self.path, "r+") as file:
            for line in file:
                temp_file.write(line)
            file.truncate(0)
            file.write("admin,admin;admin;admin:test_admin_token")

        test_token = UnauthorizedNFCToken(Identifier("test_admin_token"))
        token_list = self.token_updater.getValidTokens()

        self.assertEqual(token_list[0], test_token)
        self.assertTrue(token_list.__contains__(test_token))

        # Läd das gespeicherte Backup wieder in die Datei
        with open(self.path, "w") as file, open(self.temp_path, "r") as temp_file:
            for line in temp_file:
                file.write(line)
        os.remove(self.temp_path)
