package edu.kit.informatik.adminapp.controller.server;

import android.os.Parcel;

import java.io.IOException;
import java.util.Collection;
import java.util.LinkedList;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import edu.kit.informatik.adminapp.controller.ClientChannel;
import edu.kit.informatik.adminapp.controller.SSLClient;
import edu.kit.informatik.adminapp.model.Attribute;
import edu.kit.informatik.adminapp.model.Hostname;
import edu.kit.informatik.adminapp.model.Milliseconds;
import edu.kit.informatik.adminapp.model.Name;
import edu.kit.informatik.adminapp.model.Password;
import edu.kit.informatik.adminapp.model.Port;
import edu.kit.informatik.adminapp.model.Token;
import edu.kit.informatik.adminapp.model.TokenId;
import edu.kit.informatik.adminapp.model.User;
import edu.kit.informatik.adminapp.model.UserId;
import edu.kit.informatik.adminapp.model.resources.Errors;

/**
 * Diese Klasse stellt einen Adapter zu einem RaspberryPi welcher einen Server simuliert dar.
 *
 * @author Daniel Luckey
 * @version 1.0
 */
public class PiAdapter implements ServerAdapter {
    /** Erstellt Instanzen der Klasse. */
    public static final Creator<PiAdapter> CREATOR = new Creator<PiAdapter>() {
        @Override
        public PiAdapter createFromParcel(final Parcel in) {
            return new PiAdapter(in);
        }

        @Override
        public PiAdapter[] newArray(final int size) {
            return new PiAdapter[size];
        }
    };

    private static final String USER_SPLITTER = "\\$";
    private static final String REGEX_TOKEN = "[^;]+";
    private static final String REGEX_USER = "([^,]+),([^;]+);([^;]+);([^:]+):([^;]+(?:;[^;]+)*)?";
    private static final int LASTNAME_GROUP = 1;
    private static final int FIRSTNAME_GROUP = 2;
    private static final int UID_GROUP = 3;
    private static final int TOKENS_GROUP = 5;

    private static final String SEARCH_REQUEST_STRUCTURE = "search$%s$%s$%s";
    private static final String ADD_REQUEST_STRUCTURE = "addToken$%s$%s$%s$%s";
    private static final String DELETE_TOKEN_REQUEST_STRUCTURE = "deleteToken$%s$%s$%s$%s";
    private static final String DELETE_ALL_REQUEST_STRUCTURE = "deleteAll$%s$%s$%s";

    //base, attribute name werden von PiAdapter nicht berücksichtigt
    private static final String SEARCH_BASE = "";
    private static final String SEARCH_ATTRIBUTE_NAME = "";

    private static final String NAME_SEPARATOR = " "; //trennt Vor- und Nachname

    private Hostname hostname;
    private Port port;
    private Milliseconds timeout;
    private UserId uid;
    private Password password;
    private ClientChannel channel;

    /**
     * Erstellt einen neuen PiAdapter mit einer Nutzer-ID und einem Passwort.
     * Wird bei Anfragen an den Server der Timeout überschritten, so wird eine
     * {@link java.net.SocketTimeoutException Exception} ausgelöst. Ein Timeout von 0 wird als
     * unendlicher Timeout interpretiert.
     *
     * Es wird keine Verbindung zum Server hergestellt.
     * Es wird nicht geprüft, ob mit der Nutzer-ID und dem Passwort auf den Server zugegriffen
     * werden kann.
     *
     * @param hostname  der Hostname unter dem der Server erreichbar ist
     * @param port      der Port unter dem der Server erreichbar ist
     * @param timeout   der Timeout
     * @param uid       die Nutzer-ID mit dem auf den Server zugegriffen wird
     * @param password  das Passwort mit dem auf den Server zugegriffen wird
     */
    public PiAdapter(final Hostname hostname, final Port port, final Milliseconds timeout,
                     final UserId uid, final Password password) {
        this.hostname = hostname;
        this.port = port;
        this.timeout = timeout;
        this.uid = uid;
        this.password = password;
        this.channel = new SSLClient(this.hostname, this.port, this.timeout);
    }

    /**
     * Erstellt einen neuen PiAdapter ohne  Nutzer-ID und einem Passwort.
     * Wird bei Anfragen an den Server der Timeout überschritten, so wird eine
     * {@link java.net.SocketTimeoutException Exception} ausgelöst. Ein Timeout von 0 wird als
     * unendlicher Timeout interpretiert.
     *
     * Es wird keine Verbindung zum Server hergestellt.
     * Es wird nicht geprüft, ob mit der Nutzer-ID und dem Passwort auf den Server zugegriffen
     * werden kann.
     *
     * @param hostname  Der Hostname unter dem der Server erreichbar ist.
     * @param port      Der Port unter dem der Server erreichbar ist.
     * @param timeout   der Timeout
     */
    public PiAdapter(final Hostname hostname, final Port port, final Milliseconds timeout) {
        this(hostname, port, timeout, null, null);
    }

