package com.pinjeminaja.view;

import com.pinjeminaja.Session;
import com.pinjeminaja.controller.ItemController;
import com.pinjeminaja.controller.TransactionController;
import com.pinjeminaja.controller.WalletController;
import com.pinjeminaja.model.Item;
import javafx.geometry.Insets;
import javafx.geometry.Pos;
import javafx.scene.control.*;
import javafx.scene.effect.DropShadow;
import javafx.scene.image.Image;
import javafx.scene.image.ImageView;
import javafx.scene.layout.*;
import javafx.scene.paint.*;
import javafx.scene.text.*;

import java.time.LocalDate;
import java.time.temporal.ChronoUnit;
import java.util.function.Consumer;

// UC16, UC17
public class ProductDetailView extends ScrollPane {

    private final int itemId;
    private final Consumer<String> navigate;

    public ProductDetailView(int itemId, Consumer<String> navigate) {
        this.itemId   = itemId;
        this.navigate = navigate;
        setFitToWidth(true);
        setHbarPolicy(ScrollBarPolicy.NEVER);
        setStyle("-fx-background-color: " + UIHelper.LIGHT_BG + "; -fx-background: " + UIHelper.LIGHT_BG + ";");
        setContent(build());
    }

    private VBox build() {
        VBox root = new VBox(0);
        root.setStyle("-fx-background-color: " + UIHelper.LIGHT_BG + ";");

        Item item;
        try { item = ItemController.getItemById(itemId); }
        catch (Exception ex) { root.getChildren().add(UIHelper.secondaryLabel("Gagal memuat detail alat.")); return root; }
        if (item == null) { root.getChildren().add(UIHelper.secondaryLabel("Alat tidak ditemukan.")); return root; }

        // Breadcrumb bar
        HBox breadBar = new HBox(6);
        breadBar.setPadding(new Insets(16, 60, 16, 60));
        breadBar.setAlignment(Pos.CENTER_LEFT);
        breadBar.setStyle("-fx-background-color: white; -fx-border-color: " + UIHelper.BORDER + "; -fx-border-width: 0 0 1 0;");
        Hyperlink exploreLink = new Hyperlink("Explore Items");
        exploreLink.setFont(UIHelper.regular(12));
        exploreLink.setStyle("-fx-text-fill: " + UIHelper.TEXT_GRAY + "; -fx-border-color: transparent;");
        exploreLink.setOnAction(e -> navigate.accept(MainView.CATALOGUE));
        Label a1 = UIHelper.secondaryLabel("›");
        Label a2 = UIHelper.secondaryLabel(item.getCategory() + " ›");
        Label cur = new Label(item.getTitle());
        cur.setFont(UIHelper.medium(12));
        cur.setTextFill(Color.web(UIHelper.TEXT_DARK));
        breadBar.getChildren().addAll(exploreLink, a1, a2, cur);

        // Main detail area
        HBox detail = new HBox(40);
        detail.setPadding(new Insets(40, 80, 60, 80));
        detail.setAlignment(Pos.TOP_LEFT);

        // ── Image area ───────────────────────────────────────────────────────
        StackPane imgBox = new StackPane();
        imgBox.setPrefSize(440, 340);
        imgBox.setMinSize(440, 340);
        String imgBg = UIHelper.categoryColor(item.getCategory());
        imgBox.setStyle("-fx-background-color: " + imgBg + "; -fx-background-radius: 20;");
        imgBox.setEffect(new DropShadow(16, 0, 4, Color.rgb(0,0,0,0.08)));

        Image itemImg = UIHelper.getItemImage(item.getTitle());
        if (itemImg != null) {
            ImageView iv = new ImageView(itemImg);
            iv.setFitWidth(440);
            iv.setFitHeight(340);
            iv.setPreserveRatio(false);
            iv.setSmooth(true);
            imgBox.getChildren().add(iv);
        } else {
            Label emoji = new Label(UIHelper.categoryEmoji(item.getCategory()));
            emoji.setFont(Font.font(110));
            imgBox.getChildren().add(emoji);
        }

        // ── Info panel ───────────────────────────────────────────────────────
        VBox info = new VBox(18);
        info.setPrefWidth(400);
        HBox.setHgrow(info, Priority.ALWAYS);

        Label titleLbl = new Label(item.getTitle());
        titleLbl.setFont(UIHelper.bold(28));
        titleLbl.setTextFill(Color.web(UIHelper.TEXT_DARK));
        titleLbl.setWrapText(true);

        HBox badges = new HBox(8);
        Label statusBadge = item.getStatus().equals("AVAILABLE") ? UIHelper.availableBadge() : UIHelper.unavailableBadge();
        Label catBadge = UIHelper.badge(item.getCategory(), UIHelper.categoryColor(item.getCategory()), UIHelper.TEXT_MID);
        Label condBadge = UIHelper.badge(item.getCondition(), UIHelper.LIGHT_BG, UIHelper.TEXT_GRAY);
        badges.getChildren().addAll(statusBadge, catBadge, condBadge);

        Label priceLbl = new Label(UIHelper.formatRupiah(item.getPrice()) + " / hari");
        priceLbl.setFont(UIHelper.bold(24));
        priceLbl.setTextFill(Color.web(UIHelper.BLUE));

        // Date picker
        Separator sep1 = new Separator();
        Label datesTitle = new Label("Pilih Tanggal Sewa");
        datesTitle.setFont(UIHelper.semibold(14));
        datesTitle.setTextFill(Color.web(UIHelper.TEXT_DARK));

        HBox dateRow = new HBox(16);
        dateRow.setAlignment(Pos.CENTER_LEFT);

        VBox fromBox = new VBox(6);
        Label fromLbl = UIHelper.secondaryLabel("Mulai");
        DatePicker fromPicker = new DatePicker(LocalDate.now());
        fromPicker.setPrefWidth(180);
        fromPicker.setStyle("-fx-font-size: 13;");
        fromBox.getChildren().addAll(fromLbl, fromPicker);

        VBox toBox = new VBox(6);
        Label toLbl = UIHelper.secondaryLabel("Selesai");
        DatePicker toPicker = new DatePicker(LocalDate.now().plusDays(1));
        toPicker.setPrefWidth(180);
        toPicker.setStyle("-fx-font-size: 13;");
        toBox.getChildren().addAll(toLbl, toPicker);

        dateRow.getChildren().addAll(fromBox, toBox);

        // Total cost
        Label totalLbl = new Label();
        totalLbl.setFont(UIHelper.semibold(14));
        totalLbl.setTextFill(Color.web(UIHelper.BLUE));

        Runnable updateTotal = () -> {
            LocalDate from = fromPicker.getValue();
            LocalDate to   = toPicker.getValue();
            if (from != null && to != null && to.isAfter(from)) {
                long days = ChronoUnit.DAYS.between(from, to);
                totalLbl.setText("Total: " + UIHelper.formatRupiah(days * item.getPrice()) + "  (" + days + " hari)");
            } else {
                totalLbl.setText("");
            }
        };
        fromPicker.setOnAction(e -> updateTotal.run());
        toPicker.setOnAction(e -> updateTotal.run());
        updateTotal.run();

        // Owner
        Separator sep2 = new Separator();
        HBox ownerRow = new HBox(10);
        ownerRow.setAlignment(Pos.CENTER_LEFT);
        Label ownerIcon = new Label("👤");
        ownerIcon.setFont(Font.font(18));
        Label ownerName = new Label(item.getOwnerName());
        ownerName.setFont(UIHelper.medium(13));
        ownerName.setTextFill(Color.web(UIHelper.TEXT_DARK));
        ownerRow.getChildren().addAll(ownerIcon, ownerName);

        // Description
        Label descTitle = new Label("Description");
        descTitle.setFont(UIHelper.semibold(14));
        descTitle.setTextFill(Color.web(UIHelper.TEXT_DARK));

        Label descText = new Label(item.getDescription() != null && !item.getDescription().isBlank()
            ? item.getDescription() : "Tidak ada deskripsi.");
        descText.setFont(UIHelper.regular(13));
        descText.setTextFill(Color.web(UIHelper.TEXT_MID));
        descText.setWrapText(true);
        descText.setMaxWidth(380);
        descText.setLineSpacing(4);

        // Rent button (UC17)
        Button rentBtn = UIHelper.primaryButton("🛒  Rent Now");
        rentBtn.setPrefWidth(380);
        rentBtn.setPrefHeight(50);
        rentBtn.setFont(UIHelper.semibold(15));

        if (!item.getStatus().equals("AVAILABLE")) {
            rentBtn.setDisable(true);
            rentBtn.setText("Alat Sedang Dipinjam");
            rentBtn.setStyle(rentBtn.getStyle() + "-fx-background-color: #9CA3AF;");
        } else {
            rentBtn.setOnAction(e -> handleRent(item, fromPicker.getValue(), toPicker.getValue()));
        }

        info.getChildren().addAll(titleLbl, badges, priceLbl, sep1, datesTitle, dateRow, totalLbl, sep2, ownerRow, descTitle, descText, rentBtn);
        detail.getChildren().addAll(imgBox, info);
        root.getChildren().addAll(breadBar, detail);
        return root;
    }

