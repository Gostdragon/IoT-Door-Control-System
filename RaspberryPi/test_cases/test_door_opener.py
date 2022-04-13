import sys

sys.path.append('/home/pi/src-Building-Security-System')
import unittest
from RaspberryPi.src.door_controller.door_control_handler.door_opener import DoorOpener

"""
Dieses Modul ist zum Testen des Moduls door_opener.
Classes:
    TestDoorOpener(unittest.TestCase): Diese Klasse implementiert Test Methoden für die Klasse DoorOpener
        
@author Lukas Wittenzellner
@version 1.0
"""


class TestDoorOpener(unittest.TestCase):
    """
    Diese Klasse testet die Methoden der Klasse DoorOpener.

    Methods:
        setUp: Bereitet einige nötige Variablen für die Testmethoden vor.
        test_init: Testet den Konstruktor der Klasse DoorOpener.
        test_openDoor: Testet das Öffnen der Tür.
    """

    def setUp(self) -> None:
        self.door_opener = DoorOpener()

    def test_init(self):
        """
        Testet den Kontruktor der Klasse.
        """
        self.assertIsInstance(self.door_opener, DoorOpener)

    def test_openDoor(self):
        """
        Testet das Öffnen der Tür.
        """
        self.assertTrue(self.door_opener.openDoor())


