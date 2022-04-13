package edu.kit.informatik.adminapp.model;

import android.os.Parcel;
import android.os.Parcelable;

import java.util.Objects;

import edu.kit.informatik.adminapp.model.resources.Errors;

/**
 * Diese Klasse stellt die ID eines Nutzers dar.
 *
 * @author Daniel Luckey
 * @version 1.0
 */
public class UserId implements Parcelable {
    /**
     * Der Regex welcher die Nutzer-ID genügen muss.
     */
    public static final String REGEX_USER_ID = "[^$]*";
    /**
     * Erstellt Instanzen der Klasse.
     */
    public static final Creator<UserId> CREATOR = new Creator<UserId>() {
        @Override
        public UserId createFromParcel(final Parcel in) {
            return new UserId(in);
        }

        @Override
        public UserId[] newArray(final int size) {
            return new UserId[size];
        }
    };

    private final String uid;

    /**
     * Erstellt eine neue Nutzer-ID und überprüft, ob diese dem {@link #REGEX_USER_ID Regex} genügt.
     *
     * @param uid   die Nutzer-ID
     * @throws IllegalArgumentException falls {@code uid} nicht dem {@link #REGEX_USER_ID Regex}
     * genügt
     */
    public UserId(final String uid) {
        if (uid == null || !uid.matches(REGEX_USER_ID)) {
            throw new IllegalArgumentException(
                    String.format(Errors.REGEX_NOT_MATCHED, uid, REGEX_USER_ID));
        }
        this.uid = uid;
    }

    private UserId(final Parcel in) {
        this(in.readString());
    }

    @Override
    public void writeToParcel(final Parcel dest, final int flags) {
        dest.writeString(this.uid);
    }

    @Override
    public int describeContents() {
        return 0;
    }

    @Override
    public String toString() {
        return this.uid;
    }

    @Override
    public boolean equals(final Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        final UserId userId = (UserId) o;
        return uid.equals(userId.uid);
    }

    @Override
    public int hashCode() {
        return Objects.hash(uid);
    }
}
