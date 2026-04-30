package com.pinjeminaja.view;

import com.pinjeminaja.controller.AuthController;
import javafx.geometry.Insets;
import javafx.geometry.Pos;
import javafx.scene.control.*;
import javafx.scene.effect.DropShadow;
import javafx.scene.layout.*;
import javafx.scene.paint.*;
import javafx.scene.shape.Rectangle;
import javafx.scene.text.*;

// UC01: Registrasi Akun
public class RegisterView extends HBox {

    private final Runnable onRegisterSuccess;
    private final Runnable onGoLogin;

    public RegisterView(Runnable onRegisterSuccess, Runnable onGoLogin) {
        this.onRegisterSuccess = onRegisterSuccess;
        this.onGoLogin         = onGoLogin;
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

        Label tagline = new Label("Join your community.\nShare tools, save money,\nbuild a greener neighborhood.");
        tagline.setFont(UIHelper.regular(16));
        tagline.setTextFill(Color.rgb(255, 255, 255, 0.85));
        tagline.setWrapText(true);
        tagline.setLineSpacing(4);

        leftContent.getChildren().addAll(logoIcon, appName, tagline);
        leftPanel.getChildren().addAll(bg, leftContent);

        // ── Right panel ─────────────────────────────────────────────────────
        VBox rightPanel = new VBox(0);
        rightPanel.setAlignment(Pos.CENTER);
        rightPanel.setStyle("-fx-background-color: " + UIHelper.LIGHT_BG + ";");
        HBox.setHgrow(rightPanel, Priority.ALWAYS);

        VBox formCard = new VBox(16);
        formCard.setPadding(new Insets(36));
        formCard.setMaxWidth(420);
        formCard.setStyle(
            "-fx-background-color: white;" +
            "-fx-background-radius: 20;" +
            "-fx-border-radius: 20;" +
            "-fx-border-color: " + UIHelper.BORDER + ";" +
            "-fx-border-width: 1;"
        );
        formCard.setEffect(new DropShadow(24, 0, 8, Color.rgb(0,0,0,0.08)));

        Label title    = new Label("Create an account ✨");
        title.setFont(UIHelper.bold(22));
        title.setTextFill(Color.web(UIHelper.TEXT_DARK));
        Label subtitle = new Label("Fill in your details to get started");
        subtitle.setFont(UIHelper.regular(13));
        subtitle.setTextFill(Color.web(UIHelper.TEXT_GRAY));

        TextField nameField    = UIHelper.styledTextField("Full Name");
        TextField waField      = UIHelper.styledTextField("WhatsApp Number");
        TextField addressField = UIHelper.styledTextField("Address");
        PasswordField passField        = UIHelper.styledPasswordField("Password");
        PasswordField confirmPassField = UIHelper.styledPasswordField("Confirm Password");

        for (Control c : new Control[]{nameField, waField, addressField, passField, confirmPassField})
            ((Region) c).setPrefWidth(348);

        Button signupBtn = UIHelper.primaryButton("Create Account");
        signupBtn.setPrefWidth(348);
        signupBtn.setPrefHeight(46);
        signupBtn.setFont(UIHelper.semibold(14));

        Label errorLabel = new Label();
        errorLabel.setFont(UIHelper.regular(12));
        errorLabel.setTextFill(Color.web(UIHelper.RED));
        errorLabel.setWrapText(true);
        errorLabel.setMaxWidth(348);
        errorLabel.setVisible(false);

        Hyperlink loginHl = new Hyperlink("Log In");
        loginHl.setFont(UIHelper.semibold(13));
        loginHl.setStyle("-fx-text-fill: " + UIHelper.BLUE + "; -fx-border-color: transparent;");
        loginHl.setOnAction(e -> onGoLogin.run());
        Label hasAccLabel = new Label("Already have an account?");
        hasAccLabel.setFont(UIHelper.regular(13));
        hasAccLabel.setTextFill(Color.web(UIHelper.TEXT_GRAY));
        HBox loginRow = new HBox(4, hasAccLabel, loginHl);
        loginRow.setAlignment(Pos.CENTER);

        signupBtn.setOnAction(e -> handleRegister(
            nameField.getText().trim(), waField.getText().trim(),
            addressField.getText().trim(), passField.getText(),
            confirmPassField.getText(), errorLabel
        ));

        formCard.getChildren().addAll(
            title, subtitle,
            UIHelper.formField("Full Name", nameField),
            UIHelper.formField("WhatsApp Number", waField),
            UIHelper.formField("Address", addressField),
            UIHelper.formField("Password", passField),
            UIHelper.formField("Confirm Password", confirmPassField),
            signupBtn, errorLabel, loginRow
        );

        VBox rightInner = new VBox(20);
        rightInner.setAlignment(Pos.CENTER);
        rightInner.setPadding(new Insets(40));
        rightInner.getChildren().add(formCard);
        rightPanel.getChildren().add(rightInner);

        getChildren().addAll(leftPanel, rightPanel);
    }

    private void handleRegister(String name, String wa, String address, String pass, String confirm, Label err) {
        if (name.isEmpty() || wa.isEmpty() || address.isEmpty() || pass.isEmpty() || confirm.isEmpty()) {
            err.setText("Semua kolom harus diisi."); err.setVisible(true); return;
        }
        if (!pass.equals(confirm)) {
            err.setText("Password dan konfirmasi tidak sama."); err.setVisible(true); return;
        }
        try {
            boolean ok = AuthController.register(name, wa, address, pass);
            if (ok) {
                UIHelper.showAlert("Berhasil", "Akun berhasil dibuat. Silakan login.");
                onRegisterSuccess.run();
            } else {
                err.setText("Nomor WhatsApp sudah terdaftar."); err.setVisible(true);
            }
        } catch (Exception ex) {
            err.setText("Terjadi kesalahan. Coba lagi."); err.setVisible(true);
        }
    }
}
