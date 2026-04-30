package com.pinjeminaja.model;

public class Item {
    private int id;
    private int ownerId;
    private String ownerName;
    private String title;
    private String category;
    private double price;
    private String condition;
    private String description;
    private String status;

    public Item(int id, int ownerId, String ownerName, String title, String category,
                double price, String condition, String description, String status) {
        this.id = id;
        this.ownerId = ownerId;
        this.ownerName = ownerName;
        this.title = title;
        this.category = category;
        this.price = price;
        this.condition = condition;
        this.description = description;
        this.status = status;
    }

    public int getId() { return id; }
    public int getOwnerId() { return ownerId; }
    public String getOwnerName() { return ownerName; }
    public String getTitle() { return title; }
    public String getCategory() { return category; }
    public double getPrice() { return price; }
    public String getCondition() { return condition; }
    public String getDescription() { return description; }
    public String getStatus() { return status; }

    public void setTitle(String title) { this.title = title; }
    public void setCategory(String category) { this.category = category; }
    public void setPrice(double price) { this.price = price; }
    public void setCondition(String condition) { this.condition = condition; }
    public void setDescription(String description) { this.description = description; }
    public void setStatus(String status) { this.status = status; }
}
