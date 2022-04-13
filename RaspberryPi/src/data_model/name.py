from RaspberryPi.src.exceptions.exception import SyntaxException

"""
Dieses Modul kapselt alle Klassen, die für die Modellierung von Nutzernamen 
im Türsteuerungssystem zuständig sind.
Nutzer sind in diesem Zusammenhang alle Personen, welche die durch das Steuerungssystem 
gesteuerte Tür benutzen.

Classes:
    FirstName: Repräsentiert den Vornamen eines Nutzers.
    LastName: Repräsentiert den Nachnamen eines Nutzers.
    Name: Repräsentiert den vollständigen Namen eines Nutzers bestehend 
          aus einem Vor- und einem Nachnamen.

@author Ahmad Eynawi
@version 03.03.2022
"""


class FirstName:
    """
    Diese Klasse kapselt den Vornamen eines Nutzers als String.

    Attributes:
        firstName (str): Der Vorname des Nutzers als String-Objekt.

    Methods:
        firstName: Gibt den Vornamen des Nutzers als String-Objekt zurück.
        __init__: Konstruktor der Klasse :class:`~name.FirstName`.
        __repr__: Gibt eine String-Repräsentation für dieses FirstName-Objekt zurück.
        __eq__: Vergleicht dieses FirstName-Objekt mit einem anderen Objekt.
        __hash__: Berechnet einen Hashwert für dieses FirstName-Objekt.
    """

    def __init__(self, firstName: str):
        """
        Konstruktor der Klasse :class:`~name.FirstName`.

        Erstellt und initialisiert einen Vornamen.
        Beachte, dass der Vorname keine Ziffern oder Sonderzeichen enthalten darf.

        @param firstName: Der Vorname, der in einem FirstName-Objekt gekapselt werden muss.
        @type firstName: str

        @raise:
            SyntaxException: Wenn der als Parameter übergebene String leer ist
                             oder nicht-alphabetische Zeichen enthält.
        """
        if firstName.isalpha():
            self.__firstName = firstName
        elif firstName == "":
            raise SyntaxException("Der Vorname muss mindestens einen Buchstaben enthalten!")
        else:
            raise SyntaxException("Der Vorname darf nur aus Buchstaben bestehen!")

    @property
    def firstName(self):
        """
        Get-Methode für den in diesem FirstName-Objekt gekapselten Vornamen.

        @return: Den in diesem FirstName-Objekt gespeicherten Vornamen als String.
        @rtype: str
        """
        return self.__firstName

    def __repr__(self):
        """
        Erzeugt eine textuelle Darstellung für dieses FirstName-Objekt und gibt diese
        Darstellung als String zurück.

        @return: Die String-Repräsentation dieses FirstName-Objekts.
        @rtype: str
        """
        return f"{self.__firstName}"

    def __eq__(self, other: object):
        """
        Vergleicht dieses FirstName-Objekt mit dem Objekt `other`.

        Zwei FirstName-Objekte werden als gleich betrachtet, wenn sie den gleichen
        Vornamen speichern.

        @param other: Das Objekt, das mit diesem FirstName-Objekt verglichen werden soll.
        @type other: object
        @return: `True`, wenn das Objekt `other` auch eine Instanz der Klasse
                 :class:`~name.FirstName` ist und die beiden Objekte im oben genannten Sinne
                 gleich sind; andernfalls `False`.
        @rtype: bool
        """
        if self is other:
            return True
        return isinstance(other, self.__class__) and self.firstName == other.firstName

    def __hash__(self):
        """
        Gibt einen Hashwert für dieses FirstName-Objekt zurück.

        Der Hashwert wird anhand des FirstName-Strings berechnet, der in diesem
        FirstName-Objekt gespeichert ist.

        @return: Den für dieses FirstName-Objekt berechneten Hashwert.
        @rtype: int
        """
        return hash(self.firstName)


