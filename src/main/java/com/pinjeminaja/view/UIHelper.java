package com.pinjeminaja.view;

import javafx.geometry.Insets;
import javafx.geometry.Pos;
import javafx.scene.control.*;
import javafx.scene.effect.DropShadow;
import javafx.scene.image.Image;
import javafx.scene.image.ImageView;
import javafx.scene.layout.*;
import javafx.scene.paint.Color;
import javafx.scene.text.*;

import java.io.InputStream;
import java.util.Map;

public class UIHelper {

    public static final String BLUE       = "#3D5AF1";
    public static final String BLUE_DARK  = "#2D46D6";
    public static final String BLUE_LIGHT = "#EEF1FF";
    public static final String LIGHT_BG   = "#F7F8FC";
    public static final String BORDER     = "#E8EAF0";
    public static final String TEXT_DARK  = "#1A1D2E";
    public static final String TEXT_MID   = "#4B5563";
    public static final String TEXT_GRAY  = "#9CA3AF";
    public static final String WHITE      = "#FFFFFF";
    public static final String GREEN      = "#10B981";
    public static final String RED        = "#EF4444";

    // ── Fonts ────────────────────────────────────────────────────────────────

    private static boolean fontsLoaded = false;

    public static void loadFonts() {
        if (fontsLoaded) return;
        try {
            Font.loadFont(UIHelper.class.getResourceAsStream("/fonts/Poppins-Regular.ttf"),  13);
            Font.loadFont(UIHelper.class.getResourceAsStream("/fonts/Poppins-Medium.ttf"),   13);
            Font.loadFont(UIHelper.class.getResourceAsStream("/fonts/Poppins-SemiBold.ttf"), 13);
            Font.loadFont(UIHelper.class.getResourceAsStream("/fonts/Poppins-Bold.ttf"),     13);
            fontsLoaded = true;
        } catch (Exception e) {
            System.err.println("Poppins not loaded, falling back to system font.");
        }
    }

    public static Font regular(double size)  { return Font.font("Poppins", FontWeight.NORMAL, size); }
    public static Font medium(double size)   { return Font.font("Poppins", FontWeight.MEDIUM, size); }
    public static Font semibold(double size) { return Font.font("Poppins", FontWeight.SEMI_BOLD, size); }
    public static Font bold(double size)     { return Font.font("Poppins", FontWeight.BOLD, size); }

    // ── Input fields ─────────────────────────────────────────────────────────

    public static TextField styledTextField(String prompt) {
        TextField tf = new TextField();
        tf.setPromptText(prompt);
        tf.setFont(regular(13));
        tf.setStyle(inputStyle());
        tf.setPrefHeight(42);
        addFocusEffect(tf);
        return tf;
    }

    public static PasswordField styledPasswordField(String prompt) {
        PasswordField pf = new PasswordField();
        pf.setPromptText(prompt);
        pf.setFont(regular(13));
        pf.setStyle(inputStyle());
        pf.setPrefHeight(42);
        addFocusEffect(pf);
        return pf;
    }

    public static TextArea styledTextArea(String prompt) {
        TextArea ta = new TextArea();
        ta.setPromptText(prompt);
        ta.setFont(regular(13));
        ta.setStyle(inputStyle());
        ta.setPrefRowCount(4);
        ta.setWrapText(true);
        return ta;
    }

    private static String inputStyle() {
        return "-fx-background-color: white;" +
               "-fx-border-color: " + BORDER + ";" +
               "-fx-border-radius: 8;" +
               "-fx-background-radius: 8;" +
               "-fx-padding: 10 14;" +
               "-fx-font-size: 13;";
    }

    private static void addFocusEffect(Control ctrl) {
        ctrl.focusedProperty().addListener((obs, old, focused) -> {
            if (focused) {
                ctrl.setStyle(inputStyle().replace(BORDER, BLUE));
            } else {
                ctrl.setStyle(inputStyle());
            }
        });
    }

    // ── Buttons ───────────────────────────────────────────────────────────────

    public static Button primaryButton(String text) {
        Button btn = new Button(text);
        btn.setFont(semibold(13));
        btn.setStyle(
            "-fx-background-color: " + BLUE + ";" +
            "-fx-text-fill: white;" +
            "-fx-background-radius: 8;" +
            "-fx-border-radius: 8;" +
            "-fx-padding: 10 20;" +
            "-fx-cursor: hand;"
        );
        btn.setPrefHeight(42);
        btn.setOnMouseEntered(e -> btn.setStyle(
            "-fx-background-color: " + BLUE_DARK + ";" +
            "-fx-text-fill: white;" +
            "-fx-background-radius: 8;" +
            "-fx-border-radius: 8;" +
            "-fx-padding: 10 20;" +
            "-fx-cursor: hand;"
        ));
        btn.setOnMouseExited(e -> btn.setStyle(
            "-fx-background-color: " + BLUE + ";" +
            "-fx-text-fill: white;" +
            "-fx-background-radius: 8;" +
            "-fx-border-radius: 8;" +
            "-fx-padding: 10 20;" +
            "-fx-cursor: hand;"
        ));
        return btn;
    }

