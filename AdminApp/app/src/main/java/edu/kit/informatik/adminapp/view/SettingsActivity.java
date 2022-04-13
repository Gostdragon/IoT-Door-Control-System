package edu.kit.informatik.adminapp.view;

import android.os.Bundle;
import android.view.MenuItem;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.appcompat.app.ActionBar;
import androidx.appcompat.app.AppCompatActivity;
import androidx.preference.EditTextPreference;
import androidx.preference.Preference;
import androidx.preference.Preference.SummaryProvider;
import androidx.preference.PreferenceFragmentCompat;

import edu.kit.informatik.adminapp.R;
import edu.kit.informatik.adminapp.model.Hostname;
import edu.kit.informatik.adminapp.model.Milliseconds;
import edu.kit.informatik.adminapp.model.Port;

/**
 * Diese Klasse stellt eine Aktivität zum Anpassen der Einstellungen dar.
 *
 * @author Daniel Luckey
 * @version 1.0
 */
public class SettingsActivity extends AppCompatActivity {

    /**
     * Lädt das UI.
     *
     * @param savedInstanceState    beinhaltet den Status einer früheren gespeicherten Aktivität,
     *                              {@code null} falls die Aktivität noch nie verlassen wurde
     */
    @Override
    protected void onCreate(@Nullable final Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_settings);

        getSupportFragmentManager()
                .beginTransaction()
                .replace(R.id.activity_settings_fl_settings_container, new SettingsFragment())
                .commit();

        //aktiviert den Home-Knopf in der Symbolleiste
        ActionBar actionBar = getSupportActionBar();
        if (actionBar != null) {
            actionBar.setDisplayHomeAsUpEnabled(true);
        }
    }

    /**
     * Beendet diese Aktivität, falls der Home-Knopf in der Symbolleiste geklickt wird.
     *
     * @param item  das MenuItem das geklickt wurde
     * @return      {@code true}
     */
    @Override
    public boolean onOptionsItemSelected(@NonNull final MenuItem item) {
        if (item.getItemId() == android.R.id.home) {
            finish();
            return true;
        }
        return super.onOptionsItemSelected(item);
    }

    /**
     * Dieses Klasse lädt das Fragment aus dem die Settings-Aktivität besteht.
     */
    public static class SettingsFragment extends PreferenceFragmentCompat {

        /**
         * Lädt die Preference-Elemente dieses Fragments.
         *
         * @param savedInstanceState    beinhaltet den Status eines früher gespeicherten Fragments,
         *                              {@code null} falls das Fragment noch nie verlassen wurde
         * @param rootKey               der Schlüssel der als Wurzel der Einstellungshierarchie
         *                              verwendet werden soll
         */
        @Override
        public void onCreatePreferences(final Bundle savedInstanceState,
                                        final String rootKey) {
            setPreferencesFromResource(R.xml.fragment_preferences, rootKey);

            //Eingabe wird nur verwendet, falls sie ein gültiger Hostname ist
            EditTextPreference hostnamePreference =
                    findPreference(getString(R.string.fragment_preferences_hostname_key));
            if (hostnamePreference != null) {
                hostnamePreference.setOnPreferenceChangeListener(this::isHostname);
            }

            //Eingabe wird nur verwendet, falls sie ein gültiger Port ist
            EditTextPreference portPreference =
                    findPreference(getString(R.string.fragment_preferences_port_key));
            if (portPreference != null) {
                portPreference.setOnPreferenceChangeListener(this::isPort);
            }

            EditTextPreference timeoutPreference =
                    findPreference(getString(R.string.fragment_preferences_timeout_key));
            if (timeoutPreference != null) {
                //Eingabe wird nur verwendet, falls sie ein gültiger Timeout ist
                timeoutPreference.setOnPreferenceChangeListener(this::isTimeout);
                //füge an die Ausgabe die Einheit ms an
                timeoutPreference.setSummaryProvider(
                        (SummaryProvider<EditTextPreference>) preference -> String.format(
                                getString(R.string.activity_settings_timeout_summary),
                                preference.getText()));
            }
        }

        private boolean isTimeout(final Preference preference, final Object newValue) {
            try {
                new Milliseconds(Integer.parseInt((String) newValue));
            } catch (IllegalArgumentException | ClassCastException e) {
                return false;
            }
            return true;
        }

        private boolean isPort(final Preference preference, final Object newValue) {
            try {
                new Port(Integer.parseInt((String) newValue));
            } catch (IllegalArgumentException | ClassCastException e) {
                return false;
            }
            return true;
        }

        private boolean isHostname(final Preference preference, final Object newValue) {
            try {
                new Hostname((String) newValue);
            } catch (IllegalArgumentException | ClassCastException e) {
                return false;
            }
            return true;
        }
    }
}