import os
import pygame
from typing_extensions import Final
from RaspberryPi.src.exceptions.exception import FileFormatException, SemanticsException
from RaspberryPi.src.data_model.mqtt_protocol import MQTTSubscriber
from RaspberryPi.src.data_model.configuration import MQTTProtocolConfiguration
from RaspberryPi.src.door_controller.entities.log import LogInfo

"""
Dieses Modul kapselt Komponenten, die eine akustische Türklingel modellieren und 
auf die Betätigung des mit der Klingel übers WLAN verbundenen Klingeltasters
mit einem akustischen Signal und entsprechenden Meldungen reagieren.

Classes: 
    Doorbell: Repräsentiert eine akustische Klingel, die beim Eintreten vordefinierter
              Ereignisse (z.B. Betätigung eines Klingeltasters) akustische Signale 
              abgegeben kann.

Methods:
    on_connect: Gibt eine entsprechende Erfolgsmeldung aus, wenn sich die akustische Klingel
                erfolgreich mit dem MQTT-Server verbindet.
    on_message: Gibt eine entsprechende Erfolgsmeldung aus und weist die Klingel zum Klingen
                an, wenn ein :class:`~mqtt_protocol.MQTTPublisher` die Nachricht 
                "sound" zum Topic "RaspberryPiZeroW/Doorbell" sendet.

@author Ahmad Eynawi
@version 16.02.2022
"""


