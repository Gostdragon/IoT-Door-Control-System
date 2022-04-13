import threading
import requests
from abc import ABC, abstractmethod
import urllib.error
from RaspberryPi.src.data_model.mqtt_protocol import MQTTPublisher
from RaspberryPi.src.data_model.configuration import MQTTProtocolConfiguration
from RaspberryPi.src.door_controller.entities.log import LogInfo

from RaspberryPi.src.door_controller.entities.bot import Bot
from RaspberryPi.src.door_controller.entities.camera import Camera
from RaspberryPi.src.door_controller.entities.log import LogError
from RaspberryPi.src.door_controller.entities.doorbell import Doorbell


"""
Die Klassen in diesem Paket dienen der Weiterleitung des Signals, sobald ein Nutzer den Klingeltaster betätigt.
Das Signal wird an verbundene Soft- und Hardware weitergeleitet.

Classes:
    BellEventObserver: Die abstrakte Observer-Oberklasse des Observer-Design-Patterns.
    BellEventSubjekt: Die abstrakte Subjekt-Oberklasse des Observer-Design-Patterns.
    BellPushEventHandler: 
    BotNotifier: Implementiert die abstrakte Observer-Oberklasse und 
        benachrichtigt bei einer Zustandsänderung einen Bot.
    DoorbellNotifier: Implementiert die abstrakte Observer-Oberklasse und 
        benachrichtigt bei einer Zustandsänderung eine Türklingel.
    CameraNotifier:Implementiert die abstrakte Observer-Oberklasse und 
        benachrichtigt bei einer Zustandsänderung eine Kamera.
        
@author Fabian Schiekel
@version 1.0

@author Ahmad Eynawi
@version 16.02.2022
"""


class BellEventObserver(ABC):
    """
    Diese abstrakte Klasse bildet mit der abstrakten Klasse BellEventSubject das Observer-Design-Pattern.
    Alle Klassen, welche diese abstrakte Klasse implementieren, können als Observer bei einer Zustandsänderung
    nach Betätigung des Klingeltasters, benachrichtigt werden.

    Methods:
        update (abstract): Diese Methode wird bei einer Zustandsänderung des Subjektes aufgerufen.
    """

    @abstractmethod
    def update(self):
        """
        Diese Methode sorgt für eine Weiterverarbeitung des Signals, wenn sich der Zustand des verbundenen
        Subjektes (BellPushEventHandler) ändert. Alle registrierten Observer bekommen nach Betätigung des Klingeltasters
        eine Benachrichtigung durch den BellPushEventHandler.
        """
        pass


