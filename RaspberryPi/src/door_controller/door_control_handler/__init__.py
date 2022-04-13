"""
Dieses Paket enthält alle Module, die für das Lesen, Validieren und Weiterleiten von Tokens zuständig sind.

Modules:
    DoorOpener: Dieses Modul ist für das Ansteuern und Öffnen der Tür zuständig.
    NFCReader: Dieses Modul ist für das Einlesen von NFC-Tokens zuständig.
    Observer: Dieses Modul ist für die Implementierung des Beobachter-Design_Pattern da.
        Ein Beobachter kann über Neuigkeiten eines zu beobachtenden Subjekts informiert werden.
    Subject: Dieses Modul dient zur Umsetzung des Beobachter-Design-Patterns. Ein Subjekt ist eine Klasse,
        die von Beobachtern beobachtet werden kann.
    TokenUpdater: Dieses Modul ist Teil des Beobachter-Design-Patterns. Es implementiert einen konkreten Beobachter.
    TokenValidation: Dieses Modul ist für die Validierung von Tokens zuständig.
    UserListUpdatesNotifier: Ist Teil des Beobachter-Design-Patterns.
        Es realisiert ein konkretes Subjekt, das beobachtet werden kann.

@author Lukas Wittenzellner
@version 1.0
"""