package edu.kit.informatik.adminapp.model;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertNotEquals;
import static org.junit.Assert.assertThrows;
import static org.junit.Assert.assertTrue;

import org.junit.Test;

import edu.kit.informatik.adminapp.model.resources.Errors;

/**
 * Diese Klasse testet die Klasse {@link Milliseconds}.
 */
public class MillisecondsTest {
    private int[] validMilliseconds = {0, 10891723, Integer.MAX_VALUE};
    private int[] invalidMilliseconds = {-1, -76123, Integer.MIN_VALUE};

    /**
     * Testet ob valide Milliseconds erzeugt werden können.
     */
    @Test
    public void testValidMilliseconds() {
        for (int validMilliseconds: validMilliseconds) {
            new Milliseconds(validMilliseconds);
        }
    }

    /**
     * Testet ob invalide Milliseconds erzeugt werden können.
     */
    @Test
    public void testInvalidMilliseconds() {
        for (int invalidMilliseconds : invalidMilliseconds) {
            Exception e = assertThrows(IllegalArgumentException.class,
                    () -> new Milliseconds(invalidMilliseconds));
            assertEquals(String.format(Errors.NEGATIVE_NUMBER, invalidMilliseconds), e.getMessage());
        }
    }

    /**
     * Testet die Methode asInt()
     */
    @Test
    public void testAsInt() {
        for (int validMilliseconds : validMilliseconds) {
            Milliseconds milliseconds = new Milliseconds(validMilliseconds);
            assertEquals(validMilliseconds, milliseconds.asInt());
        }
    }

    /**
     * Testet equals-Methode auf Reflexifität.
     */
    @Test
    public void testEquals_self() {
        Milliseconds milliseconds1 = new Milliseconds(validMilliseconds[0]);
        assertTrue(milliseconds1.equals(milliseconds1));
    }

    /**
     * Testet equals-Methode für zwei gleiche Objekte.
     */
    @Test
    public void testEquals_same() {
        Milliseconds milliseconds1 = new Milliseconds(validMilliseconds[0]);
        Milliseconds milliseconds2 = new Milliseconds(validMilliseconds[0]);
        assertTrue(milliseconds1.equals(milliseconds2));
        assertTrue(milliseconds2.equals(milliseconds1));
    }

    /**
     * Testet equals-Methode für zwei verschiedene Objekte.
     */
    @Test
    public void testEquals_different() {
        Milliseconds milliseconds1 = new Milliseconds(validMilliseconds[0]);
        Milliseconds milliseconds2 = new Milliseconds(validMilliseconds[1]);
        assertFalse(milliseconds1.equals(milliseconds2));
        assertFalse(milliseconds2.equals(milliseconds1));
    }

    /**
     * Testet equals-Methode für null.
     */
    @Test
    public void testEquals_null() {
        Milliseconds milliseconds1 = new Milliseconds(validMilliseconds[0]);
        assertFalse(milliseconds1.equals(null));
    }

    /**
     * Testet zwei gleiche Objekte den selben Hashcode besitzen.
     */
    @Test
    public void testHashCode_same() {
        Milliseconds milliseconds1 = new Milliseconds(validMilliseconds[0]);
        Milliseconds milliseconds2 = new Milliseconds(validMilliseconds[0]);
        assertEquals(milliseconds1.hashCode(), milliseconds2.hashCode());
    }

    /**
     * Testet ob zwei verschiedene Objekte unterschiedliche Hashcodes besitzen.
     */
    @Test
    public void testHashCode_different() {
        Milliseconds milliseconds1 = new Milliseconds(validMilliseconds[0]);
        Milliseconds milliseconds2 = new Milliseconds(validMilliseconds[1]);
        assertNotEquals(milliseconds1.hashCode(), milliseconds2.hashCode());
    }

    /**
     * Testet die toString-Methode.
     */
    @Test
    public void testToString() {
        for (int validMilliseconds : validMilliseconds) {
            Milliseconds milliseconds = new Milliseconds(validMilliseconds);
            assertEquals(String.valueOf(validMilliseconds), milliseconds.toString());
        }
    }
}