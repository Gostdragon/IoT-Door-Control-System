from typing_extensions import Final

from RaspberryPi.src.data_model.configuration import MQTTProtocolConfiguration
from RaspberryPi.src.data_model.mqtt_protocol import MQTTSubscriber

"""
Dieses Modul kapselt die Klasse "DoorOpenButtonObserver".
Die Klasse "DoorOpenButtonObserver" modelliert einen Benachrichtiger, der
bei Betätigung des mit der Türsteuerung übers WLAN verbundenen Türöffnertasters
ein Signal an das Türschloss zum Öffnen der Tür sendet.

Classes:
    DoorOpenButtonObserver: Repräsentiert einen Benachrichtiger, der den Status 
                            des Türöffnertasters ständig beobachtet und bei Betätigung 
                            dieses Tasters ein Signal zum Öffnen der ferngesteuerten 
                            Tür sendet.
                            
@author Ahmad Eynawi
@version 19.02.2022
"""


class DoorOpenButtonObserver:
    """
      Repräsentiert einen Benachrichtiger, der den Status des Türöffnertasters ständig beobachtet
      und bei Betätigung dieses Tasters ein Signal zum Öffnen der ferngesteuerten Tür sendet.

      Attributes:
      mqttConfig (:class:`~configuration.MQTTProtocolConfiguration`):
                  Die Konfigurationsdaten des MQTT-Protokolls für den in diesem
                  DoorOpenButtonObserver-Objekt gespeicherten MQTT-Subscriber.
      on_connect ((client, userdata, flags, resultCode) -> None):
                  Diese Methode definiert die Aktionen, die der obengenannte Subscriber ausführt,
                  wenn er eine CONNACK-Antwort (Verbindungsaufbau-Bestätigung) vom MQTT-Broker erhält.
      on_message ((client, userdata, message) -> None):
                  Diese Methode definiert die Aktionen, die der der obengenannte Subscriber ausführt,
                  wenn er eine Nachricht zu einem der von ihm abonnierten Topics erhält.

      Methods:
          run: Startet den mit diesem Benachrichtiger verbundenen MQTT-Subscriber und reagiert
               auf vordefinierte Nachrichten vom MQTT-Publisher, der mit dem Türöffnertaster
               verbunden ist, mit dem Senden eines Signals für das Öffnen der ferngesteuerten Tür.
          __init__: Konstruktor der Klasse :class:`~Button.DoorOpenButtonObserver`
      """

    TOPIC: Final[str] = "shellies/shellybutton1-E8DB84ACF3CD/input_event/0"
    DOOR_OPEN_BUTTON_INPUT_EVENT_IDENTIFIER: Final[str] = "event"
    DOOR_OPEN_BUTTON_SHORT_PUSH_EVENT: Final[str] = "S"

    def __init__(self, mqttConfig: MQTTProtocolConfiguration, on_connect, on_message):
        """
        Konstruktor der Klasse :class:`~Button.DoorOpenButtonObserver`.

        Erstellt und initialisiert einen Benachrichtiger, der bei Betätigung des
        Türöffnertasters ein Signal an das Türschloss für das Öffnen der Tür sendet.

        @param mqttConfig: Die Konfigurationsdaten des MQTT-Protokolls für den in diesem
                           DoorOpenButtonObserver-Objekt gespeicherten MQTT-Subscriber.
        @type mqttConfig: :class:`~configuration.MQTTProtocolConfiguration`
        @param on_connect: Diese Methode definiert die Aktionen, die der obengenannte Subscriber ausführt,
                           wenn er eine CONNACK-Antwort (Verbindungsaufbau-Bestätigung) vom MQTT-Broker erhält.
        @type on_connect: on_connect(client, userdata, flags, resultCode) -> None
        @param on_message: Diese Methode definiert die Aktionen, die der der obengenannte Subscriber ausführt,
                           wenn er eine Nachricht zu einem der von ihm abonnierten Topics erhält.
        @type on_message: (client, userdata, message) -> None
        """
        self.__doorOpenButtonMQTTSubscriber = MQTTSubscriber(mqttConfig, on_connect, on_message)

    def run(self):
        """
        Startet den mit diesem Benachrichtiger verbundenen MQTT-Subscriber mit einer Endlosschleife,
        in der auf das Eintreffen von Nachrichten zum vordefinierten Topic für das Öffnen der Tür
        gewartet bzw. reagiert wird.
        """
        self.__doorOpenButtonMQTTSubscriber.run()