    public static Button outlineButton(String text) {
        Button btn = new Button(text);
        btn.setFont(semibold(13));
        btn.setStyle(
            "-fx-background-color: white;" +
            "-fx-text-fill: " + BLUE + ";" +
            "-fx-border-color: " + BLUE + ";" +
            "-fx-border-radius: 8;" +
            "-fx-background-radius: 8;" +
            "-fx-padding: 10 20;" +
            "-fx-cursor: hand;"
        );
        btn.setPrefHeight(42);
        return btn;
    }

    public static Button dangerButton(String text) {
        Button btn = new Button(text);
        btn.setFont(semibold(13));
        btn.setStyle(
            "-fx-background-color: " + RED + ";" +
            "-fx-text-fill: white;" +
            "-fx-background-radius: 8;" +
            "-fx-border-radius: 8;" +
            "-fx-padding: 8 16;" +
            "-fx-cursor: hand;"
        );
        btn.setPrefHeight(38);
        return btn;
    }

    // ── Labels ────────────────────────────────────────────────────────────────

    public static Label heading(String text) {
        Label l = new Label(text);
        l.setFont(bold(22));
        l.setTextFill(Color.web(TEXT_DARK));
        return l;
    }

    public static Label subheading(String text) {
        Label l = new Label(text);
        l.setFont(semibold(15));
        l.setTextFill(Color.web(TEXT_DARK));
        return l;
    }

    public static Label label(String text) {
        Label l = new Label(text);
        l.setFont(regular(13));
        l.setTextFill(Color.web(TEXT_DARK));
        return l;
    }

    public static Label secondaryLabel(String text) {
        Label l = new Label(text);
        l.setFont(regular(12));
        l.setTextFill(Color.web(TEXT_GRAY));
        return l;
    }

    // ── Cards & Layout ────────────────────────────────────────────────────────

    public static VBox card() {
        VBox c = new VBox(16);
        c.setPadding(new Insets(24));
        c.setStyle(
            "-fx-background-color: white;" +
            "-fx-background-radius: 14;" +
            "-fx-border-radius: 14;" +
            "-fx-border-color: " + BORDER + ";" +
            "-fx-border-width: 1;"
        );
        DropShadow shadow = new DropShadow();
        shadow.setRadius(12);
        shadow.setOffsetY(4);
        shadow.setColor(Color.rgb(0, 0, 0, 0.06));
        c.setEffect(shadow);
        return c;
    }

    public static Region spacer() {
        Region r = new Region();
        HBox.setHgrow(r, Priority.ALWAYS);
        return r;
    }

    public static VBox formField(String labelText, javafx.scene.Node input) {
        VBox box = new VBox(6);
        Label lbl = label(labelText);
        lbl.setFont(medium(12));
        lbl.setTextFill(Color.web(TEXT_MID));
        box.getChildren().addAll(lbl, input);
        return box;
    }

    // ── Badges ────────────────────────────────────────────────────────────────

    public static Label badge(String text, String bg, String fg) {
        Label l = new Label(text);
        l.setFont(semibold(10));
        l.setStyle(
            "-fx-background-color: " + bg + ";" +
            "-fx-text-fill: " + fg + ";" +
            "-fx-padding: 3 10;" +
            "-fx-background-radius: 20;"
        );
        return l;
    }

    public static Label availableBadge()   { return badge("AVAILABLE",   "#D1FAE5", "#065F46"); }
    public static Label unavailableBadge() { return badge("UNAVAILABLE", "#FEE2E2", "#991B1B"); }
    public static Label ongoingBadge()     { return badge("ONGOING",     "#FEF3C7", "#92400E"); }
    public static Label completedBadge()   { return badge("COMPLETED",   "#D1FAE5", "#065F46"); }

    // ── Item images ───────────────────────────────────────────────────────────

    private static final Map<String, String> ITEM_IMAGE_MAP = Map.ofEntries(
        Map.entry("Waffle Maker",          "/images/waffle_maker.jpg"),
        Map.entry("Slow Juicer",           "/images/slow_juicer.jpg"),
        Map.entry("High-Pressure Washer",  "/images/pressure_washer.jpg"),
        Map.entry("Wet & Dry Vacuum",      "/images/vacuum_cleaner.jpg"),
        Map.entry("Cordless Power Drill",  "/images/power_drill.jpg"),
        Map.entry("Step Ladder",           "/images/step_ladder.jpg"),
        Map.entry("Electric Sander",       "/images/electric_sander.jpg"),
        Map.entry("Projector HD",          "/images/projector.jpg"),
        Map.entry("Food Processor",        "/images/food_processor.jpg"),
        Map.entry("Ice Cream Maker",       "/images/ice_cream_maker.jpg"),
        Map.entry("Jumbo Rice Cooker",     "/images/rice_cooker.jpg"),
        Map.entry("Artisan Stand Mixer",   "/images/stand_mixer.jpg"),
        Map.entry("Foldable Hand Truck",   "/images/hand_truck.jpg"),
        Map.entry("Garden Hose Set",       "/images/garden_hose.jpg"),
        Map.entry("Electric Lawn Mower",   "/images/lawn_mower.jpg"),
        Map.entry("Portable Blower",       "/images/portable_blower.jpg")
    );

