package com.pinjeminaja.view;

import com.pinjeminaja.Session;
import com.pinjeminaja.controller.TransactionController;
import com.pinjeminaja.model.Transaction;
import javafx.geometry.Insets;
import javafx.geometry.Pos;
import javafx.scene.control.*;
import javafx.scene.layout.*;
import javafx.scene.paint.Color;

import java.util.List;

// UC19: Melihat Riwayat Transaksi, UC20: Filter Jenis Riwayat, UC21: Melihat Detail Transaksi, UC18 (peminjam)
public class TransactionHistoryView extends VBox {

    private TableView<Transaction> table;
    private ComboBox<String> filterBox;
    private VBox detailPanel;

    public TransactionHistoryView() {
        build();
    }

    private void build() {
        setStyle("-fx-background-color: " + UIHelper.LIGHT_BG + ";");
        setPadding(new Insets(30));
        setSpacing(16);

        Label title = UIHelper.heading("Transaction History");

        // UC20: Filter Jenis Riwayat
        HBox filterRow = new HBox(16);
        filterRow.setAlignment(Pos.CENTER_LEFT);

        Label filterLabel = UIHelper.label("Filter Transaksi:");
        filterBox = new ComboBox<>();
        filterBox.getItems().addAll("Semua", "Riwayat Peminjaman", "Barang yang Dipinjam");
        filterBox.setValue("Semua");
        filterBox.setStyle("-fx-font-size: 13;");
        filterBox.setOnAction(e -> loadData());

        filterRow.getChildren().addAll(filterLabel, filterBox);

        // Table
        VBox tableCard = new VBox(0);
        tableCard.setStyle("-fx-background-color: white; -fx-background-radius: 10;");
        tableCard.setPadding(new Insets(20));

        table = buildTable();
        tableCard.getChildren().add(table);

        // UC21: Detail panel (shown on row click)
        detailPanel = new VBox(12);
        detailPanel.setPadding(new Insets(20));
        detailPanel.setStyle("-fx-background-color: white; -fx-background-radius: 10;");
        detailPanel.setVisible(false);
        detailPanel.setManaged(false);

        getChildren().addAll(title, filterRow, tableCard, detailPanel);
        loadData();
    }

    @SuppressWarnings("unchecked")
    private TableView<Transaction> buildTable() {
        TableView<Transaction> tbl = new TableView<>();
        tbl.setStyle("-fx-font-size: 13;");
        tbl.setColumnResizePolicy(TableView.CONSTRAINED_RESIZE_POLICY);
        tbl.setPrefHeight(400);

        TableColumn<Transaction, String> itemCol = new TableColumn<>("Alat");
        itemCol.setCellValueFactory(d -> new javafx.beans.property.SimpleStringProperty(d.getValue().getItemTitle()));

        TableColumn<Transaction, String> roleCol = new TableColumn<>("Peran");
        roleCol.setPrefWidth(90);
        roleCol.setCellValueFactory(d -> new javafx.beans.property.SimpleStringProperty(
            d.getValue().getRenterId() == Session.getCurrentUser().getId() ? "Peminjam" : "Penyedia"
        ));

        TableColumn<Transaction, String> counterpartyCol = new TableColumn<>("Pihak Lain");
        counterpartyCol.setCellValueFactory(d -> {
            Transaction t = d.getValue();
            boolean isRenter = t.getRenterId() == Session.getCurrentUser().getId();
            return new javafx.beans.property.SimpleStringProperty(isRenter ? t.getOwnerName() : t.getRenterName());
        });

        TableColumn<Transaction, String> startCol = new TableColumn<>("Tgl Mulai");
        startCol.setCellValueFactory(d -> new javafx.beans.property.SimpleStringProperty(d.getValue().getStartDate()));
        startCol.setPrefWidth(100);

        TableColumn<Transaction, String> endCol = new TableColumn<>("Tgl Selesai");
        endCol.setCellValueFactory(d -> new javafx.beans.property.SimpleStringProperty(d.getValue().getEndDate()));
        endCol.setPrefWidth(100);

        TableColumn<Transaction, String> priceCol = new TableColumn<>("Total");
        priceCol.setCellValueFactory(d -> new javafx.beans.property.SimpleStringProperty(
            UIHelper.formatRupiah(d.getValue().getTotalPrice())
        ));
        priceCol.setPrefWidth(110);

        TableColumn<Transaction, String> statusCol = new TableColumn<>("Status");
        statusCol.setPrefWidth(90);
        statusCol.setCellFactory(col -> new TableCell<>() {
            @Override protected void updateItem(String v, boolean empty) {
                super.updateItem(v, empty);
                if (empty || getTableRow() == null || getTableRow().getItem() == null) { setGraphic(null); return; }
                Transaction t = (Transaction) getTableRow().getItem();
                Label badge = "COMPLETED".equals(t.getStatus())
                    ? UIHelper.badge("Selesai", "#D1FAE5", "#065F46")
                    : UIHelper.badge("Ongoing", "#FEF3C7", "#92400E");
                setGraphic(badge);
            }
        });

        tbl.getColumns().addAll(itemCol, roleCol, counterpartyCol, startCol, endCol, priceCol, statusCol);

        // UC21: Click row to see detail
        tbl.setRowFactory(tv -> {
            TableRow<Transaction> row = new TableRow<>();
            row.setOnMouseClicked(e -> {
                if (!row.isEmpty()) showDetail(row.getItem());
            });
            return row;
        });

        return tbl;
    }

