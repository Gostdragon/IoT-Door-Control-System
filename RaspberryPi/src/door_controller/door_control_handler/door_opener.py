import time

from RaspberryPi.src.door_controller.entities.log import LogInfo
from gpiozero.pins.rpigpio import RPiGPIOFactory
from gpiozero import LED
from RaspberryPi.src.data_model.configuration import PiConfiguration
"""
Dieses Modul kapselt die Klasse 'DoorOpener', die für die direkte Steuerung der Tür
zuständig ist.

Classes: 
    DoorOpener: Repräsentiert ein Steuerungsmittel, mithilfe dessen Signale 
                an das Türschloss der ferngesteuerten Tür zum Öffnen der Tür 
                gesendet werden können.
                
@author Ahmad Eynawi
@version 19.02.2022
"""


class DoorOpener:
    """
     Repräsentiert ein Steuerungsmittel, mit dem Signale direkt an das Türschloss
     zum Öffnen der ferngesteuerten Tür gesendet werden können.

     Methods:
         openDoor: Diese Methode sendet ein Signal zum Öffnen der Tür.
         __init__: Der Default-Konstruktor der Klasse :class:`~door_opener.DoorOpener`.
     """

    def __init__(self):
        """
        Konstruktor der Klasse :class:`~door_opener.DoorOpener`.

        Erstellt ein DoorOpener-Objekt (ohne Attribute), mit dem Signale an das Türschloss
        zum Öffnen der ferngesteuerten Tür gesendet werden können.
        """
        pass

    def openDoor(self) -> bool:
        """
        Diese Methode öffnet die ferngesteuerte Tür. Dies wird momentan durch das Einschalten einer (grünen)
        LED simuliert.

        @return: `True`, falls die Tür geöffnet werden konnte.
                 `False`, falls die Tür nicht geöffnet werden konnte.
        @rtype: bool
        """
        led = LED(pin=PiConfiguration().pin_green)
        led.on()
        LogInfo.get_instance().send_log_msg("Die Tür wurde geöffnet")
        time.sleep(5)
        led.off()
        led.close()
        return True
