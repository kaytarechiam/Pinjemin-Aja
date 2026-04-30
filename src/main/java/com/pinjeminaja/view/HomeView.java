package com.pinjeminaja.view;

import com.pinjeminaja.controller.ItemController;
import com.pinjeminaja.model.Item;
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
import java.util.function.IntConsumer;

public class HomeView extends ScrollPane {

    private final Consumer<String> navigate;
    private final IntConsumer onViewDetail;

    public HomeView(Consumer<String> navigate, IntConsumer onViewDetail) {
        this.navigate     = navigate;
        this.onViewDetail = onViewDetail;
        setFitToWidth(true);
        setStyle("-fx-background-color: white; -fx-background: white;");
        setHbarPolicy(ScrollBarPolicy.NEVER);
        setContent(build());
    }

    private VBox build() {
        VBox root = new VBox(0);
        root.setStyle("-fx-background-color: " + UIHelper.LIGHT_BG + ";");
        root.getChildren().addAll(buildHero(), buildFeatures(), buildCatalogSection());
        return root;
    }

    // ── Hero ─────────────────────────────────────────────────────────────────
    private StackPane buildHero() {
        StackPane hero = new StackPane();
        hero.setPrefHeight(320);

        Rectangle heroBg = new Rectangle();
        heroBg.widthProperty().bind(hero.widthProperty());
        heroBg.setHeight(320);
        heroBg.setFill(new LinearGradient(0, 0, 1, 1, true, CycleMethod.NO_CYCLE,
            new Stop(0, Color.web("#EEF1FF")),
            new Stop(1, Color.web("#E0E7FF"))
        ));

        HBox content = new HBox(40);
        content.setPadding(new Insets(60, 80, 60, 80));
        content.setAlignment(Pos.CENTER_LEFT);

        VBox text = new VBox(16);
        text.setAlignment(Pos.CENTER_LEFT);
        text.setPrefWidth(500);

        HBox earnRow = new HBox(8);
        Label earn1 = new Label("Earn Effortlessly");
        earn1.setFont(UIHelper.bold(36));
        earn1.setTextFill(Color.web(UIHelper.BLUE));
        earnRow.getChildren().add(earn1);

        Label earn2 = new Label("from What You Already Own");
        earn2.setFont(UIHelper.bold(36));
        earn2.setTextFill(Color.web(UIHelper.TEXT_DARK));
        earn2.setWrapText(true);

        Label sub = new Label("Turn your unused products into effortless income.\nList Now. Earn Smarter.");
        sub.setFont(UIHelper.regular(15));
        sub.setTextFill(Color.web(UIHelper.TEXT_MID));
        sub.setLineSpacing(4);

        Button listBtn = UIHelper.primaryButton("📦  List Your Product");
        listBtn.setPrefHeight(46);
        listBtn.setPrefWidth(200);
        listBtn.setOnAction(e -> navigate.accept(MainView.MY_ITEMS));

        text.getChildren().addAll(earn1, earn2, sub, listBtn);

        // Decorative emoji grid on the right
        FlowPane emojiGrid = new FlowPane(10, 10);
        emojiGrid.setPrefWidth(200);
        emojiGrid.setPrefHeight(200);
        String[] emojis = {"🍳","🔧","🧹","💡","🌱","🔨","🧺","🪴"};
        for (String em : emojis) {
            StackPane tile = new StackPane();
            tile.setPrefSize(80, 80);
            tile.setStyle("-fx-background-color: white; -fx-background-radius: 16;");
            tile.setEffect(new DropShadow(8, 0, 2, Color.rgb(0,0,0,0.06)));
            Label lbl = new Label(em);
            lbl.setFont(Font.font(28));
            tile.getChildren().add(lbl);
            emojiGrid.getChildren().add(tile);
        }

        content.getChildren().addAll(text, UIHelper.spacer(), emojiGrid);
        hero.getChildren().addAll(heroBg, content);
        return hero;
    }

    // ── Feature cards ─────────────────────────────────────────────────────────
    private HBox buildFeatures() {
        HBox row = new HBox(20);
        row.setPadding(new Insets(40, 80, 20, 80));
        row.setAlignment(Pos.CENTER);
        row.setStyle("-fx-background-color: " + UIHelper.LIGHT_BG + ";");
        row.getChildren().addAll(
            featureCard("🌱", "Eco-Friendly Sharing",
                "Borrow instead of buying. Reduce waste and help build a greener spirit."),
            featureCard("🤝", "Stronger Community",
                "Connect with your neighbors. Sharing items builds trust and a closer neighborhood."),
            featureCard("💰", "Smart Savings",
                "Save money and space. Just borrow the tools you rarely use.")
        );
        return row;
    }

    private VBox featureCard(String emoji, String title, String desc) {
        VBox card = new VBox(12);
        card.setPadding(new Insets(24));
        card.setStyle(
            "-fx-background-color: white;" +
            "-fx-background-radius: 16;" +
            "-fx-border-radius: 16;" +
            "-fx-border-color: " + UIHelper.BORDER + ";" +
            "-fx-border-width: 1;"
        );
        card.setEffect(new DropShadow(10, 0, 3, Color.rgb(0,0,0,0.05)));
        HBox.setHgrow(card, Priority.ALWAYS);

        Label em = new Label(emoji);
        em.setFont(Font.font(32));

        Label t = new Label(title);
        t.setFont(UIHelper.semibold(14));
        t.setTextFill(Color.web(UIHelper.TEXT_DARK));

        Label d = new Label(desc);
        d.setFont(UIHelper.regular(12));
        d.setTextFill(Color.web(UIHelper.TEXT_GRAY));
        d.setWrapText(true);
        d.setLineSpacing(3);

        card.getChildren().addAll(em, t, d);
        return card;
    }

    // ── Catalog section ────────────────────────────────────────────────────────
    private VBox buildCatalogSection() {
        VBox section = new VBox(20);
        section.setPadding(new Insets(20, 80, 60, 80));
        section.setStyle("-fx-background-color: " + UIHelper.LIGHT_BG + ";");

        HBox header = new HBox();
        header.setAlignment(Pos.CENTER_LEFT);
        Label title = UIHelper.heading("Most Borrowed");

        Button exploreBtn = UIHelper.outlineButton("Explore All →");
        exploreBtn.setPrefHeight(36);
        exploreBtn.setFont(UIHelper.medium(12));
        exploreBtn.setOnAction(e -> navigate.accept(MainView.CATALOGUE));

        header.getChildren().addAll(title, UIHelper.spacer(), exploreBtn);

        FlowPane grid = new FlowPane();
        grid.setHgap(20);
        grid.setVgap(20);
        grid.setPrefWrapLength(900);

        try {
            List<Item> items = ItemController.getAllItems();
            int count = Math.min(items.size(), 8);
            for (int i = 0; i < count; i++) {
                int finalI = i;
                grid.getChildren().add(UIHelper.itemCard(items.get(i), () -> onViewDetail.accept(items.get(finalI).getId())));
            }
            if (items.isEmpty()) {
                Label empty = UIHelper.secondaryLabel("Belum ada alat tersedia. Jadilah yang pertama mendaftarkan!");
                grid.getChildren().add(empty);
            }
        } catch (Exception ex) {
            grid.getChildren().add(UIHelper.secondaryLabel("Gagal memuat katalog."));
        }

        section.getChildren().addAll(header, grid);
        return section;
    }
}
