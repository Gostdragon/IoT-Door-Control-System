"""
Dieses Modul kapselt exceptions von verschiedenen Typen, die während der
Ausführung des Programms auftreten können.
Jede hier als Klasse modellierte Exception kann eine Fehlernachricht speichern,
die an den entsprechenden Konstruktor als Parameter übergeben wird.

Classes:
    SyntaxException: Repräsentiert einen Syntaxfehler, der während der Befehlszeilenanalyse
                     oder der Benutzereingabeanalyse auftreten kann.
    SemanticsException: Repräsentiert einen Semantikfehler, der während der Ausführung
                        des Programms auftreten kann.
    FileFormatException: Repräsentiert einen Formatfehler, der z.B. darauf hindeutet,
                         dass das Format einer gegebenen Datei keinem der vordefinierten
                         Dateiformaten entspricht.
    LogException: Repräsentiert einen Logfehler, der während der Ausführung
                  des Programms auftreten kann.
    ConnectionException: Repräsentiert einen Verbindungsfehler, der während der Ausführung
                         des Programms auftreten kann.
    NotImplementedException: Diese Exception wird verwendet, um beim Aufruf von noch nicht fertig implementiertem Code
                             eine Fehlermeldung auszugeben

@author Ahmad Eynawi
@version 16.02.2022

@author Fabian Schiekel
@version 19.02.2022
"""


class SyntaxException(Exception):
    """
    Diese Exception wird verwendet, um auf einen Syntaxfehler hinzuweisen,
    der während der Befehlszeilenanalyse oder der Benutzereingabeanalyse auftreten kann.

    Attributes:
        errorMessage (str): Die detaillierte Fehlernachricht, die in diesem
                            SyntaxException-Objekt gespeichert werden soll.

    Methods:
        __init__: Konstruktor der Klasse :class:`~exception.SyntaxException`.
    """

    def __init__(self, errorMessage: str):
        """
        Konstruktor der Klasse :class:`~exception.SyntaxException`.

        Erstellt und initialisiert eine Syntax-Exception, die auf einen Syntaxfehler
        hinweist und eine Fehlernachricht speichert.

        @param errorMessage: Die Fehlernachricht, die in diesem SyntaxException-Objekt
                             gespeichert werden soll und den Syntaxfehler genauer beschreibt.
        @type errorMessage: str
        """
        super().__init__(errorMessage)


class SemanticsException(Exception):
    """
    Diese Exception wird verwendet, um auf einen Semantikfehler hinzuweisen,
    der während der Ausführung des Programms auftreten kann.

    Attributes:
        errorMessage (str): Die detaillierte Fehlernachricht, die in diesem
                            SemanticsException-Objekt gespeichert werden soll.

    Methods:
        __init__: Konstruktor der Klasse :class:`~exception.SemanticsException`.
    """

    def __init__(self, errorMessage: str):
        """
        Konstruktor der Klasse :class:`~exception.SemanticsException`.

        Erstellt und initialisiert eine Semantik-Exception, die auf einen Semantikfehler
        hinweist und eine Fehlernachricht speichert.

        @param errorMessage: Die Fehlernachricht, die in diesem SemanticsException-Objekt
                             gespeichert werden soll und den Semantikfehler genauer beschreibt.
        @type errorMessage: str
        """
        super().__init__(errorMessage)


class FileFormatException(SemanticsException):
    """
    Diese Exception wird verwendet, um darauf hinzudeuten, dass das Format einer gegebenen
    Datei nicht den vordefinierten Dateiformaten entspricht und daher die
    entsprechende Datei nicht verarbeitet werden kann.

    Attributes:
        errorMessage (str): Die detaillierte Fehlernachricht, die in diesem
                            FileFormatException-Objekt gespeichert werden soll.

    Methods:
        __init__: Konstruktor der Klasse :class:`~exception.FileFormatException`.
    """

    def __init__(self, errorMessage: str):
        """
        Konstruktor der Klasse :class:`~exception.FileFormatException`.

        Erstellt und initialisiert eine FileFormatException, die auf einen Fehler
        in einem gegebenen Dateiformat hinweist und eine Fehlernachricht speichert.
        Dieser Fehler kann z.B. darin bestehen, dass das Format einer gegebenen Datei
        den vordefinierten Einschränkungen nicht genügt.

        @param errorMessage: Die Fehlernachricht, die in diesem FileFormatException-Objekt
                             gespeichert werden soll und den Formatfehler genauer beschreibt.
        @type errorMessage: str
        """
        super().__init__(errorMessage)


class LogException(Exception):
    """
    Diese Exception wird verwendet, um auf einen Logfehler hinzuweisen,
    der während der Ausführung des Programms auftreten kann.

    Attributes:
        errorMessage (str): Die detaillierte Fehlernachricht, die in diesem
                            LogException-Objekt gespeichert werden soll.

    Methods:
        __init__: Konstruktor der Klasse :class:`~exceptions.LogException`.
    """

    def __init__(self, error_message: str):
        """
        Konstruktor der Klasse :class:`~exceptions.LogException`.

        Erstellt und initialisiert eine Log-Exception, die auf einen Logfehler
        hinweist und eine Fehlernachricht speichert.

        @param error_message: Die Fehlernachricht, die in diesem LogException-Objekt
                             gespeichert werden soll und den Logfehler genauer beschreibt.
        @type error_message: str
        """
        super().__init__(error_message)


class ConnectionException(Exception):
    """
    Diese Exception wird verwendet, um auf einen Verbindungsfehler hinzuweisen,
    der während der Ausführung des Programms auftreten kann.

    Attributes:
        errorMessage (str): Die detaillierte Fehlernachricht, die in diesem
                            ConnectionException-Objekt gespeichert werden soll.

    Methods:
        __init__: Konstruktor der Klasse :class:`~exceptions.ConnectionException`.
    """

    def __init__(self, error_message: str):
        """
        Konstruktor der Klasse :class:`~exceptions.ConnectionException`.

        Erstellt und initialisiert eine Connection-Exception, die auf einen Verbindungsfehler
        hinweist und eine Fehlernachricht speichert.

        @param error_message: Die Fehlernachricht, die in diesem ConnectionException-Objekt
                             gespeichert werden soll und den ConnectionException genauer beschreibt.
        @type error_message: str
        """
        super().__init__(error_message)


class NotImplementedException(Exception):
    """
    Diese Exception wird verwendet, um beim Aufruf von nicht implementiertem Code eine
    Fehlermeldung auszugeben.

    Methods:
        __init__: Konstruktor der Klasse :class:`~exceptions.NotImplementedException`.
    """

    def __init__(self, error_message: str):
        """
        Konstruktor der Klasse :class:`~exceptions.NotImplementedException`.

        Erstellt und initialisiert eine NotImplementedException, die auf nicht unterstütze Funktionalitäten
        im Steuerungssystem hinweist.

        @param error_message: Die konkrete Fehlernachricht, die beim Werfen dieser Exception
                              ausgegeben werden soll.
        @rtype error_message: str
        """
        super().__init__(error_message)