class BellEventSubject(ABC):
    """
    Diese abstrakte Klasse bildet zusammen mit der abstrakten Klasse BellEventObserver das Observer-Design-Pattern.
    Hierbei sind alle Kindsklassen dieser abstrakten Klasse Subjekte und können alle registrierten Observer
    über eine Änderung ihres Zustandes, die mit der Betätigung des Klingeltasters einhergeht, benachrichtigen.
    Observer sind in diesem Zusammenhang alle Klassen bzw. Entitäten,
    die auf die Betätigung des Klingeltasters reagieren (müssen).

    Attributes:
        registered_observers (list): Die Liste mit allen dem Subjekt verbundenen Observern.

    Methods:
        addObserver: Fügt einen Observer dem Datenspeicher der registrierten Observer hinzu.
        deleteObserver: Löscht einen Observer aus dem Datenspeicher der registrierten Observer.
        notifyObserver: Benachrichtigt alle registrierten Observer über eine Zustandsänderung des Subjektes.
        setState (abstract): Mit dieser Methode kann eine Zustandsänderung des Subjektes signalisiert werden.

    """

    def __init__(self):
        """
        Konstruktor der Klasse :class`~BellPushHandler.BellEventSubjekt`.

        Erstellt und initialisiert einen Datenspeicher für die verbundenen Observer für dieses Subjekt.
        Dieser Datenspeicher speichert die mit dem Subjekt verbundenen Observer.
        """
        self.registered_observers = []

    def addObserver(self, observer: BellEventObserver):
        """
        Der Übergebene Observer wird dem Subejekt als registrierter Observer hinzugefügt.

        @param observer: Der Observer, der dem Subjekt hinzugefügt werden soll.
        @type observer: class`~BellPushHandler.BellEventObserver`.
        @return: 1 Wenn der Observer hinzugefügt wurde.
                -1 Wenn der Observer nicht hinzugefügt werden konnte.
        @rtype: int
        """
        self.registered_observers.append(observer)
        return 1

    def deleteObserver(self, observer: BellEventObserver):
        """
         Löscht einen Observer aus der Liste der registrierten Observer.

        @param observer: Der Observer, der dem Subjekt als registrierter Observer entfernt werden soll.
        @type observer: class`~BellPushHandler.BellEventObserver`.
        @return: 1 Wenn der Observer entfernt werden konnte.
                 0 Wenn das Subjekt keine registrierten Observer hat.
                -1 Wenn der Observer nicht entfernt werden konnte.
        @rtype: int
        """
        if len(self.registered_observers) != 0:
            self.registered_observers.remove(observer)
            return 1
        else:
            return 0

    def notifyObservers(self) -> int:
        """
        Benachrichtigt alle bei dem Subjekt registrierten Observer über eine Zustandsänderung des Subjektes.

        @return: 1 Wenn alle registrierten Observer benachrichtigt werden konnten.
                -1 Wenn nicht alle registrierten Observer benachrichtigt werden konnten.
        @rtype: int
        """
        __threads = []
        __ret = 1

        class Thread(threading.Thread):
            def __init__(self, observer, ret: int):
                threading.Thread.__init__(self)
                self.daemon = True
                self.observer = observer
                self.ret = ret

            def run(self):
                resp = self.observer.update()
                if resp < 0:
                    self.ret = -1

        for ele in self.registered_observers:
            thread = Thread(ele, __ret)
            __threads.append(thread)
            thread.start()

        for a in list(range(len(self.registered_observers))):
            thread = __threads[a]
            thread.join()

        return __ret

    @abstractmethod
    def setState(self):
        """
        Mit dieser Methode kann eine Zustandsänderung des Subjektes signalisiert werden.
        Dies geschieht, sobald der Klingeltaster betätigt wurde.
        """
        pass


class BellPushEventHandler(BellEventSubject):
    """
    Erweitert die abstrakte Klasse BellEventSubject und implementiert die abstrakte Methode setState.
    Diese Klasse leitet nach der Betätigung des Klingeltasters ein Signal an alle registrierten Observer
    (Akustische Klingel, Kamera, Bot und Webseite...) weiter.

    Methods:
        setState: Mit dieser Methode kann eine Zustandsänderung des Subjektes signalisiert werden,
            was für eine Benachrichtigung aller bei diesem Subjekt registrierten Observer sorgt.
    """
    def setState(self) -> int:
        """
        Mit dieser Methode kann eine Zustandsänderung des Subjektes signalisiert werden,
        was für eine Benachrichtigung aller bei diesem Subjekt registrierten Observer sorgt.
        @return: 1 Wenn alle bei dem Subjekt registrierten Observer benachrichtigt werden konnten.
                -1 Wenn nicht alle registrierten Observer benachrichtigt werden konnten.
        @rtype: int
        """
        if self.notifyObservers() != 1:
            return -1
        else:
            return 1