    private void loadData() {
        try {
            String filter = filterBox.getValue();
            List<Transaction> txns;
            int uid = Session.getCurrentUser().getId();
            if ("Riwayat Peminjaman".equals(filter)) {
                txns = TransactionController.getRentalHistory(uid);
            } else if ("Barang yang Dipinjam".equals(filter)) {
                txns = TransactionController.getLendingHistory(uid);
            } else {
                txns = TransactionController.getAllTransactions(uid);
            }
            table.getItems().setAll(txns);
            hideDetail();
        } catch (Exception ex) {
            UIHelper.showError("Gagal memuat riwayat transaksi.");
        }
    }

    // UC21: Melihat Detail Transaksi
    private void showDetail(Transaction t) {
        detailPanel.getChildren().clear();

        Label title = UIHelper.subheading("Detail Transaksi");

        boolean isRenter = t.getRenterId() == Session.getCurrentUser().getId();

        GridPane grid = new GridPane();
        grid.setHgap(20);
        grid.setVgap(10);

        addDetailRow(grid, 0, "Alat", t.getItemTitle());
        addDetailRow(grid, 1, "Peran", isRenter ? "Peminjam" : "Penyedia");
        addDetailRow(grid, 2, isRenter ? "Penyedia" : "Peminjam", isRenter ? t.getOwnerName() : t.getRenterName());
        addDetailRow(grid, 3, "Tanggal Mulai", t.getStartDate());
        addDetailRow(grid, 4, "Tanggal Selesai", t.getEndDate());
        addDetailRow(grid, 5, "Total Biaya", UIHelper.formatRupiah(t.getTotalPrice()));
        addDetailRow(grid, 6, "Status", t.getStatus());
        addDetailRow(grid, 7, "Waktu Transaksi", t.getCreatedAt());

        detailPanel.getChildren().addAll(title, grid);

        // UC18 (peminjam): Tombol "Konfirmasi Pengembalian" jika status ONGOING dan user adalah peminjam
        if (isRenter && "ONGOING".equals(t.getStatus())) {
            Button confirmBtn = UIHelper.primaryButton("Konfirmasi Pengembalian");
            confirmBtn.setOnAction(e -> {
                if (UIHelper.showConfirm("Konfirmasi bahwa Anda telah mengembalikan alat \"" + t.getItemTitle() + "\" kepada penyedia?")) {
                    UIHelper.showAlert("Menunggu Konfirmasi", "Permintaan pengembalian dikirim ke penyedia alat. Penyedia perlu mengonfirmasi penerimaan barang melalui menu My Items > Renters.");
                }
            });
            detailPanel.getChildren().add(confirmBtn);
        }

        Button closeBtn = UIHelper.outlineButton("Tutup");
        closeBtn.setOnAction(e -> hideDetail());
        detailPanel.getChildren().add(closeBtn);

        detailPanel.setVisible(true);
        detailPanel.setManaged(true);
    }

    private void addDetailRow(GridPane grid, int row, String key, String value) {
        Label keyLbl = UIHelper.label(key + ":");
        keyLbl.setFont(UIHelper.semibold(13));
        keyLbl.setMinWidth(140);
        Label valLbl = UIHelper.label(value != null ? value : "-");
        grid.add(keyLbl, 0, row);
        grid.add(valLbl, 1, row);
    }

    private void hideDetail() {
        detailPanel.setVisible(false);
        detailPanel.setManaged(false);
    }
}
