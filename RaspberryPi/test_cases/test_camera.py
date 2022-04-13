import sys

sys.path.append('/home/pi/src-Building-Security-System')
import unittest

from RaspberryPi.src.door_controller.entities.camera import TapoCamera

"""
Dieses Modul testet die Funktionalität der Klasse :class:`~camera.TapoCamera` 
mithilfe von Unittests.
Classes:
    TestCamera: Repräsentiert eine Testklasse, welche die Methoden der Klasse
                         :class:`~camera.TapoCamera`  testet.

@author Fabian Schiekel
@version 10.03.2022
"""


class TestCamera(unittest.TestCase):
    def setUp(self) -> None:
        self.camera = TapoCamera(0)

    def test_event(self):
        self.assertIsInstance(self.camera, TapoCamera)

        self.assertGreater(self.camera.ringEvent(), 0)
