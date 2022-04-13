import sys

sys.path.append('/home/pi/src-Building-Security-System')
import unittest
from RaspberryPi.src.data_model.identifier import Identifier

"""
Dieses Modul testet die Funktionalität der Klasse :class:`~identifier.Identifier` 
mithilfe von Unittests.

Classes:
    TestIdentifier: Repräsentiert eine Testklasse, welche die Methoden der Klasse
                    :class:`~identifier.Identifier` testet.

@author Ahmad Eynawi
@version 03.03.2022
"""


class TestIdentifier(unittest.TestCase):

    def setUp(self) -> None:
        self.__firstIdentifier = Identifier("12345")
        self.__secondIdentifier = Identifier("12345")

    def test_init(self):
        self.assertIsInstance(self.__firstIdentifier, Identifier)
        self.assertIsInstance(self.__secondIdentifier, Identifier)

    def test_equals(self):
        self.assertTrue(self.__firstIdentifier.__eq__(self.__secondIdentifier))
        self.assertEqual(self.__firstIdentifier, self.__secondIdentifier)

        self.__firstIdentifier = Identifier("67890")

        self.assertFalse(self.__firstIdentifier.__eq__(self.__secondIdentifier))
        self.assertNotEqual(self.__firstIdentifier, self.__secondIdentifier)


if __name__ == '__main__':
    unittest.main()
