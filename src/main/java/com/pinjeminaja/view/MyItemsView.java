package com.pinjeminaja.view;

import com.pinjeminaja.Session;
import com.pinjeminaja.controller.ItemController;
import com.pinjeminaja.controller.TransactionController;
import com.pinjeminaja.controller.WalletController;
import com.pinjeminaja.model.Item;
import com.pinjeminaja.model.Transaction;
import javafx.geometry.Insets;
import javafx.geometry.Pos;
import javafx.scene.control.*;
import javafx.scene.control.cell.PropertyValueFactory;
import javafx.scene.layout.*;
import javafx.scene.paint.Color;
import javafx.scene.text.FontWeight;
import javafx.scene.text.Font;

import java.util.List;
import java.util.function.Consumer;

// UC10: Katalog Saya, UC11: Tambah, UC12: Hapus, UC13: Edit, UC18: Konfirmasi Pengembalian
public class MyItemsView extends BorderPane {

    private final Consumer<String> navigate;
    private boolean showItems = true;

    private BorderPane contentPane;
    private Button itemsTabBtn;
    private Button rentersTabBtn;

    public MyItemsView(Consumer<String> navigate) {
        this.navigate = navigate;
        build();
    }

    private void build() {
        setStyle("-fx-background-color: " + UIHelper.LIGHT_BG + ";");

        // Left sidebar
        VBox sidebar = new VBox(4);
        sidebar.setPrefWidth(200);
        sidebar.setPadding(new Insets(30, 16, 30, 16));
        sidebar.setStyle("-fx-background-color: white; -fx-border-color: " + UIHelper.BORDER + "; -fx-border-width: 0 1 0 0;");

        Label logo = new Label("Pinjemin Aja!");
        logo.setFont(Font.font("System", FontWeight.BOLD, 16));
        logo.setPadding(new Insets(0, 0, 20, 8));

        itemsTabBtn = sidebarBtn("Items", true);
        rentersTabBtn = sidebarBtn("Renters", false);

        itemsTabBtn.setOnAction(e -> { showItems = true; setActiveTab(); loadItemsTab(); });
        rentersTabBtn.setOnAction(e -> { showItems = false; setActiveTab(); loadRentersTab(); });

        sidebar.getChildren().addAll(logo, itemsTabBtn, rentersTabBtn);

        contentPane = new BorderPane();
        contentPane.setStyle("-fx-background-color: " + UIHelper.LIGHT_BG + ";");

        setLeft(sidebar);
        setCenter(contentPane);

        loadItemsTab();
    }

    private Button sidebarBtn(String text, boolean active) {
        Button btn = new Button(text);
        btn.setPrefWidth(168);
        btn.setPrefHeight(40);
        String activeStyle = "-fx-background-color: " + UIHelper.LIGHT_BG + "; -fx-text-fill: " + UIHelper.BLUE + "; -fx-font-weight: bold; -fx-alignment: CENTER_LEFT; -fx-padding: 8 16; -fx-background-radius: 8; -fx-cursor: hand; -fx-font-size: 13;";
        String normalStyle = "-fx-background-color: transparent; -fx-text-fill: #374151; -fx-alignment: CENTER_LEFT; -fx-padding: 8 16; -fx-background-radius: 8; -fx-cursor: hand; -fx-font-size: 13;";
        btn.setStyle(active ? activeStyle : normalStyle);
        return btn;
    }

    private void setActiveTab() {
        String activeStyle = "-fx-background-color: " + UIHelper.LIGHT_BG + "; -fx-text-fill: " + UIHelper.BLUE + "; -fx-font-weight: bold; -fx-alignment: CENTER_LEFT; -fx-padding: 8 16; -fx-background-radius: 8; -fx-cursor: hand; -fx-font-size: 13;";
        String normalStyle = "-fx-background-color: transparent; -fx-text-fill: #374151; -fx-alignment: CENTER_LEFT; -fx-padding: 8 16; -fx-background-radius: 8; -fx-cursor: hand; -fx-font-size: 13;";
        itemsTabBtn.setStyle(showItems ? activeStyle : normalStyle);
        rentersTabBtn.setStyle(!showItems ? activeStyle : normalStyle);
    }

