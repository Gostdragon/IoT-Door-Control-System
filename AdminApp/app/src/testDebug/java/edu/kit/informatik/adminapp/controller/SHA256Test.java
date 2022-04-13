package edu.kit.informatik.adminapp.controller;

import static org.junit.Assert.*;

import org.junit.Test;

import java.security.NoSuchAlgorithmException;

/**
 * Diese Klasse testet die Klasse {@link SHA256}.
 */
public class SHA256Test {
    private String[] originals = {
            "",
            "a",
            "avhVHAGHvghgvaghVHG",
            "1523751273",
            "()(())??)(//&!=?=!=?)!?/!%$/(!=(§)/=/!?§!)!/",
            "sabas HJBASBSA"
    };
    private String[] hashed = {
            "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
            "ca978112ca1bbdcafac231b39a23dc4da786eff8147c4e72b9807785afee48bb",
            "ee9ba3b2a9568a6072d7edcf0537b27500fc4490e6687cee784b829b27018735",
            "b0cd10d30876c1b2f570674510e389c92bc33fec6cd906ef61704ce942232a80",
            "7108b8c4d3451e924cbd80e19f76b7a30461583827b54a27bb5f56d8a3968393",
            "673d64c2fcc25ca092f0b2dc8e061a73d340706304c954a8094ba8530fa1d970"
    };
    private HashFunction hashFunction = new SHA256();

    /**
     * Testet die hash-Methode.
     */
    @Test
    public void hash() {
        for (int i = 0; i < Math.min(originals.length, hashed.length); i++) {
            try {
                assertEquals(hashed[i], hashFunction.hash(originals[i]));
            } catch (NoSuchAlgorithmException e) {
                fail();
            }
        }
    }
}