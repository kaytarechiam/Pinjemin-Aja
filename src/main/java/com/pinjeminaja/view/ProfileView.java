package com.pinjeminaja.view;

import com.pinjeminaja.Session;
import com.pinjeminaja.controller.AuthController;
import com.pinjeminaja.model.User;
import javafx.geometry.Insets;
import javafx.geometry.Pos;
import javafx.scene.control.*;
import javafx.scene.layout.*;
import javafx.scene.paint.Color;
import javafx.scene.text.*;

// UC03, UC04, UC05
public class ProfileView extends BorderPane {

    public ProfileView() {
        build();
    }

    private void build() {
        setStyle("-fx-background-color: " + UIHelper.LIGHT_BG + ";");
        setLeft(buildSidebar());

        ScrollPane scroll = new ScrollPane();
        scroll.setFitToWidth(true);
        scroll.setHbarPolicy(ScrollPane.ScrollBarPolicy.NEVER);
        scroll.setStyle("-fx-background-color: " + UIHelper.LIGHT_BG + "; -fx-background: " + UIHelper.LIGHT_BG + ";");
        scroll.setContent(buildContent());
        setCenter(scroll);
    }

    private VBox buildContent() {
        VBox content = new VBox(20);
        content.setPadding(new Insets(32, 40, 40, 40));

        // Breadcrumb
        HBox bc = new HBox(6);
        bc.getChildren().addAll(UIHelper.secondaryLabel("Home"), UIHelper.secondaryLabel("›"), UIHelper.secondaryLabel("My Account"));

        Label pageTitle = UIHelper.heading("My Account");

        // Profile card
        VBox profileCard = UIHelper.card();
        profileCard.setMaxWidth(560);

        Label cardTitle = UIHelper.subheading("Profile");

        // Avatar circle
        StackPane avatar = new StackPane();
        avatar.setPrefSize(72, 72);
        String name = Session.getCurrentUser().getFullName();
        String initials = name.length() > 1 ? name.substring(0, 2).toUpperCase() : name.toUpperCase();
        avatar.setStyle("-fx-background-color: " + UIHelper.BLUE_LIGHT + "; -fx-background-radius: 36;");
        Label initLbl = new Label(initials);
        initLbl.setFont(UIHelper.bold(24));
        initLbl.setTextFill(Color.web(UIHelper.BLUE));
        avatar.getChildren().add(initLbl);

        User user = Session.getCurrentUser();

        TextField nameField    = UIHelper.styledTextField("Full name");
        nameField.setText(user.getFullName());
        nameField.setPrefWidth(460);

        TextField waField = UIHelper.styledTextField("WhatsApp Number");
        waField.setText(user.getWhatsapp());
        waField.setPrefWidth(460);

        TextArea addressArea = UIHelper.styledTextArea("Address");
        addressArea.setText(user.getAddress());
        addressArea.setPrefWidth(460);
        addressArea.setPrefRowCount(2);

        Separator sep = new Separator();
        sep.setPadding(new Insets(4, 0, 4, 0));

        Label passSection = new Label("Ganti Password");
        passSection.setFont(UIHelper.semibold(14));
        passSection.setTextFill(Color.web(UIHelper.TEXT_DARK));

        PasswordField oldPassField = UIHelper.styledPasswordField("Password saat ini");
        oldPassField.setPrefWidth(460);

        PasswordField newPassField = UIHelper.styledPasswordField("Password baru");
        newPassField.setPrefWidth(460);

        Label errorLabel = new Label();
        errorLabel.setFont(UIHelper.regular(12));
        errorLabel.setTextFill(Color.web(UIHelper.RED));
        errorLabel.setWrapText(true);
        errorLabel.setMaxWidth(460);
        errorLabel.setVisible(false);

        Button saveBtn = UIHelper.primaryButton("💾  Save Changes");
        saveBtn.setPrefWidth(180);
        saveBtn.setOnAction(e -> handleSave(
            nameField.getText().trim(), waField.getText().trim(),
            addressArea.getText().trim(), oldPassField.getText(),
            newPassField.getText(), errorLabel
        ));

        profileCard.getChildren().addAll(
            cardTitle, avatar,
            UIHelper.formField("Full Name", nameField),
            UIHelper.formField("WhatsApp Number", waField),
            UIHelper.formField("Address", addressArea),
            sep, passSection,
            UIHelper.formField("Current Password (kosongkan jika tidak ingin ganti)", oldPassField),
            UIHelper.formField("New Password", newPassField),
            saveBtn, errorLabel
        );

        content.getChildren().addAll(bc, pageTitle, profileCard);
        return content;
    }

