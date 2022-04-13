package edu.kit.informatik.adminapp.model;

import android.os.Parcel;
import android.os.Parcelable;

import java.util.Objects;

import edu.kit.informatik.adminapp.model.resources.Errors;

/**
 * Diese Klasse stellt die Daten eines Tokens dar.
 */
public class TokenData implements Parcelable {
    /** Der Regex dem die Daten genügen müssen. */
    public static final String REGEX_TOKEN_DATA = ".*";
    /** Die Daten für ein leeres Token. */
    public static final String NO_DATA = "";
    /** Erstellt Instanzen der Klasse. */
    public static final Creator<TokenData> CREATOR = new Creator<TokenData>() {
        @Override
        public TokenData createFromParcel(Parcel in) {
            return new TokenData(in);
        }

        @Override
        public TokenData[] newArray(int size) {
            return new TokenData[size];
        }
    };

    private final String data;

    /**
     * Erstellt ein neues TokenData-Objekt mit Daten und prüft, ob {@code data} dem
     * {@link #REGEX_TOKEN_DATA Regex} genügt.
     *
     * @param data  die Daten des Tokens
     * @throws IllegalArgumentException falls {@code data} nciht dem {@link #REGEX_TOKEN_DATA Regex}
     * genügt
     */
    public TokenData(final String data) {
        if (data == null || !data.matches(REGEX_TOKEN_DATA)) {
            throw new IllegalArgumentException(
                    String.format(Errors.REGEX_NOT_MATCHED, data, REGEX_TOKEN_DATA));
        }
        this.data = data;
    }

    /**
     * Erstellt ein TokenData-Objekt ohne Daten.
     */
    public TokenData() {
        this(NO_DATA);
    }

    private TokenData(Parcel in) {
        this(in.readString());
    }

    /**
     * Gibt die Daten des Objekts zurück.
     *
     * @return die Daten des Objekts, {@link #NO_DATA} falls das Token keine Daten besitzt
     */
    public String getData() {
        return data;
    }

    @Override
    public int describeContents() {
        return 0;
    }

    @Override
    public void writeToParcel(final Parcel parcel, final int i) {
        parcel.writeString(this.data);
    }

    @Override
    public boolean equals(final Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        final TokenData tokenData = (TokenData) o;
        return data.equals(tokenData.data);
    }

    @Override
    public int hashCode() {
        return Objects.hashCode(data);
    }

    @Override
    public String toString() {
        return this.data;
    }
}
