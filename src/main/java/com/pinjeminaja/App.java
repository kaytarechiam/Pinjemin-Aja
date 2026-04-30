package com.pinjeminaja;

import com.pinjeminaja.db.Database;
import com.pinjeminaja.db.Seeder;
import com.pinjeminaja.view.UIHelper;
import com.pinjeminaja.view.LoginView;
import com.pinjeminaja.view.MainView;
import com.pinjeminaja.view.RegisterView;
import javafx.application.Application;
import javafx.scene.Scene;
import javafx.stage.Stage;

public class App extends Application {

    private static Stage primaryStage;

    @Override
    public void start(Stage stage) {
        primaryStage = stage;
        UIHelper.loadFonts();
        Database.initialize();
        Seeder.seed();
        showLogin(stage);
        stage.setTitle("Pinjemin Aja!");
        stage.setWidth(1100);
        stage.setHeight(720);
        stage.setMinWidth(900);
        stage.setMinHeight(600);
        stage.show();
    }

    public static void showLogin(Stage stage) {
        LoginView loginView = new LoginView(
            () -> showMain(stage),
            () -> showRegister(stage)
        );
        Scene scene = new Scene(loginView);
        stage.setScene(scene);
    }

    public static void showRegister(Stage stage) {
        RegisterView registerView = new RegisterView(
            () -> showLogin(stage),
            () -> showLogin(stage)
        );
        Scene scene = new Scene(registerView);
        stage.setScene(scene);
    }

    public static void showMain(Stage stage) {
        MainView mainView = new MainView(() -> showLogin(stage));
        Scene scene = new Scene(mainView);
        stage.setScene(scene);
    }

    public static void main(String[] args) {
        launch(args);
    }
}
