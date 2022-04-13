"""
Dieses Modul dient als Adapter einer Textdatei als Datenbank für das Verwalten von Nutzern und deren Tokens.
Classes:
    ServerAdapterFromPythonFilemanager: Diese Klasse stellt die Schnittstelle zwischen einer Textdatei und Python dar.
    Sie implementiert alle abstrakten Methoden der Elternklasse ServerAdapter.
Methods:
    validate_fileself.__path: Diese Methode stellt sicher, dass der Pfad der Datei gültig ist.
    __authenticate: Überprüft, ob ein gegebener Nutzer in der Datei vorkommt.
    check_token_exists: Überprüft, ob der Token in der Datei bereits existiert.
    add_token_to_user: Fügt einem Nutzer einen Token hinzu.
    delete_token_from_user: Löscht einen Token von einem Nutzer.
    delete_all_tokens_from_user: Löscht alle Tokens eines Nutzers.
    get_user: Gibt die Daten eines Nutzers zurück.
    get_all_valid_tokens: Gibt eine Liste aller validen Token zurück.
Attributes:
    self.__path: str: Ist der Pfad, unter dem die Datei zum Verwalten von Tokens existieren soll.
@author Lukas Wittenzellner
@version 1.0
"""
from RaspberryPi.src.data_model.key_token import AuthorizedNFCToken
from RaspberryPi.src.data_model.key_token import Token
from RaspberryPi.src.data_model.key_token import Identifier
from pathlib import Path
from RaspberryPi.src.door_controller.door_control_handler.user_list_updates_notifier import UserListUpdatesNotifier
from RaspberryPi.src.data_model.user import UnauthenticatedUser
from RaspberryPi.src.data_model.password import Password
from RaspberryPi.src.door_controller.server_adapter.server_adapter import ServerAdapter
from RaspberryPi.src.door_controller.entities.log import LogError, LogInfo
from RaspberryPi.src.data_model.configuration import PiConfiguration




