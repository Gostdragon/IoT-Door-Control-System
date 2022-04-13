package edu.kit.informatik.adminapp.model;

import java.util.Objects;

/**
 * Diese Klasse beschreibt ein Attribut in einer Datenbank.
 * Ein Attribut besteht aus einem Schlüssel und einem dazugehörigen Wert.
 *
 * @author Daniel Luckey
 * @version 1.0
 */
public class Attribute {
    private final String key;
    private String value;

    /**
     * Erstellt ein neues Attribut.
     *
     * @param key   der Schlüssel
     * @param value der Wert
     */
    public Attribute(final String key, final String value) {
        this.key = key;
        this.value = value;
    }

    /**
     * Gibt den Schlüssel zurück.
     *
     * @return  der Schlüssel
     */
    public String getKey() {
        return this.key;
    }

    /**
     * Gibt den Wert zurück.
     *
     * @return  der Wert
     */
    public String getValue() {
        return this.value;
    }

    /**
     * Setzt den Wert.
     *
     * @param value der neue Wert
     */
    public void setValue(final String value) {
        this.value = value;
    }

    @Override
    public boolean equals(final Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        final Attribute attribute = (Attribute) o;
        return Objects.equals(getKey(), attribute.getKey())
                && Objects.equals(getValue(), attribute.getValue());
    }

    @Override
    public int hashCode() {
        return Objects.hash(getKey(), getValue());
    }
}
