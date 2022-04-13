import sys

import slack.errors

sys.path.append('/home/pi/src-Building-Security-System')
import unittest
from RaspberryPi.src.data_model.configuration import BotConfiguration
from RaspberryPi.src.door_controller.entities.bot import SlackBot
from RaspberryPi.src.data_model.key_token import BotIDToken, BotChannelToken
from RaspberryPi.src.data_model.identifier import Identifier
from RaspberryPi.src.door_controller.entities.log import LogError, LogInfo, LogFatal

"""
Dieses Modul testet die Funktionalität der Klasse :class:`~bot.SlackBot` 
mithilfe von Unittests.
Classes:
    TestBot: Repräsentiert eine Testklasse, welche die Methoden der Klasse
                         :class:`~bot.SlackBot` testet.
                         
@author Fabian Schiekel
@version 10.03.2022
"""


class TestBot(unittest.TestCase):
    idx = 0
    conf = BotConfiguration()
    invalid_slack_Token = BotIDToken(Identifier("invalid"))
    invalid_slack_channel_id = BotChannelToken(Identifier("invalid"))

    def setUp(self) -> None:
        self.bot = SlackBot(self.conf.bot_token[self.idx], self.conf.bot_channel_id[self.idx])
        with self.assertRaises(slack.errors.SlackApiError):
            SlackBot(self.conf.bot_token[self.idx], self.invalid_slack_channel_id)
            SlackBot(self.invalid_slack_Token, self.conf.bot_channel_id[self.idx])

    def test_init(self):
        self.assertIsInstance(self.bot, SlackBot)

    def test_send_and_delete_message(self):
        self.assertGreater(self.bot.send_and_delete_message(self.bot.send_message(self.conf.bot_msg[self.idx])), 0)


class TestLog(unittest.TestCase):

    def setUp(self) -> None:
        self.bot_log_token = BotIDToken(Identifier('xoxb-2921712558230-3063932997847-NnaaxKukW0DqxUq7KSP7QcEm'))
        self.bot_log_channel_id_fatal = BotChannelToken(Identifier("C0327JZ0P6H"))
        self.bot_log_channel_id_error = BotChannelToken(Identifier("C031G7K946S"))
        self.bot_log_channel_id_info = BotChannelToken(Identifier("C032CKMJL56"))
        self.bot_inf = LogInfo().get_instance()
        self.assertIsInstance(self.bot_inf, LogInfo)
        self.bot_err = LogError().get_instance()
        self.assertIsInstance(self.bot_err, LogError)
        self.bot_fat = LogFatal().get_instance()
        self.assertIsInstance(self.bot_fat, LogFatal)

    def test_send_log_msg(self):
        self.assertTrue(self.bot_inf.send_log_msg("log test"))
        self.assertTrue(self.bot_err.send_log_msg("log test"))
        self.assertTrue(self.bot_fat.send_log_msg("log test"))