class BotNotifier(BellEventObserver):
    """
    Diese Klasse implementiert das Interface BellEventObserver und sendet auf Befehl des Subjektes
    (BellPushEventHandler) ein Signal an den verbundenen Bot.

    Methods:
       update (abstract): Diese Methode wird bei einer Zustandsänderung des Subjektes aufgerufen.
    """

    def __init__(self, bot: Bot, msg: str):
        """
        Der Konstruktor der Klasse :class`~BellPushHandler.BotNotifier`.

        Erstellt und initialisiert ein BotNotifier und das damit verbundenen Bot-Objekt.

        @param msg: Die Nachricht, welche von dem Bot gesendet werden soll.
        @param bot: Der Bot, auf welchem die Aktionen ausgeführt werden sollen.

        @type msg: str
        @type bot: :class:`~bot.SlackBot`

        @raise: SyntaxException: Die Bot-ID und/oder die Kanal-ID ist nicht valide.
        @raise: urllib.error.URLError: Es konnte keine Verbindung zum Bot aufgebaut werden.
        """
        self.__msg = msg
        self.__bot = bot

    def update(self) -> int:
        """
        Implementiert die entsprechende Methode der abstrakten Klasse.
        Diese Methode sendet ein Signal an den verbundenen Bot, woraufhin dieser eine Nachricht in den im verbundenen
        Channel sendet.

        @return: 1 Wenn der Bot die Aktion ausführen konnte.
                -1 Wenn der Bot die Aktion nicht ausführen konnte.
        @rtype: int
        """
        try:
            rep = self.__bot.send_and_delete_message(message=self.__msg)
            if rep > 0:
                return 1
            else:
                return -1
        except urllib.error.URLError:
            return -1


class DoorbellNotifier(BellEventObserver):
    """
    Diese Klasse ist dafür zuständig, die akustische Türklingel bei Betätigung
    des Klingeltasters zu benachrichtigen, damit die Klingel ein akustisches
    Signal abgibt.

    Methods:
        update: Benachrichtigt die akustische Klingel, sobald der Klingeltaster
                betätigt wird.
    """
    def update(self):
        """
        Sendet bei Betätigung des Klingeltasters ein Signal über das MQTT-Protokoll
        an die akustische Klingel, damit die Klingel ein akustisches Signal abgibt.
        """

        def on_connect(client, userdata, flags, resultCode):
            LogInfo.get_instance().send_log_msg(f"Der Benachrichtiger der Türklingel hat sich mit dem MQTT-Broker mit "
                                                f"Ergebniscode {resultCode} verbunden.")

        mqttConfig = MQTTProtocolConfiguration(Doorbell.TOPIC, Doorbell.PAYLOAD)
        doorbellMQTTPublisher = MQTTPublisher(mqttConfig, on_connect)
        doorbellMQTTPublisher.publish(mqttConfig.topic, mqttConfig.payload)
        LogInfo.get_instance().send_log_msg(f"Der Benachrichtiger der Türklingel hat die Nachricht \""
                                            + mqttConfig.payload + "\" zum Thema \"" +
                                            mqttConfig.topic + "\" publiziert.")


class CameraNotifier(BellEventObserver):
    """
    Diese Klasse implementiert die abstrakte Klasse BellEventObserver und sendet auf Befehl des Subjektes
    (BellPushEventSender) ein Signal an die mit dem Notifier verbundenen Kameras.

    Methods:
        update (abstract): Diese Methode wird bei einer Zustandsänderung des Subjektes aufgerufen.
    """

    def __init__(self, cam: Camera):
        """
        Der Konstruktor der Klasse :class:`~BellPushHandler.CameraNotifier`.

        Erstellt ein diesem Notifier verbundenen Objekt der Klasse: :class:`~Camera.Camera`.

        @param cam: Die Kamera.

        @type cam: :class:`~camera.TapoCamera`
        """
        self.__camera = cam

    def update(self) -> int:
        """
        Implementiert die entsprechende Methode der abstrakten Klasse.
        Diese Methode sendet ein Signal an die verbundene Kamera, woraufhin diese sich einschaltet und ein
        Video-Livstream sendet.

        @return: 1 Wenn die Kamera die Aktion ausführen konnte.
                -1 Wenn die Kamera die Aktion nicht ausführen konnte.
        @rtype: int
        """
        try:
            resp = self.__camera.ringEvent()
            if resp > 0:
                return 1
            elif resp == 0:
                return 0
            else:
                return -1
        except requests.exceptions.ConnectionError as e:
            LogError.get_instance().send_log_msg("Die Kamera ist nicht verbunden! \n Fehlernachricht: " + e.__repr__())
