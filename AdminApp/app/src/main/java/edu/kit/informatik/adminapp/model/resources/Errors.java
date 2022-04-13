package edu.kit.informatik.adminapp.model.resources;

/**
 * Diese Klasse beinhaltet Error-Nachrichten für Klassen, die nicht auf die lokalen Resourcen der
 * App zugreifen können.
 */
public final class Errors {
    private Errors() {}

    /** Error-Nachricht für einen negativen Parameter. Format mit fehlerhaftem Parameter. */
    public static final String NEGATIVE_NUMBER = "'%d' should be >= 0";
    /** Error-Nachricht für einen Parameter der nicht dem erwarteten Regex entspricht.
     * Format mit Parameter und Regex. */
    public static final String REGEX_NOT_MATCHED = "'%s' does not match '%s'";
    /** Error-Nachricht für eine falsche Anzahl an Parametern für eine Suche. Format mit erwarteter
     * Anzahl an Parametern. */
    public static final String WRONG_NUMBER_SEARCH_ARGUMENTS
            = "can only search for '%d' arguments";
}