class Doorbell:
    """
    Diese Klasse repräsentiert eine akustische Türklingel im Türsteuerungssystem.

    Diese Klingel wird dazu verwendet, um akustische Signale bei Betätigung des
    Klingeltasters abzugeben und auf diese Weise die Nutzer des Türsteuerungssystems
    zu benachrichtigen.

    Attributes:
        ringtonePath (str): Der Pfad zur Audiodatei, welche die Türklingel beim Aufruf
                         der sound-Methode abspielen soll.
        speakerVolume (float): Die Lautstärke, mit der die Türklingel den Klingelton
                             abspielen soll.

    Methods:
        ringtonePath (Getter): Get-Methode für den Pfad zur Tondatei, die von dieser Türklingel
                            abgespielt wird.
        ringtonePath (Setter): Set-Methode für den Pfad zur Tondatei, die von dieser Türklingel
                            abgespielt wird.
        speakerVolume (Getter): Get-Methode für die Lautstärke, mit der die Türklingel den
                                Klingelton abspielt.
        speakerVolume (Setter): Set-Methode für die Lautstärke, mit der die Türklingel den
                                Klingelton abspielt.
        sound: Spielt den in diesem Doorbell-Objekt gespeicherten Klingelton ab.
        validateRingtonePath: Stellt sicher, dass der gegebene Pfad zur Tondatei existiert
                           und die Endung ".wav" oder ".mp3" hat und wirft andernfalls
                           eine entsprechende Exception mit einer Fehlernachricht.
        validateSpeakerVolume: Stellt sicher, dass die gegebene Lautstärke einen
                               gültigen Wert zwischen 0 (i.e. 0 %) und 1 (i.e. 100 %) hat.
        __init__: Konstruktor der Klasse :class:`~Doorbell.Doorbell`
    """

    MINIMUM_SPEAKER_VOLUME: Final[float] = 0.0
    MAXIMUM_SPEAKER_VOLUME: Final[float] = 1.0
    RINGTONE_PATH: Final[str] = "/home/pi/Music/ringtones/bell_sms_wav.wav"
    TOPIC: Final[str] = "RaspberryPiZeroW/Doorbell"
    PAYLOAD: Final[str] = "sound"

    def __init__(self, ringtonePath=RINGTONE_PATH, speakerVolume=MAXIMUM_SPEAKER_VOLUME):
        """
        Konstruktor der Klasse :class:`~Doorbell.Doorbell`.

        Erstellt und initialisiert eine akustische Türklingel.

        Die Türklingel gibt beim Eintreten vordefinierter Ereignisse akustische Signale
        zur Benachrichtigung der Nutzer des Türsteuerungssystems ab.

        @param ringtonePath: Der Pfad zur Tondatei, die von der Türklingel abgespielt wird.
        @type ringtonePath: str
        @param speakerVolume: Die Lautstärke, mit der die Türklingel den Klingelton abspielt.
                              Die Lautstärke darf nur Werte zwischen 0 (i.e. 0 %) und
                              1 (i.e. 100 %) annehmen.
        @type speakerVolume: float

        @raise:
        FileNotFoundError: Wenn die Tondatei, auf die der gegebene Pfad verweisen soll,
                           nicht existiert oder wenn der Pfad auf ein Verzeichnis
                           verweist.
        FileFormatException: Wenn die Tondatei, auf die der gegebene Pfad verweist,
                             nicht das WAV- oder das MP3-Format hat.
        SemanticsException: Wenn die als Parameter übergebene Lautstärke nicht aus dem
                            Wertebereich [0, 1] ist.
        """
        Doorbell.validateRingtonePath(ringtonePath)
        Doorbell.validateSpeakerVolume(speakerVolume)
        self.__ringtonePath = ringtonePath
        self.__speakerVolume = speakerVolume

    @property
    def ringtonePath(self):
        """
        Gibt den Pfad zur Tondatei zurück, die von dieser Türklingel abgespielt wird.

        @return: Den Pfad zur Tondatei, der in diesem Doorbell-Objekt gespeichert ist.
        @rtype: str
        """
        return self.__ringtonePath

    @ringtonePath.setter
    def ringtonePath(self, ringtonePath: str):
        """
        Speichert den als Parameter übergebenen Pfad zur Tondatei in diesem Doorbell-Objekt,
        sodass diese Tondatei beim Aufruf der sound-Methode abgespielt wird.

        @param ringtonePath: Der Pfad zur Tondatei, der in diesem Doorbell-Objekt gespeichert
                             werden soll.
        @type ringtonePath: str

        @raise:
        FileNotFoundError: Wenn die Tondatei, auf die der gegebene Pfad verweisen soll,
                           nicht existiert oder wenn der Pfad auf ein Verzeichnis
                           verweist.
        FileFormatException: Wenn die Tondatei, auf die der gegebene Pfad verweist,
                             nicht das WAV- oder das MP3-Format hat.
        """
        Doorbell.validateRingtonePath(ringtonePath)
        self.__ringtonePath = ringtonePath

    @property
    def speakerVolume(self):
        """
        Gibt die Lautstärke zurück, mit der diese Türklingel den Klingelton abspielt.

        Die Lautstärke 0 entspricht 0 % und die Lautstärke 1 entspricht 100 %.

        @return: Die aktuelle Lautstärke dieser Türklingel.
        @rtype: float
        """
        return self.__speakerVolume

    @speakerVolume.setter
    def speakerVolume(self, speakerVolume: float):
        """
        Speichert die Lautstärke, mit der die Türklingel den Klingelton zukünftig abspielen
        soll.

        Die Lautstärke darf nur Werte zwischen 0 (Minimum) und 1 (Maximum) annehmen.

        @param speakerVolume: Die Lautstärke, die in diesem Doorbell-Objekt gespeichert
                              werden soll.
        @type speakerVolume: float

        @raise:
            SemanticsException: Wenn die als Parameter übergebene Lautstärke nicht aus dem
                                Wertebereich [0, 1] ist.
        """
        Doorbell.validateSpeakerVolume(speakerVolume)
        self.__speakerVolume = speakerVolume

    def sound(self):
        """
        Spielt den in diesem Doorbell-Objekt gespeicherten Klingelton ab.
        """
        pygame.mixer.init()
        pygame.mixer_music.set_volume(self.__speakerVolume)
        pygame.mixer.music.load(self.__ringtonePath)
        pygame.mixer.music.play()

        # Stellt sicher, dass die Tondatei vollständig abgespielt wird.
        while pygame.mixer.music.get_busy():
            continue

    @staticmethod
    def validateRingtonePath(path: str):
        """
        Stellt sicher, dass der als Parameter übergebene Pfad auf eine existierende Datei
        (kein Verzeichnis) verweist und die Endung ".wav" oder ".mp3" hat.

        @param path: Der Pfad zur Tondatei, der durch diese Methode validiert werden soll.
        @type path: str

        @raise:
            FileNotFoundError: Wenn die Tondatei, auf die der gegebene Pfad verweisen soll,
                               nicht existiert oder wenn der Pfad auf ein Verzeichnis
                               verweist.
            FileFormatException: Wenn die Tondatei, auf die der gegebene Pfad verweist,
                                 nicht das WAV- oder das MP3-Format hat.
        """
        if not os.path.exists(path):
            raise FileNotFoundError("Ungültiger Pfad! Am angegebenen Speicherort befindet sich keine Datei.")
        if not os.path.isfile(path):
            raise FileNotFoundError("Der angegebene Pfad muss auf eine Datei zeigen, nicht auf einen Ordner!")
        if not path.lower().endswith(('.wav', '.mp3')):
            raise FileFormatException("Als Audiodateien für die Türklingel werden nur MP3- und WAV-Dateien akzeptiert!")

    @staticmethod
    def validateSpeakerVolume(speakerVolume: float):
        """
        Stellt sicher, dass die als Parameter übergebene Lautstärke einen Wert
        zwischen 0 (i.e. 0 %) und 1 (i.e. 100 %) hat.

        @param speakerVolume: Die Lautstärke, die durch diese Methode validiert werden soll.
        @type speakerVolume: float

        @raise:
            SemanticsException: Wenn die als Parameter übergebene Lautstärke nicht aus dem
                                Wertebereich [0, 1] ist.
        """
        if speakerVolume < Doorbell.MINIMUM_SPEAKER_VOLUME or speakerVolume > Doorbell.MAXIMUM_SPEAKER_VOLUME:
            raise SemanticsException("Die Lautstärke des Lautsprechers muss zwischen 0 und 1 liegen!")


