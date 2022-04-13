package edu.kit.informatik.adminapp.model;

import android.os.Parcel;
import android.os.Parcelable;

import java.util.Objects;

/**
 * Diese Klasse stellt ein Token mit einer ID dar, auf dem Daten gespeichert werden können.
 *
 * @author Daniel Luckey
 * @version 1.0
 */
public class Token implements Parcelable {
    /**
     * Erstellt Instanzen der Klasse.
     */
    public static final Creator<Token> CREATOR = new Creator<Token>() {
        @Override
        public Token createFromParcel(final Parcel in) {
            return new Token(in);
        }

        @Override
        public Token[] newArray(final int size) {
            return new Token[size];
        }
    };

    private final TokenId id;
    private final TokenData data;

    /**
     * Erstellt ein neues Token.
     *
     * @param id        die ID des Tokens, darf nicht {@code null} sein
     * @param data      die Daten des Tokens, darf nicht {@code null} sein
     */
    public Token(final TokenId id, final TokenData data) {
        if (id == null || data == null) {
            throw new NullPointerException();
        }

        this.id = id;
        this.data = data;
    }

    /**
     * Erstellt ein neues Token ohne Daten.
     *
     * @param id   die ID des Tokens, darf nicht {@code null} sein
     */
    public Token(final TokenId id) {
        this(id, new TokenData());
    }

    private Token(final Parcel in) {
        this(in.readParcelable(TokenId.class.getClassLoader()),
                in.readParcelable(TokenData.class.getClassLoader()));
    }

    /**
     * Gibt die Token-ID zurück.
     *
     * @return  die Token-ID
     */
    public TokenId getId() {
        return this.id;
    }

    /**
     * Gibt die Daten dieses Tokens zurück.
     *
     * @return  die Daten dieses Tokens
     */
    public TokenData getData() {
        return this.data;
    }

    @Override
    public int describeContents() {
        return 0;
    }

    @Override
    public void writeToParcel(final Parcel parcel, final int flag) {
        parcel.writeParcelable(this.id, flag);
        parcel.writeParcelable(this.data, flag);
    }

    @Override
    public boolean equals(final Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        final Token token = (Token) o;
        return id.equals(token.id) && getData().equals(token.getData());
    }

    @Override
    public int hashCode() {
        return Objects.hash(id, getData());
    }
}