class ServerAdapterFromPythonFilemanager(ServerAdapter):
    """
    ServerAdapterFromPythonFilemanager: Diese Klasse stellt die Schnittstelle zwischen einer Textdatei und Python dar.
    Sie implementiert alle abstrakten Methoden der Elternklasse ServerAdapter.
    """
    def __init__(self):
        self.__pi_conf = PiConfiguration()
        self.__path = self.__pi_conf.path_valid_tokens
        self.userListUpdateNotifier = UserListUpdatesNotifier()

    def validate_file_path(self) -> bool:
        """
        Überprüft, ob der in diesem Modul angegebene Pfad gültig ist und existiert.
        Falls eine Datei unter diesem Pfad noch nicht existiert, wird diese erstellt.

        :return: True, wenn die Datei existiert, anderenfalls wird False zurückgegeben.
        :rtype: bool.
        """
        token_file_path = Path(self.__path)

        if token_file_path:
            return True
        else:
            try:
                # erstellt die Datei unter dem Pfad
                file = open(token_file_path, "w")
                file.close()
                LogInfo.get_instance().send_log_msg("Es wurde eine Datei mit dem Pfad " + self.__path
                                                    + " erstellt")
                return True
            except FileNotFoundError:
                LogError.get_instance().send_log_msg(
                    "Fehler! Der Pfad zur Datei ist ungültig! Es existiert keine solche Datei oder Ordner: " +
                    self.__path)
            return False

    def __authenticate(self, user: UnauthenticatedUser, password: Password) -> bool:
        identifier = user.identifier.__repr__()

        with open(self.__path, "r") as f:
            lines = f.readlines()

        for line in lines:
            split_data = line.split(":")
            user_data = split_data[0].split(";")

            if (identifier == user_data[1]) & (password.password == user_data[2]):
                f.close()
                return True
        f.close()
        LogError.get_instance().send_log_msg("Authentifizierung des Admins fehlgeschlagen!")
        return False

    def __check_token_exists(self, token: Token) -> bool:
        """
        Überprüft, ob der Token in der Datei bereits existiert.
        :param token: Ist der Token, der überprüft werden soll.
        :type token:
        :return: True, wenn der Token in der Datei bereits existiert, anderenfalls False.
        :rtype: bool.
        """

        with open(self.__path, "r") as f:
            lines = f.readlines()

        for line in lines:
            line_split = line.split(":")
            tokens = line_split[1].split(";")
            for token_temp in tokens:
                if token_temp.strip() == str(token.identifier):
                    f.close()
                    return True
        f.close()
        return False

    def add_token_to_user(self, admin: UnauthenticatedUser, password: Password, user: UnauthenticatedUser,
                          user_token: Token):
        """
        Fügt einem Nutzer einen Token hinzu. Nur autorisierte Nutzer dürfen diese Operation ausführen.
        :param admin: Ist der Nutzer, der diese Methode durchführen möchte.
        :type admin: UnauthenticatedUser.
        :param password: Ist das Passwort des Admins
        :type password: Password
        :param user: Ist der Nutzer, dem ein Token hinzugefügt werden soll.
        :type user: UnauthenticatedUser.
        :param token: Ist der Token, der dem Nutzer hinzugefügt werden soll.
        :type token: Token.
        """
        # Überprüft, ob der admin autorisiert ist diese Operation auszuführen
        if not self.__authenticate(admin, password):
            return
        # Überprüft, ob der Token bereits existiert, um Doppelungen zu vermeiden
        if self.__check_token_exists(user_token):
            return
        # Ist der eindeutige Identifikator des gesuchten Nutzers
        identifier = str(user.identifier)

        # Ist der Token, der neu hinzugefügt werden soll
        new_token = str(user_token.identifier)

        with open(self.__path, "r") as f:
            lines = f.readlines()

        file = open(self.__path, "r")
        # Zählvariable der For-Schleife
        i = 0
        for token_str in file:
            # Bereitet den String vor, indem unnötige Zeichen entfernt werden
            token_str = token_str.strip()
            token_str = token_str.split(":")
            # Enthält nur die Nutzerdaten als Liste
            user_data = token_str[0].split(";")

            if user_data[1] == str(identifier):
                # Datei wird zum Lesen geschlossen, damit sie zum neu beschreiben geöffnet werden kann
                file.close()
                file = open(self.__path, "w")
                # Alle Nutzer und ihre Daten werden wieder unverändert hinzugefügt,
                # außer derjenige, der den neuen Token bekommen soll
                for j in range(len(lines)):
                    if j != i:
                        file.write(lines[j].strip() + "\n")
                # Der Nutzer mit dem neuen Token wird anschließens noch verändert hinzugefügt
                # Wenn der Nutzer noch keinen Token hatte:
                if token_str[1] == "":
                    file.write(lines[i].strip() + new_token)
                # Wenn der Nutzer bereits mindestens einen Token hatte
                else:
                    file.write(lines[i].strip() + ";" + new_token)

                file.close()
                break
            i = i + 1
        file.close()

    def delete_token_from_user(self, admin: UnauthenticatedUser, password: Password, user: UnauthenticatedUser,
                               token: Token):
        """
        Löscht einen Token von einem Nutzer. Nur autorisierte Nutzer dürfen diese Operation ausführen.
        :param admin: Ist der Nutzer, der diese Methode durchführen möchte.
        :type admin: UnauthenticatedUser.
        :param password: Ist das Passwort des Admins
        :type password: Password
        :param user: Ist der Nutzer, von dem ein Token geläscht werden soll.
        :type user: UnauthenticatedUser.
        :param token: Ist der Token, der gelöscht werden soll.
        :type token: Token.
        """

        if not self.__authenticate(admin, password):
            return

        identifier = str(user.identifier)
        token_to_delete = str(token.identifier)

        with open(self.__path, "r") as f:
            lines = f.readlines()

        file = open(self.__path, "r")

        i = 0
        for token_str in file:
            token_str = token_str.strip()
            token_str = token_str.split(":")
            user_data_str = token_str[0]  # speichert den String der Nutzerdaten
            top_list = token_str[1]  # speichert den String der Token
            user_data = user_data_str.split(";")  # aufgetrennter string der nutzerdaten

            # wenn in der Datei der identifier gleich der identifier des zu überprüfenden nutzers ist
            if user_data[1] == identifier:

                tokens = top_list.split(";")  # tokens ist nun Liste aller Tokens ohne ":" oder ";"
                token_found = False

                # speichert den neuen string der tokens
                tokens_temp_str = ""
                # schleife über alle tokens
                for token_t in tokens:
                    # alle tokens aus tokens werden einem neuen string hinzugefügt außer der zu löschende
                    if token_t != token_to_delete:
                        tokens_temp_str = token_t + ";" + tokens_temp_str
                    else:
                        token_found = True

                # nur jetzt muss die Datei angepasst werden, wenn token_found = True
                if token_found:
                    file.close()
                    # öffne file im schreibmodus => file ist nun leer
                    file = open(self.__path, "w")
                    for j in range(len(lines)):
                        # schreibe alle linien wieder in die Datei zurück außer die zu ändernde
                        if j != i:
                            # da nicht jede Zeile ein \n haben muss aber haben kann:
                            file.write(lines[j].strip() + file.newlines())

                    # Fügt den String der Nutzerdaten wieder zusammen
                    user_data_str = user_data_str + ":"

                    # wenn der zu löschende token der einzige in der Datei war, ist dieses if wahr
                    if tokens_temp_str == "":
                        file.write(user_data_str + "")

                    # ist nur wahr, wenn der Nutzer mindestens noch einen weiteren Token hatte.
                    # dann hat der neue string ein noch fehlerhaftes ";" am ende, das gelöscht werden muss
                    else:
                        tokens_temp_str = tokens_temp_str[:len(tokens_temp_str) - 1]
                        file.write(user_data_str + tokens_temp_str)

                file.close()
                break
            i = i + 1
        file.close()

    def delete_all_tokens_from_user(self, admin: UnauthenticatedUser, password: Password, user: UnauthenticatedUser):
        """
        Löscht alle Tokens eines Nutzers. Nur autorisierte Nutzer dürfen diese Operation ausführen.

        :param admin: Ist der Nutzer, der diese Methode durchführen möchte.
        :type admin: UnauthenticatedUser
        :param password: Ist das Passwort des Admins
        :type password: Password
        :param user: Ist der Nutzer, von dem alle Token gelöscht werden sollen.
        :type user: UnauthenticatedUser.
        """
        if not self.__authenticate(admin, password):
            return

            # Überprüft, ob der admin autorisiert ist diese Operation auszuführen
        if not self.__authenticate(admin, password):
            return
            # Ist der eindeutige Identifikator des gesuchten Nutzers
        identifier = str(user.identifier)

        with open(self.__path, "r") as f:
            lines = f.readlines()

        file = open(self.__path, "r")
        # Zählvariable der For-Schleife
        i = 0
        for token_str in file:
            # Bereitet den String vor, indem unnötige Zeichen entfernt werden
            token_str = token_str.strip()
            token_str = token_str.split(":")
            # Speichert den String der Nutzerdaten
            user_data_str = token_str[0]
            # Aufgetrennter string der nutzerdaten
            user_data = user_data_str.split(";")

            # Wenn in der Datei der identifier gleich der identifier des zu überprüfenden nutzers ist
            if user_data[1] == identifier:
                file.close()
                # Öffne Datei im schreibmodus => Datei ist nun leer
                file = open(self.__path, "w")
                for j in range(len(lines)):
                    # Schreibe alle Daten wieder in die Datei zurück außer die zu ändernde
                    if j != i:
                        # Da nicht jede Zeile ein \n haben muss aber haben kann:
                        file.write(lines[j].strip() + "\n")
                # Schreibt den Nutzer, dessen Daten gelöscht wurden, wieder in die Datei
                file.write(user_data_str + ":")
                file.close()
                break
            i = i + 1
        file.close()

    def get_user(self, admin: UnauthenticatedUser, password: Password, user: UnauthenticatedUser):
        """
        Gibt die Daten eines Nutzers zurück. Nur autorisierte Nutzer dürfen diese Operation ausführen.

        :param admin: Ist der Nutzer, der diese Methode durchführen möchte.
        :type admin: UnauthenticatedUser.
        :param password: Ist das Passwort des Admins.
        :type password: Password.
        :param user: Ist der Nutzer, dessen Daten zurückgegeben werden sollen.
        :type user: UnauthenticatedUser.
        :return: Den Nutzer und dessen Daten.
        """
        if not self.__authenticate(admin, password):
            return ""

        identifier = user.identifier.__repr__()

        with open(self.__path, "r") as f:
            lines = f.readlines()

        for line in lines:
            split = line.split(":")
            user_data = split[0].split(";")

            if user_data[1] == identifier:
                ret = line.strip("\n")
                f.close()
                return ret

        return ""

    def get_all_valid_tokens(self, admin: UnauthenticatedUser, password: Password) -> list:
        """
        Gibt eine Liste aller validen Token zurück. Nur autorisierte Nutzer dürfen diese Operation ausführen.

        :param admin: Ist der Nutzer, der diese Methode durchführen möchte.
        :type admin: UnauthenticatedUser.
        :param password: Ist das Passwort des Admins
        :type password: Password
        :return: Liste aller validen Tokens.
        :rtype: Liste von Tokens.
        """

        if not self.__authenticate(admin, password):
            return list()

        with open(self.__path, "r") as f:
            lines = f.readlines()
        # Liste, in die alle gefundenen Token gespeichert werden sollen
        token_list = list()
        # Iteriert durch alle Nutzer
        for line in lines:
            line_split = line.split(":")
            tokens_split = line_split[1].split(";")
            # Geht alle Token eines Nutzers durch und speichert diese in der Liste
            for tk in tokens_split:
                tk = tk.strip()
                if tk != "":
                    token_list.append(AuthorizedNFCToken(Identifier(tk)))
        return token_list