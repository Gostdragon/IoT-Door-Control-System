package edu.kit.informatik.adminapp.model;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertNotEquals;
import static org.junit.Assert.assertThrows;
import static org.junit.Assert.assertTrue;

import org.junit.Test;

import edu.kit.informatik.adminapp.model.resources.Errors;

/**
 * Diese Klasse testet die Klasse {@link Name}.
 */
public class NameTest {
    private String[] validNames = {
            "Max Mustermann",
            "",
            "Barack Obama"
    };
    private String[] invalidNames = {
            null,
            "$",
            "Mustermann$Max$1$passwort$token1$0c511be079e1da00d974571e4abe2899f4e0a19bbeb46ca72a7" +
                    "3058e7d1e981e",
            "Mustermann$",
            "$Mustermann"
    };

    /**
     * Testet ob der Name-Konstruktor valide Parameter akzeptiert.
     */
    @Test
    public void testValidName() {
        for (String validName : validNames) {
            new Name(validName);
        }
    }

    /**
     * Testet ob der Name-Konstruktur bei invaliden Parametern eine Exception wirft.
     */
    @Test
    public void testInvalidName() {
        for (String invalidName : invalidNames) {
            Exception e = assertThrows(IllegalArgumentException.class,
                    () -> new Name(invalidName));
            assertEquals(String.format(Errors.REGEX_NOT_MATCHED, invalidName, Name.REGEX_NAME),
                    e.getMessage());
        }
    }

    /**
     * Testet die toString-Methode.
     */
    @Test
    public void testToString() {
        for (String validName : validNames) {
            Name name = new Name(validName);
            assertEquals(validName, name.toString());
        }
    }

    /**
     * Testet equals-Methode auf Reflexifität.
     */
    @Test
    public void testEquals_self() {
        Name name = new Name(validNames[0]);
        assertTrue(name.equals(name));
    }

    /**
     * Testet equals-Methode für zwei gleiche Objekte.
     */
    @Test
    public void testEquals_same() {
        Name name1 = new Name(validNames[0]);
        Name name2 = new Name(validNames[0]);
        assertTrue(name1.equals(name2));
        assertTrue(name2.equals(name1));
    }

    /**
     * Testet equals-Methode für null.
     */
    @Test
    public void testEquals_null() {
        Name name1 = new Name(validNames[0]);
        assertFalse(name1.equals(null));
    }

    /**
     * Testet equals-Methode für zwei verschiedene Objekte.
     */
    @Test
    public void testEquals_different() {
        Name name1 = new Name(validNames[0]);
        Name name2 = new Name(validNames[1]);
        assertFalse(name1.equals(name2));
        assertFalse(name2.equals(name1));
    }

    /**
     * Tests ob zwei gleiche Objekte den selben Hashcode liefern.
     */
    @Test
    public void testHashCode_true() {
        Name name1 = new Name(validNames[0]);
        Name name2 = new Name(validNames[0]);
        assertEquals(name1.hashCode(), name2.hashCode());
    }

    /**
     * Tests ob zwei unterschiedliche Objekte unterschiedliche Hashcodes liefern.
     */
    @Test
    public void testHashCode_false() {
        Name name1 = new Name(validNames[0]);
        Name name2 = new Name(validNames[1]);
        assertNotEquals(name1.hashCode(), name2.hashCode());
    }
}