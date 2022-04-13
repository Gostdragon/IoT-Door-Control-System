package edu.kit.informatik.adminapp.model;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertNotEquals;
import static org.junit.Assert.assertThrows;
import static org.junit.Assert.assertTrue;

import org.junit.Test;

import edu.kit.informatik.adminapp.model.resources.Errors;

/**
 * Diese Klasse testet die Klasse {@link Password}.
 */
public class PasswordTest {
    private String[] validPasswords = {
            "aksbasd",
            "&&!&/&/!)/&((=``",
            "21638712",
            "ASsahbda71263uas",
            "asiub 12n /(&"
    };
    private String[] invalidPasswords = {
            null,
            "kashbc$asu",
            "$ashb",
            "(!/$",
            "$"
    };

    /**
     * Testet, ob der das Erzeugen von validen Passwörtern möglich ist.
     */
    @Test
    public void testValidPassword() {
        for (String validPassword : validPasswords) {
            new Password(validPassword);
        }
    }

    /**
     * Testet, ob der das Erzeugen von invaliden Passwörtern möglich ist.
     */
    @Test
    public void testInvalidPassword() {
        for (String invalidPassword : invalidPasswords) {
            Exception e = assertThrows(IllegalArgumentException.class,
                    () -> new Password(invalidPassword));
            assertEquals(String.format(Errors.REGEX_NOT_MATCHED, invalidPassword,
                    Password.REGEX_PASSWORD), e.getMessage());
        }
    }

    /**
     * Testet die toString-Methode
     */
    @Test
    public void testToString() {
        for (String validPassword : validPasswords) {
            Password password = new Password(validPassword);
            assertEquals(validPassword, password.toString());
        }
    }

    /**
     * Testet equals-Methode auf Reflexifität.
     */
    @Test
    public void testEquals_self() {
        Password password1 = new Password(validPasswords[0]);
        assertTrue(password1.equals(password1));
    }

    /**
     * Testet equals-Methode für gleiche Passwörter.
     */
    @Test
    public void testEquals_same() {
        Password password1 = new Password(validPasswords[0]);
        Password password2 = new Password(validPasswords[0]);
        assertTrue(password1.equals(password2));
        assertTrue(password2.equals(password1));
    }

    /**
     * Testet equals-Methode für verschiedene Passwörter.
     */
    @Test
    public void testEquals_different() {
        Password password1 = new Password(validPasswords[0]);
        Password password2 = new Password(validPasswords[1]);
        assertFalse(password1.equals(password2));
        assertFalse(password2.equals(password1));
    }

    /**
     * Testet equals-Methode für null.
     */
    @Test
    public void testEquals_null() {
        Password password1 = new Password(validPasswords[0]);
        assertFalse(password1.equals(null));
    }

    /**
     * Testet ob zwei gleiche Objekte den gleichen Hashcode liefern.
     */
    @Test
    public void testHashCode_same() {
        Password password1 = new Password(validPasswords[0]);
        Password password2 = new Password(validPasswords[0]);
        assertEquals(password1.hashCode(), password2.hashCode());
    }

    /**
     * Testet ob zwei verschiedne Objekte verschiedene Hashcodes liefern.
     */
    @Test
    public void testHashCode_differnt() {
        Password password1 = new Password(validPasswords[0]);
        Password password2 = new Password(validPasswords[1]);
        assertNotEquals(password1.hashCode(), password2.hashCode());
    }
}