class LastName:
    """
    Diese Klasse kapselt den Nachnamen eines Nutzers als String.

    Attributes:
        lastName (str): Der Nachname des Nutzers als String-Objekt.

    Methods:
        lastName: Gibt den Nachnamen des Nutzers als String-Objekt zurück.
        __init__: Konstruktor der Klasse :class:`~name.LastName`.
        __repr__: Gibt eine String-Repräsentation für dieses LastName-Objekt zurück.
        __eq__: Vergleicht dieses LastName-Objekt mit einem anderen Objekt.
        __hash__: Berechnet einen Hashwert für dieses LastName-Objekt.
    """

    def __init__(self, lastName: str):
        """
        Konstruktor der Klasse :class:`~name.LastName`.

        Erstellt und initialisiert einen Nachnamen.
        Beachte, dass der Nachname keine Ziffern oder Sonderzeichen enthalten darf.

        @param lastName: Der Nachname, der in einem LastName-Objekt gekapselt werden muss.
        @type lastName: str

        @raise:
            SyntaxException: Wenn der als Parameter übergebene String leer ist
                             oder nicht-alphabetische Zeichen enthält.
        """
        if lastName.isalpha():
            self.__lastName = lastName
        elif lastName == "":
            raise SyntaxException("Der Nachname muss mindestens einen Buchstaben enthalten!")
        else:
            raise SyntaxException("Der Nachname darf nur aus Buchstaben bestehen!")

    @property
    def lastName(self):
        """
        Get-Methode für den in diesem LastName-Objekt gekapselten Nachnamen.

        @return: Den in diesem LastName-Objekt gespeicherten Nachnamen als String.
        @rtype: str
        """
        return self.__lastName

    def __repr__(self):
        """
        Erzeugt eine textuelle Darstellung für dieses LastName-Objekt und gibt diese
        Darstellung als String zurück.

        @return: Die String-Repräsentation dieses LastName-Objekts.
        @rtype: str
        """
        return f"{self.__lastName}"

    def __eq__(self, other: object):
        """
        Vergleicht dieses LastName-Objekt mit dem Objekt `other`.

        Zwei LastName-Objekte werden als gleich betrachtet, wenn sie den gleichen
        Nachnamen speichern.

        @param other: Das Objekt, das mit diesem LastName-Objekt verglichen werden soll.
        @type other: object
        @return: `True`, wenn das Objekt `other` auch eine Instanz der Klasse
                 :class:`~name.LastName` ist und die beiden Objekte im oben genannten Sinne
                 gleich sind; andernfalls `False`.
        @rtype: bool
        """
        if self is other:
            return True
        return isinstance(other, self.__class__) and self.lastName == other.lastName

    def __hash__(self):
        """
        Gibt einen Hashwert für dieses LastName-Objekt zurück.

        Der Hashwert wird anhand des Nachnamen berechnet, der in diesem
        LastName-Objekt gespeichert ist.

        @return: Den für dieses LastName-Objekt berechneten Hashwert.
        @rtype: int
        """
        return hash(self.lastName)


class Name:
    """
    Diese Klasse kapselt den vollständigen Namen eines Nutzers. Dieser Name besteht aus
    einem Vor- und einem Nachnamen.

    Attributes:
        firstName (:class:`~name.FirstName`): Der Vorname des Nutzers als FirstName-Objekt.
        lastName (:class:`~name.LastName`): Der Nachname des Nutzers als LastName-Objekt.

    Methods:
        firstName: Gibt den Vornamen des Nutzers als FirstName-Objekt zurück.
        lastName: Gibt den Nachnamen des Nutzers als LastName-Objekt zurück.
        __init__: Konstruktor der Klasse :class:`~name.Name`.
        __repr__: Gibt eine String-Repräsentation für dieses Name-Objekt zurück.
        __eq__: Vergleicht dieses Name-Objekt mit einem anderen Objekt.
        __hash__: Berechnet einen Hashwert für dieses Name-Objekt.
    """

    def __init__(self, firstName: FirstName, lastName: LastName):
        """
        Konstruktor der Klasse :class:`~name.Name`.

        Erstellt und initialisiert einen vollständigen Namen bestehend
        aus einem Vor- und einem Nachnamen.
        Beachte, dass der Name keine Ziffern oder Sonderzeichen enthalten darf.

        @param firstName: Der Vorname des Nutzers.
        @type firstName: :class:`~name.FirstName`
        @param lastName: Der Nachname des Nutzers.
        @type lastName: :class:`~name.LastName`
        """
        self.__firstName = firstName
        self.__lastName = lastName

    @property
    def firstName(self):
        """
        Get-Methode für den in diesem Name-Objekt gespeicherten Vornamen.

        @return: Den Vornamen des Nutzers.
        @rtype: :class:`~name.FirstName`
        """
        return self.__firstName

    @property
    def lastName(self):
        """
        Get-Methode für den in diesem Name-Objekt gespeicherten Nachnamen.

        @return: Den Nachnamen des Nutzers.
        @rtype: :class:`~name.LastName`
        """
        return self.__lastName

    def __repr__(self):
        """
        Erzeugt eine textuelle Darstellung für dieses Name-Objekt und gibt diese
        Darstellung als String zurück.

        @return: Die String-Repräsentation dieses Name-Objekts bestehend
                 aus dem Vor- und dem Nachnamen.
        @rtype: str
        """
        return f"{self.__firstName} {self.__lastName}"

    def __eq__(self, other: object):
        """
        Vergleicht dieses Name-Objekt mit dem Objekt `other`.

        Zwei Name-Objekte werden als gleich betrachtet, wenn sie den gleichen
        Vornamen und den gleichen Nachnamen speichern.

        @param other: Das Objekt, das mit diesem Name-Objekt verglichen werden soll.
        @type other: object
        @return: `True`, wenn das Objekt `other` auch eine Instanz der Klasse
                 :class:`~name.Name` ist und die beiden Objekte im oben genannten Sinne
                 gleich sind; andernfalls `False`.
        @rtype: bool
        """
        if self is other:
            return True
        return isinstance(other, self.__class__) and self.firstName == other.firstName \
               and self.lastName == other.lastName

    def __hash__(self):
        """
        Gibt einen Hashwert für dieses Name-Objekt zurück.

        Der Hashwert wird anhand des Vor- und Nachnamen berechnet, die in diesem
        Name-Objekt gespeichert sind.

        @return: Den für dieses Name-Objekt berechneten Hashwert.
        @rtype: int
        """
        return hash((self.firstName, self.lastName))
