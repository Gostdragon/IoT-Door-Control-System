package edu.kit.informatik.adminapp.controller;

import java.security.NoSuchAlgorithmException;

/**
 * Dieses Interface stellt die Schnittstelle zu einer Hashfunktion dar.
 *
 * @author  Daniel Luckey
 * @version 1.0
 */
public interface HashFunction {
    /**
     * Gibt den gehashten Wert einer Zeichenkette zurück.
     *
     * @param originalString    die Zeichenkette die gehasht werden soll
     * @return  den Hashwert von {@code originalString}
     * @throws NoSuchAlgorithmException falls dieser Algorithmus auf der verwendeten
     * Plattform nicht verfügbar ist.
     */
    String hash(final String originalString) throws NoSuchAlgorithmException;
}
