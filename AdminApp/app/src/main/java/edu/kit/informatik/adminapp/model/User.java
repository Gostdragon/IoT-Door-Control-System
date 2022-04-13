package edu.kit.informatik.adminapp.model;

import android.os.Parcel;
import android.os.Parcelable;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collection;
import java.util.Collections;
import java.util.HashSet;
import java.util.Objects;

/**
 * Diese Klasse stellt einen Nutzer dar, welcher einen Token besitzen kann.
 *
 * @author Daniel Luckey
 * @version 1.0
 */
public class User implements Parcelable {
    /**
     * Erstellt Instanzen der Klasse.
     */
    public static final Creator<User> CREATOR = new Creator<User>() {
        @Override
        public User createFromParcel(final Parcel in) {
            return new User(in);
        }

        @Override
        public User[] newArray(final int size) {
            return new User[size];
        }
    };

    private final Name name;
    private final UserId uid;
    private Collection<Token> tokens;

    /**
     * Erstellt einen neuen Nutzer.
     *
     * @param name  der Name des Nutzers
     * @param uid   die ID des Nutzers
     * @param tokens Tokens des Nutzers
     */
    public User(final Name name, final UserId uid, final Token... tokens) {
        this.name = name;
        this.uid = uid;
        this.tokens = new HashSet<>(Arrays.asList(tokens));
    }

    private User(final Parcel in) {
        this(
                in.readParcelable(Name.class.getClassLoader()),
                in.readParcelable(Name.class.getClassLoader()),
                in.createTypedArrayList(Token.CREATOR).toArray(new Token[0])
        );
    }

    /**
     * Gibt den Namen des Nutzers zurück.
     *
     * @return  der Name des Nutzers
     */
    public Name getName() {
        return this.name;
    }

    /**
     * Gibt die ID des Nutzers zurück.
     *
     * @return  die ID des Nutzers
     */
    public UserId getId() {
        return this.uid;
    }

    /**
     * Gibt die Tokens des Nutzers als nicht modifizierbare Collection zurück.
     *
     * @return  die Tokens des Nutzers
     */
    public Collection<Token> getTokens() {
        return Collections.unmodifiableCollection(this.tokens);
    }

    /**
     * Fügt dem Nutzer einen neuen Token hinzu.
     *
     * @param token der neue Token
     */
    public void add(final Token token) {
        this.tokens.add(token);
    }

    /**
     * Entfernt einen Token des Nutzers.
     * Entfernt keinen Token, falls der Nutzer den Token nicht besitzt.
     *
     * @param token der zu entfernende Token
     */
    public void remove(Token token) {
        this.tokens.remove(token);
    }

    /**
     * Entfernt alle Token von diesem Nutzer.
     */
    public void removeAllTokens() {
        this.tokens.clear();
    }

    @Override
    public int describeContents() {
        return 0;
    }

    @Override
    public void writeToParcel(final Parcel parcel, final int flag) {
        parcel.writeParcelable(this.name, flag);
        parcel.writeParcelable(this.uid, flag);
        parcel.writeTypedList(new ArrayList<>(this.tokens));
    }

    @Override
    public boolean equals(final Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        final User user = (User) o;
        return Objects.equals(getName(), user.getName()) && Objects.equals(uid, user.uid)
                && equals(getTokens(), user.getTokens());
    }

    private <T> boolean equals(Collection<T> col1, Collection<T> col2) {
        if (col1 == null && col2 != null) return true;
        if (col1 == null || col2 == null) return false;

        for (T t : col1) {
            if (!col2.contains(t)) return false;
        }
        for (T t : col2) {
            if (!col1.contains(t)) return false;
        }

        return true;
    }

    @Override
    public int hashCode() {
        return Objects.hash(getName(), uid, this.tokens);
    }

    @Override
    public String toString() {
        return this.name.toString();
    }
}
