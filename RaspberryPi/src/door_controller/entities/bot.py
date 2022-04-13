import urllib.error
from abc import ABC, abstractmethod
from slack import WebClient
import time
from slack.errors import SlackApiError
from RaspberryPi.src.data_model.configuration import BotConfiguration
from RaspberryPi.src.data_model.key_token import BotIDToken, BotChannelToken

"""
Die Klasse in diesem Modul repräsentiert ein Bot-Objekt für eine ferngesteuerte Tür.

Classes:
    Bot: Repräsentiert ein Bot-Objekt für die gesteuerte Beobachtung einer ferngesteuerten Tür. 
    SlackBot: Eine Unterklasse von Bot, repräsentiert einen Slack Bot. 

@author Fabian Schiekel
@version 05.03.2022
"""


class Bot(ABC):
    @abstractmethod
    def send_message(self, message: str) -> str:
        """
        Sendet die angegebene Nachricht an den Channel, von dem der Bot die ID hat.

        @param message: Die Nachricht, welche der Bot senden soll.
        @param message: str

        @return: -1 Wenn die Nachricht nicht gesendet werden konnte.
                 >0 Der Timestamp der Nachricht.
        """
        pass

    @abstractmethod
    def send_and_delete_message(self, message: str) -> int:
        """
        Der Bot sendet die übergebene Nachricht und löscht diese anschließend wieder.

        @param message: Die Nachricht, welche der Bot senden soll.
        @type message: str

        @return: 1 Wenn die Nachricht gesendet und wieder gelöscht werden konnte.
                -1 Wenn die Nachricht nicht gesendet und/oder gelöscht werden konnte.
        """
        pass

    @abstractmethod
    def delete_message(self, ts: str) -> bool:
        """
        Löscht die Nachricht mit dem angegebenen Timestamp aus dem Channel, von dem der Bot die ID hat.

        @param ts: Der Timestamp der Nachricht, welche gelöscht werden soll.
        @param ts: str

        @return: False Wenn die Nachricht nicht gelöscht werden konnte.
                 True  Wenn die Nachricht gelöscht werden konnte.
        """
        pass


class SlackBot(Bot):
    """
    Repräsentiert ein Bot-Objekt für die gesteuerte Beobachtung einer ferngesteuerten Tür.

    Methods:
        send_and_delete_message: Der Bot sendet die übergebene Nachricht und löscht diese nach einer definierten
            Zeitspanne.
        send_message: Sendet die angegebene Nachricht an den Channel, von dem der Bot die ID hat.
        delete_message: Löscht die Nachricht mit dem angegebenen Timestamp aus dem Channel, von dem der Bot die ID hat.
    """
    def __init__(self, bot_token: BotIDToken, channel_id: BotChannelToken):
        """
        Der Konstruktor der Klasse:class:`~Bot.Bot`.

        Erstellt und initialisiert ein Bot-Objekt. Das Objekt speichert die Token-ID des Bots, welcher dieses Objekt
        repräsentiert und die Kanal-ID des Kanal in welcher der Bot eine Nachricht senden soll.

        @param bot_token: Der Token, welcher zu dem Bot gehört, der die Nachricht senden soll.
        @param channel_id: Die ID zu dem Kanal, in welchem der Bot die Nachricht senden soll.

        @type bot_token: BotIDToken
        @type channel_id: BotChannelToken

        @raise: SyntaxException: Die Bot-ID und/oder die Kanal-ID ist nicht valide.
        @raise: urllib.error.URLError: Es konnte keine Verbindung zum Bot aufgebaut werden.

        """
        self.__slack_token = bot_token
        self.__channel_id = channel_id
        self.__client = WebClient(token=self.__slack_token.identifier.__repr__())
        self.__timestamp = '0'
        self.__client.auth_test()

    def send_and_delete_message(self, message: str) -> int:
        """
        Der Bot sendet die übergebene Nachricht und löscht diese anschließend wieder.

        @param message: Die Nachricht, welche der Bot senden soll.
        @type message: str

        @return: 1 Wenn die Nachricht gesendet und wieder gelöscht werden konnte.
                -1 Wenn die Nachricht nicht gesendet und/oder gelöscht werden konnte.
        @raise: urllib.error: Wenn keine Verbindung zu dem Bot besteht.
        """
        if message == "":
            return 1
        resp = float(self.send_message(message))
        if resp > 0:
            time.sleep(BotConfiguration().bot_msg_visible)
            if self.delete_message(self.__timestamp):
                return 1
        return -1

    def send_message(self, message: str) -> str:
        """
        Sendet die angegebene Nachricht an den Channel, von dem der Bot die ID hat.

        @param message: Die Nachricht, welche der Bot senden soll.
        @param message: str

        @return: -1 Wenn die Nachricht nicht gesendet werden konnte.
                 >0 Der Timestamp der Nachricht.
        """
        if message == "":
            return "1"
        try:
            response = self.__client.chat_postMessage(channel=self.__channel_id.identifier.__repr__(), text=message)
            self.__timestamp = response.data.get('ts')
            return self.__timestamp
        except urllib.error.URLError:
            return '-1'

    def delete_message(self, ts: str) -> bool:
        """
        Löscht die Nachricht mit dem angegebenen Timestamp aus dem Channel, von dem der Bot die ID hat.

        @param ts: Der Timestamp der Nachricht, welche gelöscht werden soll.
        @param ts: str

        @return: False Wenn die Nachricht nicht gelöscht werden konnte.
                 True  Wenn die Nachricht gelöscht werden konnte.
        """

        if float(ts) > 0:
            try:
                resp = self.__client.chat_delete(token=self.__slack_token,
                                                 channel=self.__channel_id.identifier.__repr__(), ts=ts)
                return resp.data.get('ok')
            except SlackApiError:
                return False
            except urllib.error.URLError:
                return False
        else:
            return False
