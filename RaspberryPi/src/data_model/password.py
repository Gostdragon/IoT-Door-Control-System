from RaspberryPi.src.exceptions.exception import SyntaxException

"""
Dieses Modul kapselt alle Klassen, die für die Darstellung und Überprüfung
der im Türsteuerungssystem verwendeten Passwörter zuständig sind.

Classes:
    Password: kapselt das Passwort einer autorisierten Entität im Türsteuerungssystem.
   
@author Ahmad Eynawi
@version 26.01.2022
"""


class Password:
    """
    Diese Klasse kapselt ein Passwort, das für die Authentifizierung von autorisierten Entitäten
    (z.B. Nutzern) im Türsteuerungssystem verwendet wird.

    Attributes:
        password (str): Der Passwort-String, der für die Authentifizierung einer Entität
                        im Steuerungssystem verwendet wird.

    Methods:
        password: Gibt das als String gespeicherte Passwort zurück.
        __init__: Konstruktor der Klasse :class:`~password.Password`.
        __repr__: Gibt eine String-Repräsentation für dieses Password-Objekt zurück.
        __eq__: Vergleicht dieses Password-Objekt mit einem anderen Objekt.
        __hash__: Berechnet einen Hashwert für dieses Password-Objekt.
    """

    def __init__(self, password: str):
        """
        Konstruktor der Klasse :class:`~password.Password`.

        Erstellt und initialisiert ein neues Passwort, mit dem eine Entität im
        Türsteuerungssystem authentifiziert werden kann.

        @param password: Der Passwort-String, der für die Authentifizierung
                         einer Entität im Steuerungssystem verwendet wird.
        @type password: str

        @raise:
            SyntaxException: Wenn der als Parameter übergebene String leer ist
                             (Ein Passwort muss mindestens ein Zeichen enthalten).
        """
        if password == "":
            raise SyntaxException("Das Passwort muss mindestens ein Zeichen enthalten!")
        self.__password = password

    @property
    def password(self):
        """
        Get-Methode für das in diesem Password-Objekt gespeicherte Passwort.

        @return: Das in diesem Password-Objekt gespeicherte Password.
        @rtype: str
        """
        return self.__password

    def __repr__(self):
        """
        Erzeugt eine textuelle Darstellung für dieses Password-Objekt und gibt diese
        Darstellung als String zurück.

        @return: Die String-Repräsentation dieses Password-Objekts.
        @rtype: str
        """
        return f"{self.__password}"

    def __eq__(self, other: object):
        """
        Vergleicht dieses Password-Objekt mit dem Objekt `other`.

        Zwei Password-Objekte werden als gleich betrachtet, wenn sie den gleichen
        Password-String speichern.

        @param other: Das Objekt, das mit diesem Password-Objekt verglichen werden soll.
        @type other: object
        @return: `True`, wenn das Objekt `other` auch eine Instanz der Klasse
        :class:`~password.Password` ist und die beiden Objekte im oben genannten Sinne
        gleich sind; andernfalls `False`.
        @rtype: bool
        """
        if self is other:
            return True
        return isinstance(other, self.__class__) and self.password == other.password

    def __hash__(self):
        """
        Gibt einen Hashwert für dieses Password-Objekt zurück.

        Der Hashwert wird anhand des in diesem Password-Objekt gespeicherten
        Password-Strings berechnet.

        @return: Den für dieses Password-Objekt berechneten Hashwert.
        @rtype: int
        """
        return hash(self.password)

