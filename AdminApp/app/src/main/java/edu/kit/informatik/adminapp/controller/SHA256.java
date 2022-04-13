package edu.kit.informatik.adminapp.controller;

import android.os.Build;

import androidx.annotation.RequiresApi;

import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;

/**
 * Diese Klasse stellt eine Implementierung des SHA-256 Algorithmus zum Hashen von Zeichenketten
 * dar.
 *
 * Beachte: Die Methoden dieser Klasse  stammen von https://www.baeldung.com/sha-256-hashing-java.
 */
public class SHA256 implements HashFunction {
    private static final String HASH_NAME = "SHA-256";

    @Override
    @RequiresApi(api = Build.VERSION_CODES.KITKAT)
    public String hash(final String originalString) throws NoSuchAlgorithmException {
        final MessageDigest digest = MessageDigest.getInstance(HASH_NAME);
        final byte[] hashbytes = digest.digest(
                originalString.getBytes(StandardCharsets.UTF_8));
        return bytesToHex(hashbytes);
    }

    private static String bytesToHex(final byte[] hash) {
        final StringBuilder hexString = new StringBuilder(2 * hash.length);
        for (int i = 0; i < hash.length; i++) {
            final String hex = Integer.toHexString(0xff & hash[i]);
            if(hex.length() == 1) {
                hexString.append('0');
            }
            hexString.append(hex);
        }
        return hexString.toString();
    }
}
