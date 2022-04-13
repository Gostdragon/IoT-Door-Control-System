package edu.kit.informatik.adminapp.model;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertNotEquals;
import static org.junit.Assert.assertThrows;
import static org.junit.Assert.assertTrue;

import org.junit.Test;

import edu.kit.informatik.adminapp.model.resources.Errors;

/**
 * Diese Klasse testet die Klasse {@link UserId}.
 */
public class UserIdTest {
    private String[] validUserIds = {
            "1",
            "bashjbcsa ajhsbcs",
            "&(!&(//=`",
            "as",
            ""
    };
    private String[] invalidUserIds = {
            "$",
            null,
            "asbj$HBhjbsa",
            "$bas",
            "2678$"
    };

    /**
     * Testet ob valide UserIds erstellt werden können.
     */
    @Test
    public void testValidUserId() {
        for (String validUserId : validUserIds) {
            new UserId(validUserId);
        }
    }

    /**
     * Testet ob invalide UserIds erstellt werden können.
     */
    @Test
    public void testInvalidUserId() {
        for (String invalidUserId : invalidUserIds) {
            Exception e = assertThrows(IllegalArgumentException.class,
                    () -> new UserId(invalidUserId));
            assertEquals(String.format(Errors.REGEX_NOT_MATCHED, invalidUserId,
                    UserId.REGEX_USER_ID), e.getMessage());
        }
    }

    /**
     * Testet die toString-Methode.
     */
    @Test
    public void testToString() {
        for (String validUserId : validUserIds) {
            UserId userId = new UserId(validUserId);
            assertEquals(validUserId, userId.toString());
        }
    }

    /**
     * Testet die equals-Methode auf Reflexivität.
     */
    @Test
    public void testEquals_self() {
        UserId userId1 = new UserId(validUserIds[0]);
        assertTrue(userId1.equals(userId1));
    }

    /**
     * Testet ob die equals-methode für zwei gleiche Objekte true liefert.
     */
    @Test
    public void testEquals_same() {
        UserId userId1 = new UserId(validUserIds[0]);
        UserId userId2 = new UserId(validUserIds[0]);
        assertTrue(userId1.equals(userId2));
        assertTrue(userId2.equals(userId1));
    }

    /**
     * Testet ob die equals-Methode für zwei verschieden Objekte false liefert.
     */
    @Test
    public void testEquals_different() {
        UserId userId1 = new UserId(validUserIds[0]);
        UserId userId2 = new UserId(validUserIds[1]);
        assertFalse(userId1.equals(userId2));
        assertFalse(userId2.equals(userId1));
    }

    /**
     * Testet die equals-Methode für null.
     */
    @Test
    public void testEquals_null() {
        UserId userId1 = new UserId(validUserIds[0]);
        assertFalse(userId1.equals(null));
    }

    /**
     * Testet ob zwei gleiche Objekte den selben Hashcode liefern.
     */
    @Test
    public void testHashCode_same() {
        UserId userId1 = new UserId(validUserIds[0]);
        UserId userId2 = new UserId(validUserIds[0]);
        assertEquals(userId1.hashCode(), userId2.hashCode());
    }

    /**
     * Testet ob zwei verschiedene Objekte veschiedene Hashcodes liefern.
     */
    @Test
    public void testHashCode_different() {
        UserId userId1 = new UserId(validUserIds[0]);
        UserId userId2 = new UserId(validUserIds[1]);
        assertNotEquals(userId1.hashCode(), userId2.hashCode());
    }
}