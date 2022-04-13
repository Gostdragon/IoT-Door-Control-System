
"""
Dieses Paket enthält alle Klassen, die für die Speicherung und Verwaltung
der anwendungsspezifischen Daten im Türsteuerungssystem zuständig sind.

Die gespeicherten Daten beziehen sich auf die Nutzer der Türsteuerung,
die mit diesem Software-System gesteuerten Türen
und die NFC-Schlüsseltokens, mit denen die Türen geöffnet werden können.

Modules:
    door: Dieses Modul kapselt alle Klassen, die für die Speicherung und Verwaltung der
          Daten der durch dieses Software-System gesteuerten Türen zuständig sind.
    identifier: Dieses Modul kapselt alle Klassen, die für die Darstellung und Überprüfung
                der im Türsteuerungssystem verwendeten Identifikatoren zuständig sind.
    key_token: Dieses Modul kapselt alle Klassen, welche die verschiedenen Typen
               von Schlüsseltokens modellieren.
               Die in diesem Modul modellierten Tokens werden im Türsteuerungssystem für
               das Öffnen der elektrisch ansteuerbaren Türen verwendet.
    name: Dieses Modul kapselt alle Klassen, die für die Modellierung von Nutzernamen
          im Türsteuerungssystem zuständig sind.
    password: Dieses Modul kapselt alle Klassen, die für die Darstellung und Überprüfung
              der im Türsteuerungssystem verwendeten Passwörter zuständig sind.
    user: Dieses Modul kapselt alle Klassen, die für die Modellierung von Nutzern
          im Türsteuerungssystem zuständig sind.
          Nutzer sind in diesem Zusammenhang alle Personen, welche die durch das Steuerungssystem
          gesteuerten Türen benutzen.
    mqtt_protocol: Dieses Modul kapselt Klassen, mithilfe deren Signale zwischen bestimmten (physischen)
                   Komponenten im Türsteuerungssystem über das MQTT-Protokoll (Message Queuing Telemetry Transport)
                   drahtlos gesendet werden können.
    configuration: Dieses Modul kapselt alle Klassen, die für die Speicherung von Konfigurationsdaten
                   im Türsteuerungssystem zuständig sind.

@author Ahmad Eynawi
@version 16.02.2022
"""
