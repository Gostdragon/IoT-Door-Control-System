package edu.kit.informatik.adminapp.view;

import android.content.Intent;
import android.os.Bundle;
import android.text.Editable;
import android.text.TextWatcher;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ListView;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

import java.io.IOException;
import java.util.Collection;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

import edu.kit.informatik.adminapp.R;
import edu.kit.informatik.adminapp.controller.server.ServerAdapter;
import edu.kit.informatik.adminapp.core.Output;
import edu.kit.informatik.adminapp.model.Attribute;
import edu.kit.informatik.adminapp.model.User;
import edu.kit.informatik.adminapp.model.resources.Extras;

/**
 * Diese Klasse stellt eine Aktivität dar, mit der Suchanfragen nach Nutzern in einem Server
 * gestellt werden können.
 *
 * @author Daniel Luckey
 * @version 1.0
 */
public class SearchUserActivity extends AppCompatActivity {
    //ATTRIBUTE_KEY_USER_NAME, BASE werden von PiAdapter nicht verwendet
    private static final String ATTRIBUTE_KEY_USER_NAME = "sn";
    private static final String BASE = "";
    private final Output errorOutput = (String message) -> runOnUiThread(
            () -> Toast.makeText(this, message, Toast.LENGTH_LONG).show());

    private ServerAdapter serverAdapter;
    private ExecutorService executor;
    private EditText searchName;
    private Button searchButton;
    private ListView userList;
    private ArrayAdapter<User> userListAdapter;

    /**
     * Lädt die View-Elemente der Aktivität und versucht in einem neuen Thread eine Verbindung zum
     * Server herzustellen. Falls die Verbindung fehlschlägt, wird eine entsprechende Fehlermeldung
     * ausgegeben.
     *
     * @param savedInstanceState    beinhaltet den Status einer früheren gespeicherten Aktivität,
     *                              {@code null} falls die Aktivität noch nie verlassen wurde
     */
    @Override
    protected void onCreate(final Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_search_user);

        this.executor = Executors.newSingleThreadExecutor(); //um Tasks sequenziell abzuarbeiten;
        this.serverAdapter = getIntent().getParcelableExtra(Extras.EXTRA_SERVER_ADAPTER);
        this.searchName = findViewById(R.id.activity_search_user_et_searchName);
        this.searchButton = findViewById(R.id.activity_search_user_btn_search);
        this.userList = findViewById(R.id.activity_search_user_lv_users);

        this.searchName.addTextChangedListener(new TextWatcher() {
            @Override
            public void beforeTextChanged(final CharSequence charSequence, final int start,
                                          final int count, final int after) {}

            @Override
            public void onTextChanged(final CharSequence charSequence, final int start,
                                      final int before, final int count) {}

            @Override
            public void afterTextChanged(final Editable editable) {
                if (searchName.getText().length() == 0 && searchButton.isEnabled()) {
                    disableSearchButton();
                } else if (!searchButton.isEnabled()) {
                    enableSearchButton();
                }
            }
        });
        disableSearchButton();
        this.searchButton.setOnClickListener((View view) -> onSearchButtonClick());

        this.userListAdapter = new ArrayAdapter<>(
                this, android.R.layout.simple_list_item_1);
        this.userList.setAdapter(this.userListAdapter);
        this.userList.setOnItemClickListener(this::onItemClick);

        // connect kann nicht in onStart() aufgerufen werden, da connect() in onRestart() aufgerufen
        // werden muss und somit zweimal connect() aufgerufen werden könnte
        this.executor.submit(this::connect);
    }

    private void onItemClick(final AdapterView<?> adapterView,
                             final View view, final int position, final long id) {
        Intent intent = new Intent(this, ShowUserActivity.class);
        intent.putExtra(Extras.EXTRA_SERVER_ADAPTER, this.serverAdapter)
                .putExtra(Extras.EXTRA_USER, this.userListAdapter.getItem(position));
        startActivity(intent);
    }

    private void enableSearchButton() {
        this.searchButton.setEnabled(true);
    }

    private void disableSearchButton() {
        this.searchButton.setEnabled(false);
    }

    private void onSearchButtonClick() {
        this.executor.submit(this::searchForUsers);
    }

    private void searchForUsers() {
        runOnUiThread(() -> clearUserList());    //alte Suche wird gelöscht);
        try {
            if (!this.serverAdapter.isConnected()) {
                this.serverAdapter.connect();
            }
            Attribute searchAttribute = new Attribute(
                    ATTRIBUTE_KEY_USER_NAME, this.searchName.getText().toString());
            Collection<User> users = this.serverAdapter.search(BASE, searchAttribute);
            if (users != null && users.size() > 0) {
                runOnUiThread(() -> this.userListAdapter.addAll(users));
            } else {
                this.errorOutput.output(getString(R.string.ERROR_NO_ENTRY_FOUND));
            }
        } catch (IOException e) {
            this.errorOutput.output(getString(R.string.ERROR_CONNECT_FAILED));
        }
    }

    private void clearUserList() {
        this.userListAdapter.clear();
    }

    private void connect() {
        try {
            if (!this.serverAdapter.isConnected()) {
                serverAdapter.connect();
            }
        } catch (IOException e) {
            errorOutput.output(getString(R.string.ERROR_CONNECT_FAILED));
        }
    }

    /**
     * Lädt die letzte Suchanfrage neu.
     * Falls keien Verbindung zum Server möglich ist, wird eine entsprechende Fehlermeldung
     * ausgegeben.
     */
    @Override
    protected void onRestart() {
        super.onRestart();
        this.executor = Executors.newSingleThreadExecutor(); //um Tasks sequenziell abzuarbeiten;
        onSearchButtonClick();
    }

    /**
     * Schließt die Verbindung zum Server.
     */
    @Override
    protected void onStop() {
        super.onStop();
        this.executor.submit(this::close);
        this.executor.shutdown();
    }

    private void close() {
        try {
            this.serverAdapter.close();
        } catch (IOException e) {
            //keine Möglichkeit den Fehler zu beheben
        }
    }
}