# Der folgende Codeabschnitt definiert die on_connect- und on_message-Funktionen
# (siehe Modul "mqtt_protocol") für die Türklingel des Türsteuerungssystems und
# führt dann eine Endlosschleife aus, in der auf das Eintreffen von Signalen
# von der Klasse :class:`~BellPushHandler.DoorbellNotifier`
# gewartet wird. Beim Eintreffen eines entsprechenden Signals wird die sound-Methode
# des Doorbell-Objektes aufgerufen, damit die (physische) Türklingel ein akustisches
# Signal zur Benachrichtigung abgibt.
if __name__ == '__main__':
    def on_connect(client, userdata, flags, resultCode):
        """
        Definiert die Aktionen, die ausgeführt werden sollen, wenn die Türklingel
        sich erfolgreich mit dem MQTT-Server verbunden hat.

        @param client: Die MQTT-Client-Instanz für diesen Rückruf.
        @param userdata: Die privaten Benutzerdaten, wie sie durch die Methoden Client()
                         oder userdata_set() festgelegt wurden.
        @param flags: Die vom Broker gesendeten Antwort-Flags.
        @param resultCode: Das Verbindungsergebnis als Integer.
                           Ergebniscode 0 bedeutet, dass die Verbindung mit dem Broker
                           erfolgreich hergestellt werden konnte.
        @type resultCode: int
        """
        LogInfo.get_instance().send_log_msg("Die Türklingel hat sich mit dem MQTT-Broker "
                                            "mit Ergebniscode " + str(resultCode) + " verbunden.")

        # Abonniert das Topic "sound" für die Türklingel, sodass beim Eintreffen von
        # Nachrichten zu diesem Topic die Türklingel benachrichtigt wird.
        # Diese Funktion sorgt auch dafür, dass das obengenannte Topic automatisch wieder
        # abonniert wird, wenn die Verbindung zum MQTT-Server nach einer Unterbrechung
        # wiederhergestellt wird.
        client.subscribe(Doorbell.TOPIC)
        LogInfo.get_instance().send_log_msg(f"Die Türklingel hat das Topic \""
                                            + Doorbell.TOPIC + "\" abonniert.")


    def on_message(client, userdata, message):
        """
        Definiert die Aktionen, die von der akustischen Klingel auszuführen sind,
        wenn das entsprechende Doorbell-Objekt eine Nachricht zum Topic
        "sound" von einem MQTT-Publisher (i.d.F. der Klasse "DoorbellNotifier") erhält.

        @param client: Die Client-Instanz für diesen Rückruf.
        @param userdata: Die privaten Benutzerdaten, wie sie durch die Methoden Client()
                         oder userdata_set() festgelegt wurden.
        @param message: Eine Instanz der Klasse "MQTTMessage".
        @type message: MQTTMessage
        """
        messageString = message.payload.decode()
        LogInfo.get_instance().send_log_msg("Die Türklingel hat die Nachricht \"" + messageString +
                                            "\" zum Thema \"" + message.topic + "\" erhalten.")
        if messageString == Doorbell.PAYLOAD:
            doorbell = Doorbell()
            doorbell.sound()


    mqttConfig = MQTTProtocolConfiguration(Doorbell.TOPIC, Doorbell.PAYLOAD)
    doorbellMQTTSubscriber = MQTTSubscriber(mqttConfig, on_connect, on_message)
    doorbellMQTTSubscriber.run()
