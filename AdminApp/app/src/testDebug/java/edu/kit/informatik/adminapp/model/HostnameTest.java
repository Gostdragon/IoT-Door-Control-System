package edu.kit.informatik.adminapp.model;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertThrows;
import static org.junit.Assert.assertTrue;

import org.junit.Test;

import edu.kit.informatik.adminapp.model.resources.Errors;

/**
 * Diese Klasse testet die Klasse {@link Hostname}.
 */
public class HostnameTest {
    private String[] validHostnames = {
            "192.168.111.111",
            "100.com",
            "hs.dd.com",
            "192.168.10.109",
            "127.0.1.1"
    };
    private String[] invalidHostnames = {
            null,
            "",
            "0123456789",
            "IP-REGEX",
            "Sample",
            "foo@demo.net",
            "bar.ba@test.co.uk",
            "256.168.111.1",
            "0.0.0.999",
            "1::1",
            "http://foo.co.uk/>><"
    };

    /**
     * Überprüft ob beim Erzeugen von Hostnamen mit invaliden Parametern eine Exception geworfen
     * wird.
     */
    @Test
    public void testInvalidHostname() {
        for (String invalidHostname : invalidHostnames) {
            Exception e = assertThrows(IllegalArgumentException.class,
                    () -> new Hostname(invalidHostname));
            assertEquals(String.format(Errors.REGEX_NOT_MATCHED, invalidHostname,
                    Hostname.REGEX_HOSTNAME), e.getMessage());
        }
    }

    /**
     * Überprüft ob beim erzeugen von Hostnamen mit validen Parametern
     * keine Exception geworfen wird.
     */
    @Test
    public void testValidHostname() {
        for (String validHostname : validHostnames) {
            new Hostname(validHostname);
        }
    }

    /**
     * Testet ob toString-Methode.
     */
    @Test
    public void testToString() {
        for (String validHostname : validHostnames) {
            Hostname hostname = new Hostname(validHostname);
            assertEquals(validHostname, hostname.toString());
        }
    }

    /**
     * Testet equals-Methode auf Reflexifität.
     */
    @Test
    public void testEquals_self() {
        Hostname hostname1 = new Hostname(validHostnames[0]);
        assertTrue(hostname1.equals(hostname1));
    }

    /**
     * Testet equals-Methode für zwei gleiche Objekte.
     */
    @Test
    public void equalsTest_same() {
        Hostname hostname1 = new Hostname(validHostnames[0]);
        Hostname hostname2 = new Hostname(validHostnames[0]);
        assertTrue(hostname1.equals(hostname2));
        assertTrue(hostname2.equals(hostname1));
    }

    /**
     * Testet equals-Methode für ein null-Objekt.
     */
    @Test
    public void equalsTest_null() {
        Hostname hostname1 = new Hostname(validHostnames[0]);
        assertFalse(hostname1.equals(null));
    }

    /**
     * Testet equals-Methode für zwei verschiedene Objekte.
     */
    @Test
    public void equalsTest_notEquals() {
        Hostname hostname1 = new Hostname(validHostnames[0]);
        Hostname hostname2 = new Hostname(validHostnames[1]);
        assertFalse(hostname1.equals(hostname2));
        assertFalse(hostname2.equals(hostname1));
    }

    /**
     * Testet hashCode-Methode
     */
    @Test
    public void testHashCode() {
        Hostname hostname1 = new Hostname(validHostnames[0]);
        Hostname hostname2 = new Hostname(validHostnames[0]);
        assertEquals(hostname1.hashCode(), hostname2.hashCode());
    }
}