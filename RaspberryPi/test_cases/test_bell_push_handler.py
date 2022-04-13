import sys

sys.path.append('/home/pi/src-Building-Security-System')
import unittest
from RaspberryPi.src.door_controller.bell_push_handler import BotNotifier
from RaspberryPi.src.door_controller.bell_push_handler import CameraNotifier
from RaspberryPi.src.door_controller.entities.bot import SlackBot
from RaspberryPi.src.data_model.key_token import BotIDToken, BotChannelToken
from RaspberryPi.src.data_model.identifier import Identifier
from RaspberryPi.src.door_controller.entities.camera import TapoCamera
from RaspberryPi.src.door_controller.bell_push_handler import BellPushEventHandler

"""
Dieses Modul testet die Funktionalität der Klasse :class:`~bell_push_handler.BotNotifier`, 
:class:`~bell_push_handler.BellPushHandler` und :class:`~bell_push_handler.CameraNotifier` mithilfe von Unittests.

Classes:
    TestBotNotifier: Repräsentiert eine Testklasse, welche die Methoden der Klasse
                         :class:`~bell_push_handler.BotNotifier` testet.
    TestCameraNotifier: Repräsentiert eine Testklasse, welche die Methoden der Klasse
                         :class:`~bell_push_handler.CameraNotifier` testet.
    TestBellPushHandler: Repräsentiert eine Testklasse, welche die Methoden der Klasse
                         :class:`~bell_push_handler.BellPushHandler` testet.
                         
@author Fabian Schiekel
@version 10.03.2022
"""


class TestBotNotifierKonstruktor(unittest.TestCase):
    valid_slack_Token = BotIDToken(Identifier('xoxb-2921712558230-3057072859875-uBvcWy1IrpK6iPn6Qm7uMrrK'))
    valid_slack_channel_id = BotChannelToken(Identifier('C02T8HVHUB1'))
    valid_message = 'Message'

    def setUp(self) -> None:
        bot = SlackBot(self.valid_slack_Token, self.valid_slack_channel_id)
        self.bot_notifier = BotNotifier(bot, self.valid_message)

    def test_init(self):
        self.assertIsInstance(self.bot_notifier, BotNotifier)

    def test_update(self):
        ret = self.bot_notifier.update()
        self.assertEqual(ret, 1)


class TestCameraNotifier(unittest.TestCase):

    def setUp(self) -> None:
        cam = TapoCamera(0)
        self.camera_notifier = CameraNotifier(cam)

    def test_init(self) -> None:
        self.assertIsInstance(self.camera_notifier, CameraNotifier)

    def test_update(self):
        self.assertGreater(self.camera_notifier.update(), 0)


class TestBellPushHandler(unittest.TestCase):
    valid_slack_Token = BotIDToken(Identifier('xoxb-2921712558230-3057072859875-uBvcWy1IrpK6iPn6Qm7uMrrK'))
    valid_slack_channel_id = BotChannelToken(Identifier('C02T8HVHUB1'))
    valid_message = 'Message'

    def setUp(self) -> None:
        bot = SlackBot(self.valid_slack_Token, self.valid_slack_channel_id)
        self.bot_notifier = BotNotifier(bot, self.valid_message)
        cam = TapoCamera(0)
        self.camera_notifier = CameraNotifier(cam)

        self.bell_push_handler = BellPushEventHandler()

        ret = self.bell_push_handler.addObserver(self.bot_notifier)
        self.assertGreater(ret, 0)
        ret = self.bell_push_handler.addObserver(self.camera_notifier)
        self.assertGreater(ret, 0)

    def test_notifyObserver(self):
        ret = self.bell_push_handler.notifyObservers()
        self.assertGreater(ret, 0)

    def test_deleteObserver(self):
        ret = self.bell_push_handler.deleteObserver(self.camera_notifier)
        self.assertGreater(ret, 0)

        ret = self.bell_push_handler.deleteObserver(self.bot_notifier)
        self.assertGreater(ret, 0)
