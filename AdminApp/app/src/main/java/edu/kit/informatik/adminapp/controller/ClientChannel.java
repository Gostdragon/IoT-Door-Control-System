package edu.kit.informatik.adminapp.controller;

import java.io.IOException;

/**
 * Dieses Interface beschreibt eine klientenseitige Verbindung über die Daten übertragen werden
 * können.
 *
 * @author Daniel Luckey
 * @version 1.0
 */
public interface ClientChannel extends AutoCloseable {
    /**
     * Stellt eine neue Verbindung zu einem Server her.
     * Falls bereits eine Verbindung besteht, wird eine neue Verbindung erstellt
     * und die alte Verbindung wird nicht geschlossen.
     *
     * @throws IOException  falls beim Herstellen der Verbindung ein Fehler auftritt
     */
    void connect() throws IOException;

    /**
     * Gibt zurück, ob eine Verbindung zum Server besteht.
     *
     *  @return  {@code true} falls eine Verbindung zum Server besteht
     */
    boolean isConnected();

    /**
     * Sendet eine Nachricht an den Server und gibt die Antwort vom Server zurück.
     *
     * @param message   die Nachricht
     * @return  die Antwort vom Server
     * @throws IOException  falls keine Verbindung zum Server besteht, oder
     *                      beim Senden ein Fehler auftritt
     */
    String send(final String message) throws IOException;

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
}