package edu.kit.informatik.adminapp.model.resources;

import edu.kit.informatik.adminapp.model.User;
import edu.kit.informatik.adminapp.controller.server.ServerAdapter;

/**
 * Diese Klasse beinhaltet IDs welche zum identifizieren von Extras genutzt werden können,
 * die einem Intent übergeben werden.
 *
 *  @version 1.0
 *  @author Daniel Luckey
 */
public final class Extras {
    private Extras() {}

    /** Extra für einen {@link ServerAdapter}. */
    public static final String EXTRA_SERVER_ADAPTER = "edu.kit.informatik.EXTRA_SERVER";
    /** Extra für einen {@link User}. */
    public static final String EXTRA_USER = "edu.kit.informatik.EXTRA_USER";
}
