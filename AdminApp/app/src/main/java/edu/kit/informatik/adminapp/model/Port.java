package edu.kit.informatik.adminapp.model;

import android.os.Parcel;
import android.os.Parcelable;

import java.util.Objects;

import edu.kit.informatik.adminapp.model.resources.Errors;

/**
 * Diese Klasse stellt die Portnummer innerhalb eines Netzwerkes dar.
 *
 * @author Daniel Luckey
 * @version 1.0
 */
public class Port implements Parcelable {
    /**
     * Erstellt Instanzen der Klasse.
     */
    public static final Creator<Port> CREATOR = new Creator<Port>() {
        @Override
        public Port createFromParcel(final Parcel in) {
            return new Port(in);
        }

        @Override
        public Port[] newArray(final int size) {
            return new Port[size];
        }
    };
    private final int port;

    /**
     * Erstellt einen neuen Port.
     *
     * @param port  die Portnummer, muss &ge; 0 sein
     * @throws IllegalArgumentException falls {@code port} &lt; 0
     */
    public Port(final int port) {
        if (port < 0) {
            throw new IllegalArgumentException(String.format(Errors.NEGATIVE_NUMBER, port));
        }
        this.port = port;
    }

    private Port(final Parcel in) {
        this(in.readInt());
    }

    /**
     * Gibt eine Interger-Repräsentation des Ports zurück.
     *
     * @return  die Integer-Repräsentation des Ports
     */
    public int toInt() {
        return this.port;
    }

    @Override
    public int describeContents() {
        return 0;
    }

    @Override
    public void writeToParcel(final Parcel parcel, final int flag) {
        parcel.writeInt(this.port);
    }

    @Override
    public boolean equals(final Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        final Port port1 = (Port) o;
        return port == port1.port;
    }

    @Override
    public int hashCode() {
        return Objects.hash(port);
    }
}