    // UC10: Melihat Katalog Saya — Items tab
    private void loadItemsTab() {
        VBox content = new VBox(0);
        content.setPadding(new Insets(30));
        content.setStyle("-fx-background-color: " + UIHelper.LIGHT_BG + ";");

        VBox card = new VBox(16);
        card.setPadding(new Insets(24));
        card.setStyle("-fx-background-color: white; -fx-background-radius: 10;");

        // Header row
        HBox header = new HBox(16);
        header.setAlignment(Pos.CENTER_LEFT);
        Label title = UIHelper.heading("My Items");

        Button addBtn = UIHelper.primaryButton("Add Item");
        addBtn.setOnAction(e -> contentPane.setCenter(
            new AddEditProductView(null, this::loadItemsTab, this::loadItemsTab)
        ));

        TextField searchField = UIHelper.styledTextField("Search");
        searchField.setPrefWidth(200);

        header.getChildren().addAll(title, UIHelper.spacer(), addBtn, searchField);

        // Table
        TableView<Item> table = buildItemsTable();
        loadItemsData(table, searchField);

        searchField.setOnAction(e -> loadItemsData(table, searchField));

        card.getChildren().addAll(header, table);
        content.getChildren().add(card);
        contentPane.setCenter(content);
    }

    @SuppressWarnings("unchecked")
    private TableView<Item> buildItemsTable() {
        TableView<Item> table = new TableView<>();
        table.setStyle("-fx-font-size: 13;");
        table.setColumnResizePolicy(TableView.CONSTRAINED_RESIZE_POLICY);

        TableColumn<Item, String> nameCol = new TableColumn<>("Name");
        nameCol.setCellValueFactory(d -> new javafx.beans.property.SimpleStringProperty(d.getValue().getTitle()));

        TableColumn<Item, String> catCol = new TableColumn<>("Category");
        catCol.setCellValueFactory(d -> new javafx.beans.property.SimpleStringProperty(d.getValue().getCategory()));
        catCol.setPrefWidth(100);

        TableColumn<Item, String> descCol = new TableColumn<>("Description");
        descCol.setCellValueFactory(d -> new javafx.beans.property.SimpleStringProperty(
            d.getValue().getDescription() != null ? d.getValue().getDescription() : "-"
        ));

        TableColumn<Item, String> priceCol = new TableColumn<>("Price");
        priceCol.setCellValueFactory(d -> new javafx.beans.property.SimpleStringProperty(
            UIHelper.formatRupiah(d.getValue().getPrice())
        ));
        priceCol.setPrefWidth(110);

        TableColumn<Item, String> condCol = new TableColumn<>("Condition");
        condCol.setCellValueFactory(d -> new javafx.beans.property.SimpleStringProperty(d.getValue().getCondition()));
        condCol.setPrefWidth(110);

        TableColumn<Item, Void> actionCol = new TableColumn<>("Action");
        actionCol.setPrefWidth(90);
        actionCol.setCellFactory(col -> new TableCell<>() {
            private final MenuButton menu = new MenuButton("•••");
            {
                menu.setStyle("-fx-background-color: transparent; -fx-font-size: 16; -fx-cursor: hand;");
                MenuItem editItem = new MenuItem("Edit");
                editItem.setOnAction(e -> {
                    Item item = getTableView().getItems().get(getIndex());
                    contentPane.setCenter(new AddEditProductView(item, () -> loadItemsTab(), () -> loadItemsTab()));
                });
                MenuItem removeItem = new MenuItem("Remove");
                removeItem.setStyle("-fx-text-fill: #EF4444;");
                removeItem.setOnAction(e -> {
                    Item item = getTableView().getItems().get(getIndex());
                    if (UIHelper.showConfirm("Hapus alat \"" + item.getTitle() + "\"?")) {
                        try {
                            ItemController.deleteItem(item.getId());
                            loadItemsTab();
                        } catch (Exception ex) {
                            UIHelper.showError("Gagal menghapus alat.");
                        }
                    }
                });
                menu.getItems().addAll(editItem, removeItem);
            }
            @Override protected void updateItem(Void v, boolean empty) {
                super.updateItem(v, empty);
                setGraphic(empty ? null : menu);
            }
        });

        table.getColumns().addAll(nameCol, catCol, descCol, priceCol, condCol, actionCol);
        table.setPrefHeight(500);
        return table;
    }

    private void loadItemsData(TableView<Item> table, TextField searchField) {
        try {
            String kw = searchField.getText().trim();
            List<Item> items = kw.isEmpty()
                ? ItemController.getMyItems(Session.getCurrentUser().getId())
                : ItemController.getMyItems(Session.getCurrentUser().getId()).stream()
                    .filter(i -> i.getTitle().toLowerCase().contains(kw.toLowerCase()))
                    .toList();
            table.getItems().setAll(items);
        } catch (Exception ex) {
            UIHelper.showError("Gagal memuat data alat.");
        }
    }

