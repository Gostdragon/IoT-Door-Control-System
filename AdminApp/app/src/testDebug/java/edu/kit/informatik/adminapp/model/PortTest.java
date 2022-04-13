package edu.kit.informatik.adminapp.model;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertNotEquals;
import static org.junit.Assert.assertThrows;
import static org.junit.Assert.assertTrue;

import org.junit.Test;

import edu.kit.informatik.adminapp.model.resources.Errors;

/**
 * Diese Klasse testet die Klasse {@link Port}.
 */
public class PortTest {
    private int[] validPorts = {0, 10891723, Integer.MAX_VALUE};
    private int[] invalidPorts = {-1, -76123, Integer.MIN_VALUE};

    /**
     * Testet ob valide Ports erzeugt werden können.
     */
    @Test
    public void testValidPort() {
        for (int validPort: validPorts) {
            new Port(validPort);
        }
    }

    /**
     * Testet ob invalide Ports erzeugt werden können.
     */
    @Test
    public void testInvalidPort() {
        for (int invalidPort : invalidPorts) {
            Exception e = assertThrows(IllegalArgumentException.class,
                    () -> new Port(invalidPort));
            assertEquals(String.format(Errors.NEGATIVE_NUMBER, invalidPort), e.getMessage());
        }
    }

    /**
     * Testet die Methode toInt()
     */
    @Test
    public void testToInt() {
        for (int validPort : validPorts) {
            Port port = new Port(validPort);
            assertEquals(validPort, port.toInt());
        }
    }

    /**
     * Testet equals-Methode auf Reflexifität.
     */
    @Test
    public void testEquals_self() {
        Port port1 = new Port(validPorts[0]);
        assertTrue(port1.equals(port1));
    }

    /**
     * Testet equals-Methode für zwei gleiche Objekte.
     */
    @Test
    public void testEquals_same() {
        Port port1 = new Port(validPorts[0]);
        Port port2 = new Port(validPorts[0]);
        assertTrue(port1.equals(port2));
        assertTrue(port2.equals(port1));
    }

    /**
     * Testet equals-Methode für zwei verschiedene Objekte.
     */
    @Test
    public void testEquals_different() {
        Port port1 = new Port(validPorts[0]);
        Port port2 = new Port(validPorts[1]);
        assertFalse(port1.equals(port2));
        assertFalse(port2.equals(port1));
    }

    /**
     * Testet equals-Methode für null.
     */
    @Test
    public void testEquals_null() {
        Port port1 = new Port(validPorts[0]);
        assertFalse(port1.equals(null));
    }

    /**
     * Testet ob zwei gleiche Objekte den selben Hashcode besitzen.
     */
    @Test
    public void testHashCode_same() {
        Port port1 = new Port(validPorts[0]);
        Port port2 = new Port(validPorts[0]);
        assertEquals(port1.hashCode(), port2.hashCode());
    }

    /**
     * Testet ob zwei verschiedene Objekte unterschiedliche Hashcodes besitzen.
     */
    @Test
    public void testHashCode_different() {
        Port port1 = new Port(validPorts[0]);
        Port port2 = new Port(validPorts[1]);
        assertNotEquals(port1.hashCode(), port2.hashCode());
    }
}