    private void handleRent(Item item, LocalDate from, LocalDate to) {
        if (from == null || to == null || !to.isAfter(from)) {
            UIHelper.showError("Pilih tanggal yang valid (tanggal selesai harus setelah tanggal mulai)."); return;
        }
        if (item.getOwnerId() == Session.getCurrentUser().getId()) {
            UIHelper.showError("Anda tidak bisa meminjam alat milik sendiri."); return;
        }
        long days  = ChronoUnit.DAYS.between(from, to);
        double total = days * item.getPrice();

        if (!UIHelper.showConfirm(
            "Konfirmasi peminjaman:\n\n" +
            "Alat     : " + item.getTitle() + "\n" +
            "Durasi   : " + days + " hari\n" +
            "Total    : " + UIHelper.formatRupiah(total) + "\n" +
            "Saldo    : " + UIHelper.formatRupiah(Session.getCurrentUser().getWalletBalance())
        )) return;

        try {
            WalletController.deductForRental(Session.getCurrentUser().getId(), total);
            WalletController.creditOwner(item.getOwnerId(), total);
            ItemController.updateStatus(item.getId(), "UNAVAILABLE");
            TransactionController.createTransaction(item.getId(), Session.getCurrentUser().getId(),
                item.getOwnerId(), from.toString(), to.toString(), total);
            Session.refreshBalance(WalletController.getBalance(Session.getCurrentUser().getId()));
            UIHelper.showAlert("Berhasil! 🎉", "Peminjaman berhasil!\nSaldo tersisa: " +
                UIHelper.formatRupiah(Session.getCurrentUser().getWalletBalance()));
            navigate.accept(MainView.TRANSACTIONS);
        } catch (IllegalStateException ex) {
            UIHelper.showError("Saldo tidak mencukupi untuk melakukan peminjaman.");
        } catch (Exception ex) {
            UIHelper.showError("Terjadi kesalahan. Coba lagi.");
        }
    }
}