    // UC18 (penyedia): Konfirmasi Pengembalian — Renters tab
    private void loadRentersTab() {
        VBox content = new VBox(0);
        content.setPadding(new Insets(30));

        VBox card = new VBox(16);
        card.setPadding(new Insets(24));
        card.setStyle("-fx-background-color: white; -fx-background-radius: 10;");

        HBox header = new HBox(16);
        header.setAlignment(Pos.CENTER_LEFT);
        Label title = UIHelper.heading("My Items");
        TextField searchField = UIHelper.styledTextField("Search");
        searchField.setPrefWidth(200);
        header.getChildren().addAll(title, UIHelper.spacer(), searchField);

        TableView<Transaction> table = buildRentersTable();
        loadRentersData(table);

        card.getChildren().addAll(header, table);
        content.getChildren().add(card);
        contentPane.setCenter(content);
    }

    @SuppressWarnings("unchecked")
    private TableView<Transaction> buildRentersTable() {
        TableView<Transaction> table = new TableView<>();
        table.setStyle("-fx-font-size: 13;");
        table.setColumnResizePolicy(TableView.CONSTRAINED_RESIZE_POLICY);

        TableColumn<Transaction, String> nameCol = new TableColumn<>("Name");
        nameCol.setCellValueFactory(d -> new javafx.beans.property.SimpleStringProperty(d.getValue().getItemTitle()));

        TableColumn<Transaction, String> renterCol = new TableColumn<>("Renter");
        renterCol.setCellValueFactory(d -> new javafx.beans.property.SimpleStringProperty(d.getValue().getRenterName()));
        renterCol.setPrefWidth(100);

        TableColumn<Transaction, String> pickupCol = new TableColumn<>("Pick-up Date");
        pickupCol.setCellValueFactory(d -> new javafx.beans.property.SimpleStringProperty(d.getValue().getStartDate()));
        pickupCol.setPrefWidth(110);

        TableColumn<Transaction, String> returnCol = new TableColumn<>("Return Date");
        returnCol.setCellValueFactory(d -> new javafx.beans.property.SimpleStringProperty(d.getValue().getEndDate()));
        returnCol.setPrefWidth(110);

        TableColumn<Transaction, String> priceCol = new TableColumn<>("Price");
        priceCol.setCellValueFactory(d -> new javafx.beans.property.SimpleStringProperty(
            UIHelper.formatRupiah(d.getValue().getTotalPrice())
        ));
        priceCol.setPrefWidth(100);

        TableColumn<Transaction, String> statusCol = new TableColumn<>("Status");
        statusCol.setCellValueFactory(d -> new javafx.beans.property.SimpleStringProperty(d.getValue().getStatus()));
        statusCol.setPrefWidth(90);

        TableColumn<Transaction, Void> confirmCol = new TableColumn<>("Confirm Return");
        confirmCol.setPrefWidth(140);
        confirmCol.setCellFactory(col -> new TableCell<>() {
            private final Button btn = new Button("Returned");
            {
                btn.setStyle("-fx-background-color: " + UIHelper.BLUE + "; -fx-text-fill: white; -fx-background-radius: 6; -fx-cursor: hand; -fx-font-size: 12;");
            }
            @Override protected void updateItem(Void v, boolean empty) {
                super.updateItem(v, empty);
                if (empty) { setGraphic(null); return; }
                Transaction t = getTableView().getItems().get(getIndex());
                if ("COMPLETED".equals(t.getStatus())) {
                    btn.setStyle("-fx-background-color: #9CA3AF; -fx-text-fill: white; -fx-background-radius: 6; -fx-font-size: 12;");
                    btn.setDisable(true);
                } else {
                    btn.setDisable(false);
                    btn.setStyle("-fx-background-color: " + UIHelper.BLUE + "; -fx-text-fill: white; -fx-background-radius: 6; -fx-cursor: hand; -fx-font-size: 12;");
                }
                btn.setOnAction(e -> {
                    if (UIHelper.showConfirm("Konfirmasi barang \"" + t.getItemTitle() + "\" sudah diterima kembali?")) {
                        try {
                            TransactionController.confirmReturn(t.getId());
                            loadRentersData(getTableView());
                        } catch (Exception ex) {
                            UIHelper.showError("Gagal mengonfirmasi pengembalian.");
                        }
                    }
                });
                setGraphic(btn);
            }
        });

        table.getColumns().addAll(nameCol, renterCol, pickupCol, returnCol, priceCol, statusCol, confirmCol);
        table.setPrefHeight(500);
        return table;
    }

    private void loadRentersData(TableView<Transaction> table) {
        try {
            List<Transaction> txns = TransactionController.getLendingHistory(Session.getCurrentUser().getId());
            table.getItems().setAll(txns);
        } catch (Exception ex) {
            UIHelper.showError("Gagal memuat data penyewa.");
        }
    }
}
