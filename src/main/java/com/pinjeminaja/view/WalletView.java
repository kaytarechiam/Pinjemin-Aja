package com.pinjeminaja.view;

import com.pinjeminaja.Session;
import com.pinjeminaja.controller.TransactionController;
import com.pinjeminaja.controller.WalletController;
import com.pinjeminaja.model.Transaction;
import javafx.geometry.Insets;
import javafx.geometry.Pos;
import javafx.scene.control.*;
import javafx.scene.effect.DropShadow;
import javafx.scene.layout.*;
import javafx.scene.paint.*;
import javafx.scene.shape.Rectangle;
import javafx.scene.text.*;

import java.util.List;
import java.util.function.Consumer;

// UC06, UC07, UC08
public class WalletView extends BorderPane {

    private final Consumer<String> navigate;
    private Label balanceLabel;

    public WalletView(Consumer<String> navigate) {
        this.navigate = navigate;
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
        bc.setAlignment(Pos.CENTER_LEFT);
        bc.getChildren().addAll(UIHelper.secondaryLabel("Home"), UIHelper.secondaryLabel("›"), UIHelper.secondaryLabel("My Account"));

        Label pageTitle = UIHelper.heading("My Account");

        // Balance card (UC06)
        StackPane balanceCard = new StackPane();
        balanceCard.setPrefHeight(120);
        balanceCard.setMaxWidth(460);

        Rectangle cardBg = new Rectangle(460, 120);
        cardBg.setArcWidth(20); cardBg.setArcHeight(20);
        cardBg.setFill(new LinearGradient(0, 0, 1, 0, true, CycleMethod.NO_CYCLE,
            new Stop(0, Color.web("#3D5AF1")),
            new Stop(1, Color.web("#6B8EFF"))
        ));
        cardBg.setEffect(new DropShadow(20, 0, 6, Color.web("#3D5AF1", 0.35)));

        VBox cardText = new VBox(6);
        cardText.setAlignment(Pos.CENTER_LEFT);
        cardText.setPadding(new Insets(0, 0, 0, 28));

        Label balLbl = new Label("Balance");
        balLbl.setFont(UIHelper.regular(13));
        balLbl.setTextFill(Color.rgb(255, 255, 255, 0.8));

        balanceLabel = new Label(UIHelper.formatRupiah(Session.getCurrentUser().getWalletBalance()));
        balanceLabel.setFont(UIHelper.bold(30));
        balanceLabel.setTextFill(Color.WHITE);

        cardText.getChildren().addAll(balLbl, balanceLabel);
        balanceCard.getChildren().addAll(cardBg, cardText);

        // Action buttons (UC07 Top-up, UC08 Withdraw)
        HBox actions = new HBox(16);
        actions.setAlignment(Pos.CENTER_LEFT);

        Button topUpBtn   = actionBtn("➕", "Top Up");
        Button withdrawBtn = actionBtn("⬆", "Withdraw");
        topUpBtn.setOnAction(e -> showAmountDialog("Top Up Saldo", true));
        withdrawBtn.setOnAction(e -> showAmountDialog("Tarik Saldo", false));
        actions.getChildren().addAll(topUpBtn, withdrawBtn);

        // Recent transactions
        VBox txCard = UIHelper.card();
        txCard.setMaxWidth(Double.MAX_VALUE);

        HBox txHeader = new HBox();
        txHeader.setAlignment(Pos.CENTER_LEFT);
        Label txTitle = UIHelper.subheading("Recent Transaction");
        Hyperlink viewAll = new Hyperlink("View All →");
        viewAll.setFont(UIHelper.medium(12));
        viewAll.setStyle("-fx-text-fill: " + UIHelper.BLUE + "; -fx-border-color: transparent;");
        viewAll.setOnAction(e -> navigate.accept(MainView.TRANSACTIONS));
        txHeader.getChildren().addAll(txTitle, UIHelper.spacer(), viewAll);

        VBox txList = new VBox(0);
        try {
            List<Transaction> txns = TransactionController.getRecentTransactions(Session.getCurrentUser().getId(), 5);
            if (txns.isEmpty()) {
                Label empty = UIHelper.secondaryLabel("Belum ada transaksi.");
                empty.setPadding(new Insets(12, 0, 0, 0));
                txList.getChildren().add(empty);
            } else {
                for (Transaction t : txns) txList.getChildren().add(txRow(t));
            }
        } catch (Exception ex) {
            txList.getChildren().add(UIHelper.secondaryLabel("Gagal memuat transaksi."));
        }

        txCard.getChildren().addAll(txHeader, new Separator(), txList);
        content.getChildren().addAll(bc, pageTitle, balanceCard, actions, txCard);
        return content;
    }

