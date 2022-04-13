package edu.kit.informatik.adminapp.controller.server;

import android.os.Parcelable;

import java.io.IOException;
import java.util.Collection;

import edu.kit.informatik.adminapp.model.Attribute;
import edu.kit.informatik.adminapp.model.Password;
import edu.kit.informatik.adminapp.model.Token;
import edu.kit.informatik.adminapp.model.User;
import edu.kit.informatik.adminapp.model.UserId;

/**
 * Dieses Interface stellt eine Schnittstelle dar, über die mit einem Server kommuniziert
 * werden kann.
 *
 * @author Daniel Luckey
 * @version 1.0
 */
public interface ServerAdapter extends AutoCloseable, Parcelable {
    /**
     * Legt eine Nutzer-ID für den Zugriff auf den Server fest.
     *
     * @param uid   die NutzerId
     */
    void set(UserId uid);

    /**
     * Legt ein Passwort für den Zugriff auf den Server fest.
     *
     * @param password  das Passwort
     */
    void set(Password password);

    /**
     * Stellt eine Verbindung zum Server her.
     *
     * @throws IOException  falls beim Herstellen der Verbindung ein Fehler auftritt
     */
    void connect() throws IOException;

    /**
     * Gibt zurück, ob eine Verbindung zum Server besteht
     *
     * @return  {@code true} falls ob eine Verbindung zum Server besteht
     */
    boolean isConnected();

    /**
     * Schließt die Verbindung zum Server.
     *
     * @throws IOException  falls beim Schließen der Verbindung ein Fehler auftritt
     */
    void close() throws IOException;

    /**
     * Gibt zurück, ob {@link #close()} erfolgreich ausgeführt wurde.
     *
     * @return  {@code true} falls {@link #close()} erfolgreich ausgeführt wurde
     */
    boolean isClosed();

    /**
     * Prüft ob mit der Nutzer-ID und dem Passwort dieses PiAdapters Zugriff auf den Server besteht.
     * {@link #connect()} muss erfolgreich ausgeführt worden sein.
     *
     * @return  {@code true} falls Zugriff auf den Srver besteht, sonst {@code false}
     * @throws IOException  falls beim Prüfen des Zugriffs ein Fehler auftritt
     */
    boolean isAuthenticated() throws IOException;

    /**
     * Durchsucht jeden Eintrag unterhalb des angegebenen distinguished name, sowie den Eintrag
     * selbst nach den angegebene Attributen. Gibt eine Collection der Nutzer zurück, die allen
     * Attributen genügen.
     * Falls keine Zugriffsrechte auf den Server bestehen, wird eine leere Collection zurückgegeben.
     * {@link #connect()} muss erfolgreich aufgerufen worden sein.
     *
     * @param base          den distinguished name ab dem die Suche durchgeführt werden soll
     * @param attributes    die Attribute
     * @return              eine Collection der Nutzer die allen Attributen genügen
     * @throws IOException falls bei der Suche ein Fehler auftritt
     */
    Collection<User> search(
            final String base, final Attribute... attributes) throws IOException;

    /**
     * Fügt einen Token zu dem Nutzer in dem Server hinzu.
     * Falls keine Zugriffsrechte auf den Server bestehen, wird nichts getan.
     * {@link #connect()} muss erfolgreich aufgerufen worden sein.
     *
     * @param user  der Nutzer
     * @param token der Token
     * @throws IOException  falls beim Hinzufügen ein Fehler auftritt
     */
    void addToken(User user, Token token) throws IOException;

    /**
     * Entfernt ein Token von dem angegebenen Nutzer.
     * Entfernt kein Token, falls der Nutzer das Token nicht besitzt.
     * Falls keine Zugriffsrechte auf den Server bestehen, wird nichts getan.
     * {@link #connect()} muss erfolgreich aufgerufen worden sein.
     *
     * @param token das Token
     * @param user  der Nutzer
     * @throws IOException  falls beim Entfernen ein Fehler auftritt
     */
    void removeToken(User user, Token token) throws IOException;

    /**
     * Entfernt alle Token von dem Nutzer.
     * Falls keine Zugriffsrechte auf den Server bestehen, wird nichts getan.
     * {@link #connect()} muss erfolgreich aufgerufen worden sein.
     *
     * @param user  der Nutzer
     * @throws IOException  falls beim Entfernen der Token ein Fehler auftritt
     */
    void removeAllTokens(User user) throws IOException;
}