    public static Image getItemImage(String title) {
        String path = ITEM_IMAGE_MAP.get(title);
        if (path == null) return null;
        try {
            InputStream is = UIHelper.class.getResourceAsStream(path);
            if (is == null) return null;
            return new Image(is);
        } catch (Exception e) {
            return null;
        }
    }

    // ── Category colors ───────────────────────────────────────────────────────

    public static String categoryColor(String category) {
        return switch (category == null ? "" : category) {
            case "Kitchen"     -> "#FFF7ED";
            case "Tools"       -> "#EFF6FF";
            case "Cleaning"    -> "#F0FDF4";
            case "Electronics" -> "#FAF5FF";
            case "Gardening"   -> "#ECFDF5";
            default            -> LIGHT_BG;
        };
    }

    public static String categoryEmoji(String category) {
        return switch (category == null ? "" : category) {
            case "Kitchen"     -> "🍳";
            case "Tools"       -> "🔧";
            case "Cleaning"    -> "🧹";
            case "Electronics" -> "💡";
            case "Gardening"   -> "🌱";
            default            -> "📦";
        };
    }

    // ── Item card (reusable) ──────────────────────────────────────────────────

    public static VBox itemCard(com.pinjeminaja.model.Item item, Runnable onClick) {
        VBox card = new VBox(0);
        card.setPrefWidth(200);
        card.setStyle(
            "-fx-background-color: white;" +
            "-fx-background-radius: 14;" +
            "-fx-border-radius: 14;" +
            "-fx-border-color: " + BORDER + ";" +
            "-fx-border-width: 1;" +
            "-fx-cursor: hand;"
        );
        DropShadow shadow = new DropShadow();
        shadow.setRadius(10);
        shadow.setOffsetY(3);
        shadow.setColor(Color.rgb(0, 0, 0, 0.07));
        card.setEffect(shadow);

        // Image area — real photo if available, else category emoji
        StackPane imgArea = new StackPane();
        imgArea.setPrefHeight(130);
        String bg = categoryColor(item.getCategory());
        imgArea.setStyle("-fx-background-color: " + bg + "; -fx-background-radius: 14 14 0 0;");
        Image img = getItemImage(item.getTitle());
        if (img != null) {
            ImageView iv = new ImageView(img);
            iv.setFitWidth(200);
            iv.setFitHeight(130);
            iv.setPreserveRatio(false);
            iv.setSmooth(true);
            imgArea.getChildren().add(iv);
        } else {
            Label emoji = new Label(categoryEmoji(item.getCategory()));
            emoji.setFont(Font.font(52));
            imgArea.getChildren().add(emoji);
        }

        // Info area
        VBox info = new VBox(6);
        info.setPadding(new Insets(14));

        Label name = new Label(item.getTitle());
        name.setFont(semibold(13));
        name.setTextFill(Color.web(TEXT_DARK));
        name.setWrapText(true);

        Label cat = new Label(item.getCategory());
        cat.setFont(regular(11));
        cat.setTextFill(Color.web(TEXT_GRAY));

        HBox statusRow = new HBox(8);
        statusRow.setAlignment(Pos.CENTER_LEFT);
        Label statusBadge = item.getStatus().equals("AVAILABLE") ? availableBadge() : unavailableBadge();
        Label price = new Label(formatRupiah(item.getPrice()));
        price.setFont(semibold(13));
        price.setTextFill(Color.web(TEXT_DARK));
        statusRow.getChildren().addAll(statusBadge, price);

        info.getChildren().addAll(name, cat, statusRow);
        card.getChildren().addAll(imgArea, info);

        // Hover effect
        card.setOnMouseEntered(e -> {
            shadow.setRadius(18);
            shadow.setOffsetY(6);
            shadow.setColor(Color.rgb(61, 90, 241, 0.12));
        });
        card.setOnMouseExited(e -> {
            shadow.setRadius(10);
            shadow.setOffsetY(3);
            shadow.setColor(Color.rgb(0, 0, 0, 0.07));
        });
        card.setOnMouseClicked(e -> onClick.run());
        return card;
    }

    // ── Dialogs ───────────────────────────────────────────────────────────────

    public static void showAlert(String title, String message) {
        Alert a = new Alert(Alert.AlertType.INFORMATION);
        a.setTitle(title); a.setHeaderText(null); a.setContentText(message);
        a.showAndWait();
    }

    public static void showError(String message) {
        Alert a = new Alert(Alert.AlertType.ERROR);
        a.setTitle("Error"); a.setHeaderText(null); a.setContentText(message);
        a.showAndWait();
    }

    public static boolean showConfirm(String message) {
        Alert a = new Alert(Alert.AlertType.CONFIRMATION);
        a.setTitle("Konfirmasi"); a.setHeaderText(null); a.setContentText(message);
        return a.showAndWait().filter(r -> r == ButtonType.OK).isPresent();
    }

    public static String formatRupiah(double amount) {
        return "Rp " + String.format("%,.0f", amount).replace(",", ".");
    }
}
