import unittest

from RaspberryPi.src.door_controller.entities.doorbell import Doorbell
from RaspberryPi.src.exceptions.exception import SemanticsException, FileFormatException

"""
Dieses Modul testet die Funktionalität der Klasse :class:`~doorbell.Doorbell`
mithilfe von Unittests.

Classes:
    TestDoorbell: Repräsentiert eine Testklasse, welche die Methoden der Klasse
                  :class:`~doorbell.Doorbell` testet.

@author Ahmad Eynawi
@version 03.03.2022
"""


class TestDoorbell(unittest.TestCase):

    def setUp(self) -> None:
        self.__path = "C:/Users/ahmad/Desktop/bell_sms_wav.wav"
        self.__doorbell = Doorbell(self.__path, 1)

    def test_init(self):
        self.assertIsInstance(self.__doorbell, Doorbell)

        with self.assertRaises(FileNotFoundError):
            Doorbell("C:/Users/ahmad/Desktop/ringtone.wav")
            Doorbell("C:/Users/ahmad/Desktop/Verschiedenes")

        with self.assertRaises(FileFormatException):
            Doorbell("C:/Users/ahmad/Desktop/test.txt")

        with self.assertRaises(SemanticsException):
            Doorbell(self.__path, speakerVolume=2.5)
            Doorbell(self.__path, speakerVolume=-1)

    def test_setRingtonePath(self):
        with self.assertRaises(FileNotFoundError):
            self.__doorbell.ringtonePath = "C:/Users/ahmad/Desktop/ringtone.wav"
            self.__doorbell.ringtonePath = "C:/Users/ahmad/Desktop/Verschiedenes"

        with self.assertRaises(FileFormatException):
            self.__doorbell.ringtonePath = "C:/Users/ahmad/Desktop/test.txt"

    def test_setSpeakerVolume(self):
        with self.assertRaises(SemanticsException):
            self.__doorbell.speakerVolume = 2
            self.__doorbell.speakerVolume = -0.5


if __name__ == '__main__':
    unittest.main()
