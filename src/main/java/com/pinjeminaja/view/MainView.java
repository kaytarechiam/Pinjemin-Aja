package com.pinjeminaja.view;

import com.pinjeminaja.Session;
import javafx.geometry.Insets;
import javafx.geometry.Pos;
import javafx.scene.Node;
import javafx.scene.control.*;
import javafx.scene.layout.*;
import javafx.scene.paint.Color;
import javafx.scene.text.*;

public class MainView extends BorderPane {

    private final Runnable onLogout;
    private BorderPane contentArea;

    public static final String HOME         = "home";
    public static final String CATALOGUE    = "catalogue";
    public static final String MY_ITEMS     = "myitems";
    public static final String WALLET       = "wallet";
    public static final String PROFILE      = "profile";
    public static final String TRANSACTIONS = "transactions";

    public MainView(Runnable onLogout) {
        this.onLogout = onLogout;
        build();
        navigate(HOME);
    }

    private void build() {
        setTop(buildNavbar());
        contentArea = new BorderPane();
        contentArea.setStyle("-fx-background-color: " + UIHelper.LIGHT_BG + ";");
        setCenter(contentArea);
    }

    private HBox buildNavbar() {
        HBox navbar = new HBox(0);
        navbar.setAlignment(Pos.CENTER_LEFT);
        navbar.setPadding(new Insets(0, 32, 0, 32));
        navbar.setPrefHeight(62);
        navbar.setStyle(
            "-fx-background-color: white;" +
            "-fx-border-color: " + UIHelper.BORDER + ";" +
            "-fx-border-width: 0 0 1 0;" +
            "-fx-effect: dropshadow(gaussian, rgba(0,0,0,0.04), 6, 0, 0, 2);"
        );

        // Logo
        HBox logoBox = new HBox(8);
        logoBox.setAlignment(Pos.CENTER_LEFT);
        logoBox.setPadding(new Insets(0, 28, 0, 0));
        Label logoIcon = new Label("🏠");
        logoIcon.setFont(Font.font(20));
        Label logoText = new Label("Pinjemin Aja!");
        logoText.setFont(UIHelper.bold(17));
        logoText.setTextFill(Color.web(UIHelper.TEXT_DARK));
        logoBox.getChildren().addAll(logoIcon, logoText);

        // Nav items
        HBox navLinks = new HBox(4);
        navLinks.setAlignment(Pos.CENTER);
        navLinks.getChildren().addAll(
            navBtn("Home",         HOME),
            navBtn("Explore Items", CATALOGUE),
            navBtn("My Items",     MY_ITEMS)
        );

        // Search bar (UC14)
        TextField searchField = new TextField();
        searchField.setPromptText("Search products...");
        searchField.setPrefWidth(220);
        searchField.setPrefHeight(36);
        searchField.setFont(UIHelper.regular(13));
        searchField.setStyle(
            "-fx-background-color: " + UIHelper.LIGHT_BG + ";" +
            "-fx-border-color: " + UIHelper.BORDER + ";" +
            "-fx-border-radius: 20;" +
            "-fx-background-radius: 20;" +
            "-fx-padding: 6 14 6 36;" +
            "-fx-font-size: 13;"
        );
        searchField.setOnAction(e -> {
            String kw = searchField.getText().trim();
            setContent(new CatalogueView(kw, null, this::navigate, this::showProductDetail));
        });

        // User avatar + menu
        String name = Session.getCurrentUser() != null ? Session.getCurrentUser().getFullName() : "User";
        String initials = name.length() > 0 ? String.valueOf(name.charAt(0)).toUpperCase() : "U";

        MenuButton userMenu = new MenuButton(initials + "  ▾");
        userMenu.setFont(UIHelper.semibold(13));
        userMenu.setStyle(
            "-fx-background-color: " + UIHelper.BLUE_LIGHT + ";" +
            "-fx-text-fill: " + UIHelper.BLUE + ";" +
            "-fx-background-radius: 20;" +
            "-fx-border-radius: 20;" +
            "-fx-padding: 6 14;" +
            "-fx-cursor: hand;"
        );

        MenuItem profileItem = new MenuItem("👤  Profile");
        profileItem.setOnAction(e -> navigate(PROFILE));

        MenuItem walletItem = new MenuItem("💳  My Wallet");
        walletItem.setOnAction(e -> navigate(WALLET));

        MenuItem transItem = new MenuItem("📋  Transaction History");
        transItem.setOnAction(e -> navigate(TRANSACTIONS));

        MenuItem logoutItem = new MenuItem("🚪  Logout");
        logoutItem.setOnAction(e -> { Session.logout(); onLogout.run(); });

        userMenu.getItems().addAll(profileItem, walletItem, transItem, new SeparatorMenuItem(), logoutItem);

        HBox rightBox = new HBox(12, searchField, userMenu);
        rightBox.setAlignment(Pos.CENTER_RIGHT);

        navbar.getChildren().addAll(logoBox, navLinks, UIHelper.spacer(), rightBox);
        return navbar;
    }

    private Button navBtn(String text, String page) {
        Button btn = new Button(text);
        btn.setFont(UIHelper.medium(13));
        btn.setStyle(
            "-fx-background-color: transparent;" +
            "-fx-text-fill: " + UIHelper.TEXT_MID + ";" +
            "-fx-cursor: hand;" +
            "-fx-padding: 8 16;" +
            "-fx-background-radius: 8;"
        );
        btn.setOnMouseEntered(e -> btn.setStyle(
            "-fx-background-color: " + UIHelper.BLUE_LIGHT + ";" +
            "-fx-text-fill: " + UIHelper.BLUE + ";" +
            "-fx-cursor: hand;" +
            "-fx-padding: 8 16;" +
            "-fx-background-radius: 8;"
        ));
        btn.setOnMouseExited(e -> btn.setStyle(
            "-fx-background-color: transparent;" +
            "-fx-text-fill: " + UIHelper.TEXT_MID + ";" +
            "-fx-cursor: hand;" +
            "-fx-padding: 8 16;" +
            "-fx-background-radius: 8;"
        ));
        btn.setOnAction(e -> navigate(page));
        return btn;
    }

    public void navigate(String page) {
        switch (page) {
            case HOME         -> setContent(new HomeView(this::navigate, this::showProductDetail));
            case CATALOGUE    -> setContent(new CatalogueView(null, null, this::navigate, this::showProductDetail));
            case MY_ITEMS     -> setContent(new MyItemsView(this::navigate));
            case WALLET       -> setContent(new WalletView(this::navigate));
            case PROFILE      -> setContent(new ProfileView());
            case TRANSACTIONS -> setContent(new TransactionHistoryView());
        }
    }

    private void showProductDetail(int itemId) {
        setContent(new ProductDetailView(itemId, this::navigate));
    }

    public void setContent(Node node) {
        contentArea.setCenter(node);
    }
}