    private void handleSave(String name, String wa, String address, String oldPass, String newPass, Label err) {
        if (name.isEmpty() || wa.isEmpty() || address.isEmpty()) {
            err.setText("Nama, WhatsApp, dan alamat tidak boleh kosong."); err.setVisible(true); return;
        }
        try {
            AuthController.updateProfile(Session.getCurrentUser().getId(), name, wa, address);
            if (!oldPass.isEmpty() || !newPass.isEmpty()) {
                if (oldPass.isEmpty() || newPass.isEmpty()) {
                    err.setText("Isi password lama dan baru untuk mengganti password."); err.setVisible(true); return;
                }
                if (!AuthController.changePassword(Session.getCurrentUser().getId(), oldPass, newPass)) {
                    err.setText("Password lama salah."); err.setVisible(true); return;
                }
            }
            User updated = AuthController.getUserById(Session.getCurrentUser().getId());
            Session.login(updated);
            err.setVisible(false);
            UIHelper.showAlert("Berhasil ✓", "Profil berhasil diperbarui.");
        } catch (Exception ex) {
            err.setText("Terjadi kesalahan. Coba lagi."); err.setVisible(true);
        }
    }

    private VBox buildSidebar() {
        VBox sidebar = new VBox(4);
        sidebar.setPrefWidth(220);
        sidebar.setPadding(new Insets(28, 16, 28, 16));
        sidebar.setStyle("-fx-background-color: white; -fx-border-color: " + UIHelper.BORDER + "; -fx-border-width: 0 1 0 0;");

        Button profileBtn = sidebarBtn("👤  Profile", true);
        Button walletBtn  = sidebarBtn("💳  My Wallet", false);
        walletBtn.setOnAction(e -> {
            javafx.stage.Stage stage = (javafx.stage.Stage) getScene().getWindow();
            com.pinjeminaja.App.showMain(stage);
        });

        Separator sep = new Separator();
        sep.setPadding(new Insets(8, 0, 8, 0));

        Button logoutBtn = new Button("🚪  Logout");
        logoutBtn.setFont(UIHelper.medium(13));
        logoutBtn.setPrefWidth(188);
        logoutBtn.setPrefHeight(40);
        logoutBtn.setStyle("-fx-background-color: transparent; -fx-text-fill: " + UIHelper.RED + "; -fx-alignment: CENTER_LEFT; -fx-padding: 8 16; -fx-background-radius: 8; -fx-cursor: hand;");
        logoutBtn.setOnAction(e -> {
            if (UIHelper.showConfirm("Yakin ingin logout?")) {
                Session.logout();
                javafx.stage.Stage stage = (javafx.stage.Stage) getScene().getWindow();
                com.pinjeminaja.App.showLogin(stage);
            }
        });

        sidebar.getChildren().addAll(profileBtn, walletBtn, sep, logoutBtn);
        return sidebar;
    }

    private Button sidebarBtn(String text, boolean active) {
        Button btn = new Button(text);
        btn.setFont(UIHelper.medium(13));
        btn.setPrefWidth(188);
        btn.setPrefHeight(40);
        btn.setStyle(active
            ? "-fx-background-color: " + UIHelper.BLUE_LIGHT + "; -fx-text-fill: " + UIHelper.BLUE + "; -fx-font-weight: bold; -fx-alignment: CENTER_LEFT; -fx-padding: 8 16; -fx-background-radius: 8; -fx-cursor: hand;"
            : "-fx-background-color: transparent; -fx-text-fill: " + UIHelper.TEXT_MID + "; -fx-alignment: CENTER_LEFT; -fx-padding: 8 16; -fx-background-radius: 8; -fx-cursor: hand;"
        );
        return btn;
    }
}
