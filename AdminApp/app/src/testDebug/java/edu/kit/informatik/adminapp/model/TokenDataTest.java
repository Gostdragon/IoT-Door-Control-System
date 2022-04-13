package edu.kit.informatik.adminapp.model;

import static org.junit.Assert.*;

import org.junit.Before;
import org.junit.Test;

/**
 * Diese Klasse testet die Klasse {@link TokenData}.
 */
public class TokenDataTest {
    private String[] tokenDataString = {
            "238175612",
            "!&(/)(!=(/!",
            "Data",
            "ASh HAGSah  ahsgd7aa7 ,",
            "HAGG aaagAg ",
            TokenData.NO_DATA

    };
    private TokenData[] tokenData;
    private TokenData[] tokenDataCopy;

    /**
     * Initialisiert Token-Daten zum Testen.
     */
    @Before
    public void setUp() {
        this.tokenData = new TokenData[this.tokenDataString.length];
        this.tokenDataCopy = new TokenData[this.tokenDataString.length];
        for (int i = 0; i < tokenData.length - 1; i++) {
            this.tokenData[i] = new TokenData(this.tokenDataString[i]);
            this.tokenDataCopy[i] = new TokenData(this.tokenDataString[i]);
        }
        this.tokenData[this.tokenData.length - 1] = new TokenData();
        this.tokenDataCopy[this.tokenDataCopy.length - 1] = new TokenData();
    }

    /**
     * Testet die Methode getData().
     */
    @Test
    public void testGetData() {
        for (int i = 0; i < this.tokenData.length; i++) {
            assertEquals(this.tokenDataString[i], this.tokenData[i].getData());
        }
    }

    /**
     * Testet die equals-Methode auf Reflexifität.
     */
    @Test
    public void testEquals_self() {
        for (TokenData data : this.tokenData) {
            assertTrue(data.equals(data));
        }
    }

    /**
     * Testet die equals-Methode für gleiche Objekte.
     */
    @Test
    public void testEquals_same() {
        for (int i = 0; i < this.tokenData.length; i++) {
            assertTrue(this.tokenData[i].equals(this.tokenDataCopy[i]));
        }
    }

    /**
     * Testet die equals-Methode für verschiedene Objekte.
     */
    @Test
    public void testEquals_different() {
        for (int i = 0; i < this.tokenData.length; i++) {
            for (int j = 0; j < this.tokenData.length; j++) {
                if (i != j) {
                    assertFalse(this.tokenData[i].equals(this.tokenDataCopy[j]));
                }
            }
        }
    }

    /**
     * Testet die equals-Methode für {@code null}.
     */
    @Test
    public void testEquals_null() {
        for (TokenData data : this.tokenData) {
            assertFalse(data.equals(null));
        }
    }

    /**
     * Testet die hashCode-Methode für gleiche Objekte.
     */
    @Test
    public void testHashCode_same() {
        for (int i = 0; i < this.tokenData.length; i++) {
            assertEquals(this.tokenData[i].hashCode(), this.tokenDataCopy[i].hashCode());
        }
    }

    /**
     * Testet die hashCode-methode für verschiedene Objekte.
     */
    @Test
    public void testHashCode_different() {
        for (int i = 0; i < this.tokenData.length; i++) {
            for (int j = 0; j < this.tokenData.length; j++) {
                if (i != j) {
                    assertNotEquals(this.tokenData[i].hashCode(), this.tokenDataCopy[j].hashCode());
                }
            }
        }
    }

    /**
     * Testet die toString-Methode.
     */
    @Test
    public void testToString() {
        for (int i = 0; i < this.tokenData.length; i++) {
            assertEquals(this.tokenDataString[i], this.tokenData[i].toString());
        }
    }
}