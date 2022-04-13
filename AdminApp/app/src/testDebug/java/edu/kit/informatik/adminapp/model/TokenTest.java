package edu.kit.informatik.adminapp.model;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertNotEquals;
import static org.junit.Assert.assertTrue;

import org.junit.Before;
import org.junit.Test;

/**
 * Diese Klasse testet die Klasse {@link Token}.
 */
public class TokenTest {
    private TokenId[] tokenIds = {
            new TokenId("aksbasd"),
            new TokenId("&&!&/&/!)/&((=``"),
            new TokenId("21638712"),
            new TokenId("ASsahbda71263uas"),
            new TokenId("asiub 12n /(&")
    };
    private TokenData[] data = {
            new TokenData("akjsnda"),
            new TokenData("as a s()/"),
            new TokenData("&/(!18762"),
            new TokenData("asd aksdahsbda JHASB"),
            new TokenData("")
    };
    private Token[] tokensWithData;
    private Token[] tokensWithoutData;

    /**
     * Initialisiert Tokens zum Testen.
     */
    @Before
    public void setUp() {
        this.tokensWithData = new Token[this.tokenIds.length];
        this.tokensWithoutData = new Token[this.tokenIds.length];
        for (int i = 0; i < this.tokensWithData.length; i++) {
            this.tokensWithData[i] = new Token(this.tokenIds[i], this.data[i]);
            this.tokensWithoutData[i] = new Token(this.tokenIds[i]);
        }
    }


    /**
     * Testet die methode {@link Token#getId()}.
     */
    @Test
    public void testGetId() {
        for (int i = 0; i < this.tokensWithData.length; i++) {
            assertEquals(this.tokenIds[i], tokensWithData[i].getId());
        }

        for (int i = 0; i < this.tokensWithoutData.length; i++) {
            assertEquals(this.tokenIds[i], tokensWithoutData[i].getId());
        }
    }

    /**
     * Testet die Methode {@link Token#getData()} für Token ohne Daten.
     */
    @Test
    public void testGetData() {
        for (int i = 0; i < this.tokensWithData.length; i++) {
            assertEquals(this.data[i], tokensWithData[i].getData());
        }
    }

    /**
     * Testet die Methode {@link Token#getData()} für Token mit Daten.
     */
    @Test
    public void testGetData_noData() {
        for (int i = 0; i < this.tokensWithData.length; i++) {
            assertEquals(new String(), tokensWithoutData[i].getData());
        }
    }

    /**
     * Testet die equals-Methode auf Reflexifität.
     */
    @Test
    public void testEquals_Self() {
        for (Token token : this.tokensWithData) {
            assertTrue(token.equals(token));
        }

        for (Token token : this.tokensWithoutData) {
            assertTrue(token.equals(token));
        }
    }

    /**
     * Testet equals-Methode für zwei gleiche Objekte.
     */
    @Test
    public void testEquals_Same() {
        Token token1 = new Token(this.tokenIds[0]);
        Token token2 = new Token(this.tokenIds[0]);
        assertTrue(token1.equals(token2));
        assertTrue(token2.equals(token1));

        Token token3 = new Token(this.tokenIds[0], this.data[0]);
        Token token4 = new Token(this.tokenIds[0], this.data[0]);
        assertTrue(token3.equals(token4));
        assertTrue(token4.equals(token3));
    }

    /**
     * Testet equals-Methode für zwei verschiedene Objekte.
     */
    @Test
    public void testEquals_different() {
        assertFalse(this.tokensWithData[0].equals(this.tokensWithData[1]));
        assertFalse(this.tokensWithData[1].equals(this.tokensWithData[0]));

        assertFalse(this.tokensWithoutData[0].equals(this.tokensWithoutData[1]));
        assertFalse(this.tokensWithoutData[1].equals(this.tokensWithoutData[0]));
    }

    /**
     * Testet equals-Methode für null.
     */
    @Test
    public void testEquals_null() {
        assertFalse(this.tokensWithoutData[0].equals(null));
        assertFalse(this.tokensWithData[0].equals(null));
    }

    /**
     * Testet ob zwei gleiche Objekte den selben Hashcode besitzen.
     */
    @Test
    public void testHashCode_same() {
        Token token1 = new Token(this.tokenIds[0], this.data[0]);
        Token token2 = new Token(this.tokenIds[0], this.data[0]);
        assertEquals(token1.hashCode(), token2.hashCode());

        Token token3 = new Token(this.tokenIds[0]);
        Token token4 = new Token(this.tokenIds[0]);
        assertEquals(token3.hashCode(), token4.hashCode());
    }

    /**
     * Testet ob zwei verschiedene Objekte unterschiedliche Hashcodes besitzen.
     */
    @Test
    public void testHashCode_different() {
        Token token1 = new Token(this.tokenIds[0], this.data[0]);
        Token token2 = new Token(this.tokenIds[1], this.data[1]);
        assertNotEquals(token1.hashCode(), token2.hashCode());

        Token token3 = new Token(this.tokenIds[0]);
        Token token4 = new Token(this.tokenIds[1]);
        assertNotEquals(token3.hashCode(), token4.hashCode());
    }
}