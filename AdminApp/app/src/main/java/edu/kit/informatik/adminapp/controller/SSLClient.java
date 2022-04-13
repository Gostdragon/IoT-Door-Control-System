package edu.kit.informatik.adminapp.controller;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.InetSocketAddress;
import java.net.Socket;
import java.net.SocketTimeoutException;

import javax.net.SocketFactory;
import javax.net.ssl.SSLSocketFactory;

import edu.kit.informatik.adminapp.model.Hostname;
import edu.kit.informatik.adminapp.model.Milliseconds;
import edu.kit.informatik.adminapp.model.Port;

/**
 * Diese Klasse stellt eine clientenseitige SSL-Verbindung zwischen zwei Maschinen dar,
 * welche über Sockets bereitgestellt wird.
 *
 * @author Daniel Luckey
 * @version 1.0
 */
public class SSLClient implements ClientChannel {
    private static final SocketFactory SOCKET_FACTORY = SSLSocketFactory.getDefault();
    private static final int NO_TIMEOUT = 0;

    private final Hostname hostname;
    private final Port port;
    private final Milliseconds timeout;
    private Socket clientSocket;
    private PrintWriter writer;
    private BufferedReader reader;
    private boolean isClosed;

    /**
     * Erstellt einen neuen SSLSocketChannel mit einem Timeout.
     *
     * Es wird keine Verbindung hergestellt.
     * Wird bei {@link #connect()} oder {@link #send(String)} der Timeout überschritten, so wird
     * eine {@link SocketTimeoutException} ausgelöst. Ein Timeout von 0 wird als unendlicher Timeout
     * interpretiert.
     *
     * @param hostname  der Hostname des Servers
     * @param port      der Port des Servers
     * @param timeout   der Timeout in Millisekunden, muss &ge; 0 sein
     */
    public SSLClient(final Hostname hostname, final Port port, final Milliseconds timeout) {
        this.hostname = hostname;
        this.port = port;
        this.timeout = timeout;
        this.isClosed = false;
    }

    /**
     * Erstellt einen neuen SSLSocketChannel ohne Timeout.
     *
     * @param hostname  der Hostname des Servers
     * @param port      der Port des Servers
     */
    public SSLClient(final Hostname hostname, final Port port) {
        this(hostname, port, new Milliseconds(NO_TIMEOUT));
    }

    /**
     * Stellt eine Verbindung zu einem Server her.
     * Falls bereits eine Verbindung besteht, wird eine neue Verbindung erstellt
     * und die alte Verbindung wird nicht geschlossen.
     *
     * @throws IOException  falls beim Herstellen der Verbindung der Timeout überschritten wird,
     * oder ein anderer Fehler auftritt
     */
    @Override
    public void connect() throws IOException {
        //auch wenn connect() fehlschlägt, gilt der SSLSocketChannel als nicht closed
        this.isClosed = false;

        this.clientSocket = SOCKET_FACTORY.createSocket();
        this.clientSocket.connect(new InetSocketAddress(
                this.hostname.toString(), this.port.toInt()), this.timeout.asInt());
        this.clientSocket.setSoTimeout(this.timeout.asInt());
        this.writer = new PrintWriter(this.clientSocket.getOutputStream(), true);
        this.reader = new BufferedReader(new InputStreamReader(this.clientSocket.getInputStream()));
    }

    @Override
    public boolean isConnected() {
        boolean isConnected = true;
        try {
            send(new String());
        } catch (IOException e) {
            isConnected = false;
        }
        return isConnected;
    }

    /**
     * Sendet eine Nachricht an den Server und gibt die Antwort vom Server zurück.
     *
     * @param message   die Nachricht
     * @return  die Antwort vom Server
     * @throws IOException  falls keine Verbindung zum Server besteht,
     *                      beim Sender der Nachricht der Timeout überschritten wurde oder
     *                      beim Senden ein Fehler auftritt
     */
    @Override
    public String send(final String message) throws IOException {
        if (this.clientSocket == null ||this.reader == null || this.writer == null) {
            throw new IOException();
        }

        this.writer.println(message);
        String result = this.reader.readLine();

        if (result == null) {
            //Verbindung wurde unterbrochen
            throw new IOException();
        }
        return result;
    }

    @Override
    public void close() throws IOException {
        if (this.reader != null) this.reader.close();
        if (this.writer != null) this.writer.close();
        if (this.clientSocket != null) this.clientSocket.close();

        this.isClosed = true;
    }

    @Override
    public boolean isClosed() {
        return this.isClosed;
    }
}