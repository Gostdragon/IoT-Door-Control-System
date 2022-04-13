"""
Dieses Paket enthält Klassen, die physische oder virtuelle Entitäten
(z.B. Bot oder Türklingel) im Türsteuerungssystem modellieren und
entsprechende Methoden zum Steuern dieser Komponenten bieten.


Modules:
    bot: Die Klasse "Bot" in diesem Modul repräsentiert ein Bot-Objekt für eine
         ferngesteuerte Tür.
         Der Bot kann von Nutzern des Türsteuerungssystems abonniert werden und sendet
         Benachrichtigungen an seine Abonnenten, sobald der Klingeltaster im Türbereich
         betätigt wird.
    camera: Die Klasse "Camera" in diesem Modul repräsentiert eine (physische) Kamera für
            eine ferngesteuerte Tür.
            Bei Betätigung des Klingeltasters wird die Kamera automatisch eingeschaltet,
            filmt den Türbereich und überträgt dann den Livestream an die Webseite zur
            Türsteuerung.
    log: Die Klassen in diesem Modul repräsentieren Logs verschiedener Arten, in die
         z.B. Fehler- oder Benachrichtigungsnachrichten geschrieben werden können.
    doorbell: Dieses Modul kapselt Komponenten, die eine akustische Türklingel modellieren und
              auf die Betätigung des mit der Klingel übers WLAN verbundenen Klingeltasters
              mit einem akustischen Signal und entsprechenden Meldungen reagieren.
    button: Dieses Modul kapselt die Klasse "DoorOpenButtonObserver", die es ermöglicht,
            bei Betätigung des mit der Türsteuerung übers WLAN verbundenen Türöffnertasters
            ein Signal an das Türschloss zum Öffnen der Tür zu senden.

@author Fabian Schiekel
@version 20.02.2022

@author Ahmad Eynawi
@version 16.02.2022
"""