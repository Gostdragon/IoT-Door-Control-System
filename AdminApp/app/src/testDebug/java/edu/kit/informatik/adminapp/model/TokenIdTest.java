package edu.kit.informatik.adminapp.model;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertNotEquals;
import static org.junit.Assert.assertThrows;
import static org.junit.Assert.assertTrue;

import org.junit.Test;

import edu.kit.informatik.adminapp.model.resources.Errors;

/**
 * Diese Klasse testet die Klasse {@link TokenId}.
 */
public class TokenIdTest {
    private String[] validTokenIds = {
            "aksbasd",
            "&&!&/&/!)/&((=``",
            "21638712",
            "ASsahbda71263uas",
            "asiub 12n /(&"
    };
    private String[] invalidTokenIds = {
            null,
            "kashbc$asu",
            "$ashb",
            "(!/$",
            "$"
    };

    /**
     * Testet ob valide TokenIds erstellt werden können.
     */
    @Test
    public void testValidTokenId() {
        for (String validTokenId : validTokenIds) {
            new TokenId(validTokenId);
        }
    }

    /**
     * Testet ob invalide TokenIds erstellt werden können.
     */
    @Test
    public void testInvalidTokenId() {
        for (String invalidTokenId : invalidTokenIds) {
            Exception e = assertThrows(IllegalArgumentException.class,
                    () -> new TokenId(invalidTokenId));
            assertEquals(String.format(Errors.REGEX_NOT_MATCHED, invalidTokenId,
                    TokenId.REGEX_TOKEN_ID), e.getMessage());
        }
    }

    /**
     * Testet die toString-Methode.
     */
    @Test
    public void testToString() {
        for (String validTokenId : validTokenIds) {
            TokenId tokenId = new TokenId(validTokenId);
            assertEquals(validTokenId, tokenId.toString());
        }
    }

    /**
     * Testet die equals-methode auf Reflexifität.
     */
    @Test
    public void testEquals_self() {
        TokenId tokenId1 = new TokenId(validTokenIds[0]);
        assertTrue(tokenId1.equals(tokenId1));
    }

    /**
     * Testet die equals-Methode für zwei gleiche Objekte.
     */
    @Test
    public void testEquals_same() {
        TokenId tokenId1 = new TokenId(validTokenIds[0]);
        TokenId tokenId2 = new TokenId(validTokenIds[0]);
        assertTrue(tokenId1.equals(tokenId2));
        assertTrue(tokenId2.equals(tokenId1));
    }

    /**
     * Testet die equals-Methode für zwei verschiedene Objekte.
     */
    @Test
    public void testEquals_different() {
        TokenId tokenId1 = new TokenId(validTokenIds[0]);
        TokenId tokenId2 = new TokenId(validTokenIds[1]);
        assertFalse(tokenId1.equals(tokenId2));
        assertFalse(tokenId2.equals(tokenId1));
    }

    /**
     * Testet die equals-Methode für null.
     */
    @Test
    public void testEquals_null() {
        TokenId tokenId1 = new TokenId(validTokenIds[0]);
        assertFalse(tokenId1.equals(null));
    }

    /**
     * Testet ob zwei gleiche Objekte den gleichen Hashcode liefern.
     */
    @Test
    public void testHashCode_same() {
        TokenId tokenId1 = new TokenId(validTokenIds[0]);
        TokenId tokenId2 = new TokenId(validTokenIds[0]);
        assertEquals(tokenId1.hashCode(), tokenId2.hashCode());
    }

    /**
     * Testet ob zwei verschiedene Objekte verschiedene Hashcodes liefern.
     */
    @Test
    public void testHashCode_different() {
        TokenId tokenId1 = new TokenId(validTokenIds[0]);
        TokenId tokenId2 = new TokenId(validTokenIds[1]);
        assertNotEquals(tokenId1.hashCode(), tokenId2.hashCode());
    }
}