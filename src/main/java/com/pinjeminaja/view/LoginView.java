package com.pinjeminaja.view;

import com.pinjeminaja.Session;
import com.pinjeminaja.controller.AuthController;
import com.pinjeminaja.model.User;
import javafx.geometry.Insets;
import javafx.geometry.Pos;
import javafx.scene.control.*;
import javafx.scene.effect.DropShadow;
import javafx.scene.layout.*;
import javafx.scene.paint.Color;
import javafx.scene.paint.LinearGradient;
import javafx.scene.paint.Stop;
import javafx.scene.paint.CycleMethod;
import javafx.scene.shape.Rectangle;
import javafx.scene.text.*;

// UC02: Login ke Sistem
public class LoginView extends HBox {

    private final Runnable onLoginSuccess;
    private final Runnable onGoRegister;

    public LoginView(Runnable onLoginSuccess, Runnable onGoRegister) {
        this.onLoginSuccess = onLoginSuccess;
        this.onGoRegister   = onGoRegister;
        build();
    }

    private void build() {
        setMinHeight(640);

        // ── Left panel ──────────────────────────────────────────────────────
        StackPane leftPanel = new StackPane();
        leftPanel.setPrefWidth(520);
        leftPanel.setMinWidth(520);

        Rectangle bg = new Rectangle();
        bg.widthProperty().bind(leftPanel.widthProperty());
        bg.heightProperty().bind(leftPanel.heightProperty());
        bg.setFill(new LinearGradient(0, 0, 1, 1, true, CycleMethod.NO_CYCLE,
            new Stop(0, Color.web("#3D5AF1")),
            new Stop(1, Color.web("#6B8EFF"))
        ));

        VBox leftContent = new VBox(24);
        leftContent.setAlignment(Pos.CENTER_LEFT);
        leftContent.setPadding(new Insets(60));

        Label logoIcon = new Label("🏠");
        logoIcon.setFont(Font.font(52));

        Label appName = new Label("Pinjemin Aja!");
        appName.setFont(UIHelper.bold(36));
        appName.setTextFill(Color.WHITE);

        Label tagline = new Label("The best things in life aren't\nthe things we own, but the\nresources we share.");
        tagline.setFont(UIHelper.regular(16));
        tagline.setTextFill(Color.rgb(255, 255, 255, 0.85));
        tagline.setWrapText(true);
        tagline.setLineSpacing(4);

        // Feature pills
        HBox pill1 = pill("🌱  Eco-Friendly");
        HBox pill2 = pill("🤝  Community");
        HBox pill3 = pill("💰  Smart Savings");
        HBox pills = new HBox(10, pill1, pill2, pill3);
        pills.setAlignment(Pos.CENTER_LEFT);

        leftContent.getChildren().addAll(logoIcon, appName, tagline, pills);
        leftPanel.getChildren().addAll(bg, leftContent);

        // ── Right panel ─────────────────────────────────────────────────────
        VBox rightPanel = new VBox(0);
        rightPanel.setAlignment(Pos.CENTER);
        rightPanel.setStyle("-fx-background-color: " + UIHelper.LIGHT_BG + ";");
        HBox.setHgrow(rightPanel, Priority.ALWAYS);

        VBox formCard = new VBox(20);
        formCard.setPadding(new Insets(40));
        formCard.setMaxWidth(420);
        formCard.setStyle(
            "-fx-background-color: white;" +
            "-fx-background-radius: 20;" +
            "-fx-border-radius: 20;" +
            "-fx-border-color: " + UIHelper.BORDER + ";" +
            "-fx-border-width: 1;"
        );
        DropShadow shadow = new DropShadow(24, 0, 8, Color.rgb(0,0,0,0.08));
        formCard.setEffect(shadow);

        Label title = new Label("Welcome back 👋");
        title.setFont(UIHelper.bold(24));
        title.setTextFill(Color.web(UIHelper.TEXT_DARK));

        Label subtitle = new Label("Log in to your account");
        subtitle.setFont(UIHelper.regular(13));
        subtitle.setTextFill(Color.web(UIHelper.TEXT_GRAY));

        TextField waField = UIHelper.styledTextField("WhatsApp Number");
        waField.setPrefWidth(340);

        PasswordField passField = UIHelper.styledPasswordField("Password");
        passField.setPrefWidth(340);

        Button loginBtn = UIHelper.primaryButton("Log In");
        loginBtn.setPrefWidth(340);
        loginBtn.setPrefHeight(46);
        loginBtn.setFont(UIHelper.semibold(14));

        Label errorLabel = new Label();
        errorLabel.setFont(UIHelper.regular(12));
        errorLabel.setTextFill(Color.web(UIHelper.RED));
        errorLabel.setWrapText(true);
        errorLabel.setMaxWidth(340);
        errorLabel.setVisible(false);

        Hyperlink signupHl = new Hyperlink("Sign Up");
        signupHl.setFont(UIHelper.semibold(13));
        signupHl.setStyle("-fx-text-fill: " + UIHelper.BLUE + "; -fx-border-color: transparent;");
        signupHl.setOnAction(e -> onGoRegister.run());

        Label noAccLabel = new Label("Don't have an account?");
        noAccLabel.setFont(UIHelper.regular(13));
        noAccLabel.setTextFill(Color.web(UIHelper.TEXT_GRAY));

        HBox signupRow = new HBox(4, noAccLabel, signupHl);
        signupRow.setAlignment(Pos.CENTER);

        loginBtn.setOnAction(e -> handleLogin(waField.getText().trim(), passField.getText(), errorLabel));
        passField.setOnAction(e -> loginBtn.fire());

        formCard.getChildren().addAll(
            UIHelper.formField("WhatsApp Number", waField),
            UIHelper.formField("Password", passField),
            loginBtn, errorLabel, signupRow
        );

        // Add title above card
        VBox rightInner = new VBox(24);
        rightInner.setAlignment(Pos.CENTER);
        rightInner.setPadding(new Insets(40));
        VBox titleBox = new VBox(4, title, subtitle);
        titleBox.setAlignment(Pos.CENTER_LEFT);
        titleBox.setMaxWidth(420);
        rightInner.getChildren().addAll(titleBox, formCard);
        rightPanel.getChildren().add(rightInner);

        getChildren().addAll(leftPanel, rightPanel);
    }

    private HBox pill(String text) {
        HBox pill = new HBox();
        pill.setPadding(new Insets(6, 14, 6, 14));
        pill.setStyle("-fx-background-color: rgba(255,255,255,0.2); -fx-background-radius: 20;");
        Label lbl = new Label(text);
        lbl.setFont(UIHelper.regular(12));
        lbl.setTextFill(Color.WHITE);
        pill.getChildren().add(lbl);
        return pill;
    }

    private void handleLogin(String wa, String password, Label errorLabel) {
        if (wa.isEmpty() || password.isEmpty()) {
            errorLabel.setText("WhatsApp dan password tidak boleh kosong.");
            errorLabel.setVisible(true);
            return;
        }
        try {
            User user = AuthController.login(wa, password);
            if (user == null) {
                errorLabel.setText("WhatsApp atau password salah.");
                errorLabel.setVisible(true);
            } else {
                Session.login(user);
                onLoginSuccess.run();
            }
        } catch (Exception ex) {
            errorLabel.setText("Terjadi kesalahan. Coba lagi.");
            errorLabel.setVisible(true);
        }
    }
}
