import sys

sys.path.append('/home/pi/src-Building-Security-System')
import unittest

from RaspberryPi.src.data_model.name import Name, FirstName, LastName
from RaspberryPi.src.exceptions.exception import SyntaxException

"""
Dieses Modul testet die Funktionalität der Klassen :class:`~name.Name`, :class:`~name.FirstName`,
und :class:`~name.LastName` mithilfe von Unittests.

Classes:
    TestName: Repräsentiert eine Testklasse, welche die Methoden der Klassen
              :class:`~name.Name`, :class:`~name.FirstName` und :class:`~name.LastName` testet.

@author Ahmad Eynawi
@version 03.03.2022
"""


class TestName(unittest.TestCase):

    def setUp(self) -> None:
        self.__firstName = FirstName("Albert")
        self.__lastName = LastName("Einstein")
        self.__fullName = Name(self.__firstName, self.__lastName)

    def test_init(self):
        self.assertIsInstance(self.__firstName, FirstName)
        self.assertIsInstance(self.__lastName, LastName)
        self.assertIsInstance(self.__fullName, Name)

        with self.assertRaises(SyntaxException):
            FirstName("12abc")
            LastName("34cdf")
            FirstName("")
            LastName("")
            Name(FirstName("a#bc"), LastName("34def"))
            Name(FirstName("abc"), LastName("34def"))
            Name(FirstName("12abc"), LastName("def"))
            Name(FirstName(""), LastName("34def"))
            Name(FirstName("12abc"), LastName(""))

    def test_equals(self):
        self.assertTrue(self.__firstName.__eq__(FirstName("Albert")))
        self.assertFalse(self.__firstName.__eq__(FirstName("Bassel")))

        self.assertTrue(self.__lastName.__eq__(LastName("Einstein")))
        self.assertFalse(self.__lastName.__eq__(LastName("Safadi")))

        self.assertTrue(self.__fullName.__eq__(Name(FirstName("Albert"), LastName("Einstein"))))
        self.assertFalse(self.__fullName.__eq__(Name(FirstName("Bassel"), LastName("Safadi"))))
