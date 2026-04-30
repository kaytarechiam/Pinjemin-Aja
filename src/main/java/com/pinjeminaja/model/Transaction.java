package com.pinjeminaja.model;

public class Transaction {
    private int id;
    private int itemId;
    private int renterId;
    private int ownerId;
    private String itemTitle;
    private String renterName;
    private String ownerName;
    private String startDate;
    private String endDate;
    private double totalPrice;
    private String status;
    private String createdAt;

    public Transaction(int id, int itemId, int renterId, int ownerId,
                       String itemTitle, String renterName, String ownerName,
                       String startDate, String endDate, double totalPrice,
                       String status, String createdAt) {
        this.id = id;
        this.itemId = itemId;
        this.renterId = renterId;
        this.ownerId = ownerId;
        this.itemTitle = itemTitle;
        this.renterName = renterName;
        this.ownerName = ownerName;
        this.startDate = startDate;
        this.endDate = endDate;
        this.totalPrice = totalPrice;
        this.status = status;
        this.createdAt = createdAt;
    }

    public int getId() { return id; }
    public int getItemId() { return itemId; }
    public int getRenterId() { return renterId; }
    public int getOwnerId() { return ownerId; }
    public String getItemTitle() { return itemTitle; }
    public String getRenterName() { return renterName; }
    public String getOwnerName() { return ownerName; }
    public String getStartDate() { return startDate; }
    public String getEndDate() { return endDate; }
    public double getTotalPrice() { return totalPrice; }
    public String getStatus() { return status; }
    public String getCreatedAt() { return createdAt; }
    public void setStatus(String status) { this.status = status; }
}
