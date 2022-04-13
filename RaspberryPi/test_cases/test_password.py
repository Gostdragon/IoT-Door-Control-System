import sys

sys.path.append('/home/pi/src-Building-Security-System')
import unittest

from RaspberryPi.src.data_model.password import Password
from RaspberryPi.src.exceptions.exception import SyntaxException

"""
Dieses Modul testet die Funktionalität der Klasse :class:`~password.Password` 
mithilfe von Unittests.

Classes:
    TestPassword: Repräsentiert eine Testklasse, welche die Methoden der Klasse
                  :class:`~password.Password` testet.

@author Ahmad Eynawi
@version 03.03.2022
"""


class TestPassword(unittest.TestCase):

    def setUp(self) -> None:
        self.__password = Password("123abc")

    def test_init(self):
        self.assertIsInstance(self.__password, Password)

        with self.assertRaises(SyntaxException):
            Password("")

    def test_equals(self):
        self.assertTrue(self.__password.__eq__(Password("123abc")))
        self.assertFalse(self.__password.__eq__(Password("567abc")))
