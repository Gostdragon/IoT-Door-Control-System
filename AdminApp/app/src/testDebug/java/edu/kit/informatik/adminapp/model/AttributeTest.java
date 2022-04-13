package edu.kit.informatik.adminapp.model;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertNull;
import static org.junit.Assert.assertTrue;

import org.junit.Test;

/**
 * Diese Klasse testet die Klasse {@link Attribute}.
 */
public class AttributeTest {
    private Attribute attribute1;
    private Attribute attribute2;
    private String key1 = "key1";
    private String value1 = "value1";
    private String key2 = "key2";
    private String value2 = "value2";

    /**
     * Testet die getKey-Methode für ein Attribute mit Key {@code null}.
     */
    @Test
    public void testGetKey_null() {
        this.attribute1 = new Attribute(null, null);
        assertNull(attribute1.getKey());
    }

    /**
     * Testet die getKey-Methode für ein Attribut mit leerem Key.
     */
    @Test
    public void testGetKey_empty() {
        this.attribute1 = new Attribute("", "");
        assertEquals("", this.attribute1.getKey());
    }

    /**
     * Testet die getKey-Methode für ein Attribut mit nicht-leerem Key.
     */
    @Test
    public void testGetKey_notEmpty() {
        this.attribute1 = new Attribute(key1, value1);
        assertEquals(key1, this.attribute1.getKey());
    }

    /**
     * Testet die getValue-Methode für ein Attribut mit Key {@code null}.
     */
    @Test
    public void testGetValue_null() {
        this.attribute1 = new Attribute(null, null);
        assertNull(attribute1.getValue());
    }

    /**
     * Testet die getValue-Methode für ein Attribut mit leerem Key.
     */
    @Test
    public void testGetValue_empty() {
        this.attribute1 = new Attribute("", "");
        assertEquals("", this.attribute1.getValue());
    }

    /**
     * Testet die getValue-Methode für ein Attribut mit nicht-leerem Key.
     */
    @Test
    public void testGetValue_notEmpty() {
        this.attribute1 = new Attribute(key1, value1);
        assertEquals(value1, this.attribute1.getValue());
    }

    /**
     * Testet die equals-Methode auf Reflexivität.
     */
    @Test
    public void testEquals_self() {
        attribute1 = new Attribute(key1, value1);
        assertTrue(attribute1.equals(attribute1));
    }

    /**
     * Testet die equals-Methode für null.
     */
    @Test
    public void testEquals_null() {
        attribute1 = new Attribute(key1, value1);
        assertFalse(attribute1.equals(null));
    }

    /**
     * Testet die equals-Methode für verschiedene Objekte.
     */
    @Test
    public void testEquals_different() {
        attribute1 = new Attribute(key1, value1);
        attribute2 = new Attribute(key2, value2);
        assertFalse(attribute1.equals(attribute2));
        assertFalse(attribute2.equals(attribute1));
    }

    /**
     * Testet die HashCode-Methode.
     */
    @Test
    public void testHashCode() {
        attribute1 = new Attribute(key1, value1);
        attribute2 = new Attribute(key1, value1);
        assertEquals(attribute1.hashCode(), attribute2.hashCode());
    }
}