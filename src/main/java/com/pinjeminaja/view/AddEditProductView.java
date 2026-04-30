package com.pinjeminaja.view;

import com.pinjeminaja.Session;
import com.pinjeminaja.controller.ItemController;
import com.pinjeminaja.model.Item;
import javafx.geometry.Insets;
import javafx.geometry.Pos;
import javafx.scene.control.*;
import javafx.scene.layout.*;
import javafx.scene.paint.Color;
import javafx.scene.text.*;

// UC11, UC13
public class AddEditProductView extends VBox {

    private static final String[] CATEGORIES = {"Cleaning", "Electronics", "Kitchen", "Tools", "Gardening"};
    private static final String[] CONDITIONS  = {"Good", "Fair", "Needs Repair"};

    private final Item existingItem;
    private final Runnable onSave;
    private final Runnable onCancel;

    public AddEditProductView(Item existingItem, Runnable onSave, Runnable onCancel) {
        this.existingItem = existingItem;
        this.onSave       = onSave;
        this.onCancel     = onCancel;
        build();
    }

    private void build() {
        setStyle("-fx-background-color: " + UIHelper.LIGHT_BG + ";");
        setPadding(new Insets(28));
        setSpacing(16);

        boolean isEdit = existingItem != null;

        // Breadcrumb
        HBox bc = new HBox(6);
        bc.setAlignment(Pos.CENTER_LEFT);
        bc.getChildren().addAll(
            UIHelper.secondaryLabel("My Items"), UIHelper.secondaryLabel("›"),
            new Label(isEdit ? "Edit Product" : "Add Product") {{
                setFont(UIHelper.medium(12)); setTextFill(Color.web(UIHelper.TEXT_DARK));
            }}
        );

        // Card
        VBox card = UIHelper.card();
        card.setSpacing(20);

        Label cardTitle = UIHelper.heading(isEdit ? "Edit Product" : "Add Product");

        // Row 1: Title + Price
        TextField titleField = UIHelper.styledTextField("Nama produk");
        titleField.setPrefWidth(340);
        if (isEdit) titleField.setText(existingItem.getTitle());

        TextField priceField = UIHelper.styledTextField("Harga / hari (Rp)");
        priceField.setPrefWidth(220);
        if (isEdit) priceField.setText(String.valueOf((int) existingItem.getPrice()));

        HBox row1 = new HBox(20,
            UIHelper.formField("Title", titleField),
            UIHelper.formField("Price per Day", priceField)
        );

        // Row 2: Category + Condition
        ComboBox<String> catBox = styledCombo(CATEGORIES, "Pilih kategori");
        catBox.setPrefWidth(220);
        if (isEdit) catBox.setValue(existingItem.getCategory());

        ComboBox<String> condBox = styledCombo(CONDITIONS, "Pilih kondisi");
        condBox.setPrefWidth(220);
        if (isEdit) condBox.setValue(existingItem.getCondition());

        HBox row2 = new HBox(20,
            UIHelper.formField("Category", catBox),
            UIHelper.formField("Condition", condBox)
        );

        // Description
        TextArea descArea = UIHelper.styledTextArea("Deskripsikan alat Anda...");
        descArea.setPrefWidth(580);
        if (isEdit && existingItem.getDescription() != null) descArea.setText(existingItem.getDescription());

        // Buttons
        Button saveBtn   = UIHelper.primaryButton(isEdit ? "💾  Save Changes" : "✅  Save Item");
        saveBtn.setPrefWidth(160);
        Button cancelBtn = UIHelper.outlineButton("Batal");
        cancelBtn.setOnAction(e -> onCancel.run());

        Label errorLabel = new Label();
        errorLabel.setFont(UIHelper.regular(12));
        errorLabel.setTextFill(Color.web(UIHelper.RED));
        errorLabel.setVisible(false);

        HBox btnRow = new HBox(12, saveBtn, cancelBtn);
        btnRow.setAlignment(Pos.CENTER_LEFT);

        saveBtn.setOnAction(e -> handleSave(titleField, priceField, catBox, condBox, descArea, errorLabel));

        card.getChildren().addAll(cardTitle, row1, row2,
            UIHelper.formField("Description", descArea), btnRow, errorLabel);

        getChildren().addAll(bc, card);
    }

    private ComboBox<String> styledCombo(String[] items, String prompt) {
        ComboBox<String> cb = new ComboBox<>();
        cb.getItems().addAll(items);
        cb.setPromptText(prompt);
        cb.setStyle("-fx-font-size: 13; -fx-background-radius: 8; -fx-border-radius: 8;");
        cb.setPrefHeight(42);
        return cb;
    }

    private void handleSave(TextField tf, TextField pf, ComboBox<String> cat, ComboBox<String> cond,
                            TextArea desc, Label err) {
        String title    = tf.getText().trim();
        String priceStr = pf.getText().trim();
        String category = cat.getValue();
        String condition = cond.getValue();
        String description = desc.getText().trim();

        if (title.isEmpty() || priceStr.isEmpty() || category == null || condition == null) {
            err.setText("Judul, harga, kategori, dan kondisi harus diisi."); err.setVisible(true); return;
        }
        double price;
        try {
            price = Double.parseDouble(priceStr);
            if (price <= 0) throw new NumberFormatException();
        } catch (NumberFormatException ex) {
            err.setText("Harga harus berupa angka positif."); err.setVisible(true); return;
        }
        try {
            if (existingItem == null) {
                ItemController.addItem(Session.getCurrentUser().getId(), title, category, price, condition, description);
            } else {
                ItemController.updateItem(existingItem.getId(), title, category, price, condition, description);
            }
            onSave.run();
        } catch (Exception ex) {
            err.setText("Gagal menyimpan. Coba lagi."); err.setVisible(true);
        }
    }
}
