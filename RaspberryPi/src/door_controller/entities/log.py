from abc import ABC, abstractmethod
from RaspberryPi.src.data_model.configuration import BotConfiguration
from RaspberryPi.src.door_controller.entities.bot import SlackBot, Bot
from RaspberryPi.src.exceptions.exception import LogException

"""
Die Klassen in diesem Packet dienen zur Erstellung und Verwaltung von Log-Files für das Türsteuerungssystem.

Classes:
    Log: Die abstrakte Klasse für Log Klassen.
    LogLow: Eine Log Klasse mit niedrigem Informationsgehalt.
    LogMedium: Eine Log Klasse mit mittlerem Informationsgehalt.
    LogHigh: Eine Log Klasse mit hohem Informationsgehalt.
    
@author Fabian Schiekel
@version 1.0
"""


class Log(ABC):
    """
    Diese abstrakte Klasse repräsentiert ein Log.

    Attributes:
        bot(SlackBot): Die Log-Bot Instanz, auf der die Aktionen ausgeführt werden sollen.
        ts([str]): Die Liste, in der die Timestamps aller Log-Nachrichten gespeichert werden.
    Methods:
        bot_conf: Die Getter Methode für die Bot-Configuration.
        get_instance(abstrakt): Diese Methode repräsentiert die get_instance Methode des Singleton Design-patterns.
        send_log_msg: Diese Methode sendet die übergebene Nachricht mit dem gespeicherten Bot Objekt in das verbundene
            Log.
        clear_log_history: Löscht alle Log-Nachrichten, deren Timestamps in der Variable ts gespeichert sind.
    """
    __bot = None
    __ts = []
    __bot_conf = BotConfiguration()

    def __init__(self, bot: Bot):
        self.__bot = bot

    @property
    def bot_conf(self):
        """
        Gibt die Bot Configuration, in welcher die Daten für die Initialisierung der Logs gespeichert ist, zurück.

        @return: Die Bot Configuration.
        """
        return self.__bot_conf

    @abstractmethod
    def get_instance(self):
        pass

    def send_log_msg(self, msg: str) -> bool:
        """
        Sendet die Übergebene Nachricht an das Log. (Hier an einen Slack Bot.)

        @param msg: Die Log-Nachricht die gesendet werden soll.
        @param msg: str

        @return: True Wenn die Log Nachricht gesendet werden konnte.
                 False Wenn die Log Nachricht nicht gesendet werden konnte.
        @rtype: bool
        @raise LogException: Wenn die Log-Nachricht nicht gesendet werden konnte.
        """
        ts = self.__bot.send_message(msg)
        if abs(float(ts)) - 1 < float(0.01):
            # Keine Verbindung zum Log vorhanden, Fehlerbehandlung besteht aus keiner Reaktion.
            return True
        if float(ts) > 0:
            self.__ts.append(ts)
            return True
        else:
            raise LogException("Die Log-Nachricht konnte nicht gesendet werden!")

    def clear_log_history(self) -> bool:
        """
        Löscht alle Log-Nachtrichten, welche seid dem letzten Neustart geschrieben worden.

        @return: True Wenn die Log Nachrichten gelöscht werden konnte.
                 False Wenn die Log Nachrichten nicht gelöscht werden konnte.
        @rtype: bool
        @raise LogException: Log konnte nicht gelöscht werden.
        """
        if len(self.__ts) == 0:
            raise LogException("Nichts zum Löschen vorhanden!")

        for ts in self.__ts:
            resp = self.__bot.delete_message(ts)
        self.__ts.clear()
        return True


class LogInfo(Log):
    """
    Diese Klasse repräsentiert ein Log-Objekt mit dem Log Level Info.
    Erweitert die abstrakte Klasse Log.

    Attributes:
        instance: Die Instance des LogInfo Objekts.

    Methods:
        get_instance: Implementiert die abstrakte get_instance Methode der Oberklasse.
            Gibt das in instance gespeicherte Log-Objekt zurück oder erzeugt ein neues.
    """
    __instance = None

    def __init__(self):
        super().__init__(SlackBot(self.bot_conf.bot_log_token, self.bot_conf.bot_inf_id))

    @classmethod
    def get_instance(cls):
        """
        Implementiert die get_instance Methode des Singleton Design-Patterns.

        @return: Das in instance gespeicherte Log-Objekt oder eine neue Instance des Objekts.
        @rtype: LogInfo
        """
        if cls.__instance is None:
            cls.__instance = LogInfo()
        return cls.__instance


class LogError(Log):
    """
    Diese Klasse repräsentiert ein Log-Objekt mit dem Log Level Error.
    Erweitert die abstrakte Klasse Log.

    Attributes:
        instance: Die Instance des LogError Objekts.

    Methods:
        get_instance: Implementiert die abstrakte get_instance Methode der Oberklasse.
            Gibt das in instance gespeicherte Log-Objekt zurück oder erzeugt ein neues.
    """
    __instance = None

    def __init__(self):
        super().__init__(SlackBot(self.bot_conf.bot_log_token, self.bot_conf.bot_err_id))

    @classmethod
    def get_instance(cls):
        """
        Implementiert die get_instance Methode des Singleton Design-Patterns.

        @return: Das in instance gespeicherte Log-Objekt oder eine neue Instance des Objekts.
        @rtype: LogError
        """
        if cls.__instance is None:
            cls.__instance = LogError()
        return cls.__instance


class LogFatal(Log):
    """
    Diese Klasse repräsentiert ein Log-Objekt mit dem Log Level Fatal.
    Erweitert die abstrakte Klasse Log.

    Attributes:
        instance: Die Instance des LogFatal Objekts.

    Methods:
        get_instance: Implementiert die abstrakte get_instance Methode der Oberklasse.
            Gibt das in instance gespeicherte Log-Objekt zurück oder erzeugt ein neues.
    """
    __instance = None

    def __init__(self):
        super().__init__(SlackBot(self.bot_conf.bot_log_token, self.bot_conf.bot_fat_id))

    @classmethod
    def get_instance(cls):
        """
        Implementiert die get_instance Methode des Singleton Design-Patterns.

        @return: Das in instance gespeicherte Log-Objekt oder eine neue Instance des Objekts.
        @rtype: LogFatal
        """
        if cls.__instance is None:
            cls.__instance = LogFatal()
        return cls.__instance