    private Button actionBtn(String icon, String label) {
        VBox box = new VBox(6);
        box.setAlignment(Pos.CENTER);
        box.setPrefWidth(100);
        box.setPrefHeight(70);
        box.setStyle(
            "-fx-background-color: " + UIHelper.BLUE_LIGHT + ";" +
            "-fx-background-radius: 12;" +
            "-fx-cursor: hand;"
        );
        Label ic = new Label(icon);
        ic.setFont(Font.font(20));
        ic.setTextFill(Color.web(UIHelper.BLUE));
        Label lbl = new Label(label);
        lbl.setFont(UIHelper.medium(12));
        lbl.setTextFill(Color.web(UIHelper.BLUE));
        box.getChildren().addAll(ic, lbl);

        Button btn = new Button();
        btn.setGraphic(box);
        btn.setStyle("-fx-background-color: transparent; -fx-padding: 0; -fx-cursor: hand;");
        return btn;
    }

    private HBox txRow(Transaction t) {
        HBox row = new HBox(14);
        row.setAlignment(Pos.CENTER_LEFT);
        row.setPadding(new Insets(12, 0, 12, 0));
        row.setStyle("-fx-border-color: " + UIHelper.BORDER + "; -fx-border-width: 0 0 1 0;");

        boolean isRenter = t.getRenterId() == Session.getCurrentUser().getId();

        // Icon
        StackPane iconBox = new StackPane();
        iconBox.setPrefSize(40, 40);
        iconBox.setStyle("-fx-background-color: " + UIHelper.BLUE_LIGHT + "; -fx-background-radius: 10;");
        Label ic = new Label(UIHelper.categoryEmoji(t.getItemTitle().contains("Maker") ? "Kitchen" : "Tools"));
        ic.setFont(Font.font(18));
        iconBox.getChildren().add(ic);

        VBox text = new VBox(3);
        Label name = new Label(t.getItemTitle());
        name.setFont(UIHelper.semibold(13));
        name.setTextFill(Color.web(UIHelper.TEXT_DARK));
        Label type = new Label(isRenter ? "Rent" : "Income");
        type.setFont(UIHelper.regular(11));
        type.setTextFill(Color.web(UIHelper.TEXT_GRAY));
        text.getChildren().addAll(name, type);

        Label amt = new Label((isRenter ? "-" : "+") + UIHelper.formatRupiah(t.getTotalPrice()));
        amt.setFont(UIHelper.semibold(14));
        amt.setTextFill(isRenter ? Color.web(UIHelper.RED) : Color.web(UIHelper.GREEN));

        row.getChildren().addAll(iconBox, text, UIHelper.spacer(), amt);
        return row;
    }

    private VBox buildSidebar() {
        VBox sidebar = new VBox(4);
        sidebar.setPrefWidth(220);
        sidebar.setPadding(new Insets(28, 16, 28, 16));
        sidebar.setStyle("-fx-background-color: white; -fx-border-color: " + UIHelper.BORDER + "; -fx-border-width: 0 1 0 0;");

        Button profileBtn = sidebarBtn("👤  Profile", false);
        profileBtn.setOnAction(e -> navigate.accept(MainView.PROFILE));

        Button walletBtn  = sidebarBtn("💳  My Wallet", true);

        Separator sep = new Separator();
        sep.setPadding(new Insets(8, 0, 8, 0));

        Button logoutBtn = new Button("🚪  Logout");
        logoutBtn.setFont(UIHelper.medium(13));
        logoutBtn.setPrefWidth(188);
        logoutBtn.setPrefHeight(40);
        logoutBtn.setStyle("-fx-background-color: transparent; -fx-text-fill: " + UIHelper.RED + "; -fx-alignment: CENTER_LEFT; -fx-padding: 8 16; -fx-background-radius: 8; -fx-cursor: hand;");
        logoutBtn.setOnAction(e -> { Session.logout(); navigate.accept("logout"); });

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

    private void showAmountDialog(String title, boolean isTopUp) {
        TextInputDialog dialog = new TextInputDialog();
        dialog.setTitle(title);
        dialog.setHeaderText(null);
        dialog.setContentText("Masukkan nominal (Rp):");
        dialog.showAndWait().ifPresent(input -> {
            try {
                double amount = Double.parseDouble(input.trim().replace(".", "").replace(",", ""));
                double newBalance = isTopUp
                    ? WalletController.topUp(Session.getCurrentUser().getId(), amount)
                    : WalletController.withdraw(Session.getCurrentUser().getId(), amount);
                Session.refreshBalance(newBalance);
                UIHelper.showAlert("Berhasil", title + " berhasil!\nSaldo: " + UIHelper.formatRupiah(newBalance));
                build();
            } catch (NumberFormatException ex) {
                UIHelper.showError("Masukkan angka yang valid.");
            } catch (IllegalArgumentException ex) {
                UIHelper.showError("Nominal harus lebih dari 0.");
            } catch (IllegalStateException ex) {
                UIHelper.showError("Saldo tidak mencukupi.");
            } catch (Exception ex) {
                UIHelper.showError("Terjadi kesalahan.");
            }
        });
    }
}
