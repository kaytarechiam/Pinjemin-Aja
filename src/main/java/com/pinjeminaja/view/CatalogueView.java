package com.pinjeminaja.view;

import com.pinjeminaja.controller.ItemController;
import com.pinjeminaja.model.Item;
import javafx.geometry.Insets;
import javafx.geometry.Pos;
import javafx.scene.control.*;
import javafx.scene.effect.DropShadow;
import javafx.scene.layout.*;
import javafx.scene.paint.Color;
import javafx.scene.text.*;

import java.util.List;
import java.util.function.Consumer;
import java.util.function.IntConsumer;

// UC09, UC14, UC15
public class CatalogueView extends HBox {

    private static final String[] CATEGORIES = {"Cleaning", "Electronics", "Kitchen", "Tools", "Gardening"};

    private final Consumer<String> navigate;
    private final IntConsumer onViewDetail;
    private String selectedCategory;

    private FlowPane grid;
    private TextField searchField;
    private ToggleGroup categoryGroup;

    public CatalogueView(String initialKeyword, String initialCategory, Consumer<String> navigate, IntConsumer onViewDetail) {
        this.navigate         = navigate;
        this.onViewDetail     = onViewDetail;
        this.selectedCategory = initialCategory != null ? initialCategory : "";
        this.searchField      = UIHelper.styledTextField("Search products...");
        if (initialKeyword != null) searchField.setText(initialKeyword);
        build();
    }

    private void build() {
        setStyle("-fx-background-color: " + UIHelper.LIGHT_BG + ";");
        setMinHeight(600);

        // ── Sidebar ──────────────────────────────────────────────────────────
        VBox sidebar = new VBox(8);
        sidebar.setPrefWidth(210);
        sidebar.setPadding(new Insets(28, 18, 28, 24));
        sidebar.setStyle("-fx-background-color: white; -fx-border-color: " + UIHelper.BORDER + "; -fx-border-width: 0 1 0 0;");

        Label catTitle = new Label("Categories");
        catTitle.setFont(UIHelper.semibold(13));
        catTitle.setTextFill(Color.web(UIHelper.TEXT_DARK));
        catTitle.setPadding(new Insets(0, 0, 8, 0));
        sidebar.getChildren().add(catTitle);

        categoryGroup = new ToggleGroup();

        RadioButton allBtn = categoryRadio("All", "");
        allBtn.setSelected(selectedCategory.isEmpty());
        sidebar.getChildren().add(allBtn);

        for (String cat : CATEGORIES) {
            RadioButton rb = categoryRadio(UIHelper.categoryEmoji(cat) + "  " + cat, cat);
            rb.setSelected(cat.equals(selectedCategory));
            sidebar.getChildren().add(rb);
        }

        // ── Main content ─────────────────────────────────────────────────────
        VBox content = new VBox(0);
        HBox.setHgrow(content, Priority.ALWAYS);
        content.setStyle("-fx-background-color: " + UIHelper.LIGHT_BG + ";");

        // Top bar: breadcrumb + search
        HBox topBar = new HBox(16);
        topBar.setPadding(new Insets(20, 28, 16, 28));
        topBar.setAlignment(Pos.CENTER_LEFT);
        topBar.setStyle("-fx-background-color: white; -fx-border-color: " + UIHelper.BORDER + "; -fx-border-width: 0 0 1 0;");

        HBox breadcrumb = new HBox(6);
        breadcrumb.setAlignment(Pos.CENTER_LEFT);
        Hyperlink homeLink = new Hyperlink("Home");
        homeLink.setFont(UIHelper.regular(12));
        homeLink.setStyle("-fx-text-fill: " + UIHelper.TEXT_GRAY + "; -fx-border-color: transparent;");
        homeLink.setOnAction(e -> navigate.accept(MainView.HOME));
        Label arr = UIHelper.secondaryLabel("›");
        Label cur = new Label("Explore Items");
        cur.setFont(UIHelper.medium(12));
        cur.setTextFill(Color.web(UIHelper.TEXT_DARK));
        breadcrumb.getChildren().addAll(homeLink, arr, cur);

        searchField.setPrefWidth(260);
        searchField.setPrefHeight(38);
        searchField.setOnAction(e -> applyFilter());

        Button searchBtn = UIHelper.primaryButton("Search");
        searchBtn.setPrefHeight(38);
        searchBtn.setFont(UIHelper.medium(12));
        searchBtn.setOnAction(e -> applyFilter());

        topBar.getChildren().addAll(breadcrumb, UIHelper.spacer(), searchField, searchBtn);

        // Grid
        ScrollPane scrollPane = new ScrollPane();
        scrollPane.setFitToWidth(true);
        scrollPane.setHbarPolicy(ScrollPane.ScrollBarPolicy.NEVER);
        scrollPane.setStyle("-fx-background-color: " + UIHelper.LIGHT_BG + "; -fx-background: " + UIHelper.LIGHT_BG + ";");

        VBox gridWrapper = new VBox(16);
        gridWrapper.setPadding(new Insets(24, 28, 32, 28));

        grid = new FlowPane();
        grid.setHgap(20);
        grid.setVgap(20);
        grid.setPrefWrapLength(700);

        gridWrapper.getChildren().add(grid);
        scrollPane.setContent(gridWrapper);
        VBox.setVgrow(scrollPane, Priority.ALWAYS);

        content.getChildren().addAll(topBar, scrollPane);
        getChildren().addAll(sidebar, content);

        loadItems();
    }

    private RadioButton categoryRadio(String text, String value) {
        RadioButton rb = new RadioButton(text);
        rb.setToggleGroup(categoryGroup);
        rb.setFont(UIHelper.regular(13));
        rb.setStyle("-fx-padding: 6 8; -fx-cursor: hand;");
        rb.setOnAction(e -> { selectedCategory = value; applyFilter(); });
        return rb;
    }

    private void applyFilter() {
        loadItemsFiltered(searchField.getText().trim(), selectedCategory);
    }

    private void loadItems() {
        loadItemsFiltered(searchField.getText().trim(), selectedCategory);
    }

    private void loadItemsFiltered(String keyword, String category) {
        grid.getChildren().clear();
        try {
            List<Item> items = ItemController.searchAndFilter(keyword, category);
            if (items.isEmpty()) {
                VBox empty = new VBox(12);
                empty.setAlignment(Pos.CENTER);
                empty.setPadding(new Insets(60));
                Label em = new Label("🔍");
                em.setFont(Font.font(48));
                Label msg = UIHelper.secondaryLabel("Tidak ada alat yang sesuai dengan pencarian atau kategori.");
                msg.setFont(UIHelper.regular(14));
                empty.getChildren().addAll(em, msg);
                grid.getChildren().add(empty);
            } else {
                for (Item item : items) {
                    grid.getChildren().add(UIHelper.itemCard(item, () -> onViewDetail.accept(item.getId())));
                }
            }
        } catch (Exception ex) {
            grid.getChildren().add(UIHelper.secondaryLabel("Gagal memuat katalog."));
        }
    }
}