    private PiAdapter(final Parcel in) {
        this(
                in.readParcelable(Hostname.class.getClassLoader()),
                in.readParcelable(Port.class.getClassLoader()),
                in.readParcelable(Milliseconds.class.getClassLoader()),
                in.readParcelable(UserId.class.getClassLoader()),
                in.readParcelable(Password.class.getClassLoader())
        );
    }

    @Override
    public void set(UserId uid) {
        this.uid = uid;
    }

    @Override
    public void set(Password password) {
        this.password = password;
    }

    @Override
    public void connect() throws IOException {
        this.channel.connect();
    }

    @Override
    public boolean isConnected() {
        return this.channel.isConnected();
    }

    @Override
    public boolean isAuthenticated() throws IOException {
        if (this.uid == null || this.password == null) {
            return false;
        }

        Collection<User> result = search(SEARCH_BASE,
                new Attribute(SEARCH_ATTRIBUTE_NAME, this.uid.toString()));
        if (result == null || result.size() == 0) {
            return false;
        } else {
            return true;
        }
    }

    @Override
    public void close() throws IOException {
        this.channel.close();
    }

    @Override
    public boolean isClosed() {
        return this.channel.isClosed();
    }

    @Override
    public Collection<User> search(
            final String base, final Attribute... attributes) throws IOException {
        String users = this.channel.send(createSearchRequest(attributes));
        return extractUsers(users);
    }

    private Collection<User> extractUsers(final String result) {
        final Collection<User> users = new LinkedList<>();
        if (result == null) {
            return users;
        }

        for (final String userString : result.split(USER_SPLITTER)) {
            Matcher userMatcher = Pattern.compile(REGEX_USER).matcher(userString);

            if (userMatcher.matches()) {
                Name name = new Name(userMatcher.group(FIRSTNAME_GROUP) + NAME_SEPARATOR
                        + userMatcher.group(LASTNAME_GROUP));
                UserId uid = new UserId(userMatcher.group(UID_GROUP));
                User user = new User(name, uid);

                String tokens = userMatcher.group(TOKENS_GROUP);
                if (tokens != null) {
                    Matcher tokenMatcher = Pattern.compile(REGEX_TOKEN).matcher(tokens);
                    while (tokenMatcher.find()) {
                        Token token = new Token(new TokenId(tokenMatcher.group()));
                        user.add(token);
                    }
                }

                users.add(user);
            }
        }

        return users;
    }

    private String createSearchRequest(final Attribute[] attributes) {
        if (attributes.length != 1) {
            throw new IllegalArgumentException(
                    String.format(Errors.WRONG_NUMBER_SEARCH_ARGUMENTS, 1));
        }

        String adminId = this.uid.toString();
        String adminPassword = this.password.toString();
        String userId = attributes[0].getValue();
        String send = String.format(SEARCH_REQUEST_STRUCTURE, adminId, adminPassword, userId);
        return send;
    }

    /**
     * Fügt einen Token zu dem Nutzer in dem Server hinzu.
     * Falls der Token bereits für einen beliebigen Nutzer auf dem Server hinterlegt ist, wird der
     * Token nicht hinzugefügt und es wird keine Exception ausgelöst.
     *
     * @param user  der Nutzer
     * @param token der Token
     * @throws IOException  falls beim Hinzufügen ein Fehler auftritt
     */
    @Override
    public void addToken(User user, Token token) throws IOException {
        String addTokenRequest = String.format(ADD_REQUEST_STRUCTURE,
                this.uid, this.password, user.getId(), token.getId());
        this.channel.send(addTokenRequest);
    }

    @Override
    public void removeToken(User user, Token token) throws IOException {
        String deleteTokenRequest = String.format(DELETE_TOKEN_REQUEST_STRUCTURE,
                this.uid, this.password, user.getId(), token.getId());
        this.channel.send(deleteTokenRequest);
    }

    @Override
    public void removeAllTokens(final User user) throws IOException {
        String removeAllTokensRequest = String.format(DELETE_ALL_REQUEST_STRUCTURE,
                this.uid, this.password, user.getId());
        this.channel.send(removeAllTokensRequest);
    }

    @Override
    public int describeContents() {
        return 0;
    }

    @Override
    public void writeToParcel(final Parcel parcel, final int flag) {
        parcel.writeParcelable(this.hostname, flag);
        parcel.writeParcelable(this.port, flag);
        parcel.writeParcelable(this.timeout, flag);
        parcel.writeParcelable(this.uid, flag);
        parcel.writeParcelable(this.password, flag);
    }
}
