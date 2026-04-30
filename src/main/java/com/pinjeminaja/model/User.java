package com.pinjeminaja.model;

public class User {
    private int id;
    private String fullName;
    private String whatsapp;
    private String address;
    private String password;
    private double walletBalance;

    public User(int id, String fullName, String whatsapp, String address, String password, double walletBalance) {
        this.id = id;
        this.fullName = fullName;
        this.whatsapp = whatsapp;
        this.address = address;
        this.password = password;
        this.walletBalance = walletBalance;
    }

    public int getId() { return id; }
    public String getFullName() { return fullName; }
    public String getWhatsapp() { return whatsapp; }
    public String getAddress() { return address; }
    public String getPassword() { return password; }
    public double getWalletBalance() { return walletBalance; }

    public void setFullName(String fullName) { this.fullName = fullName; }
    public void setWhatsapp(String whatsapp) { this.whatsapp = whatsapp; }
    public void setAddress(String address) { this.address = address; }
    public void setPassword(String password) { this.password = password; }
    public void setWalletBalance(double walletBalance) { this.walletBalance = walletBalance; }
}
