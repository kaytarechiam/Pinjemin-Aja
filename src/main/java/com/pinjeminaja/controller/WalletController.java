package com.pinjeminaja.controller;

import com.pinjeminaja.db.Database;

import java.sql.*;

// UC06: Melihat Saldo, UC07: Top-up, UC08: Tarik Saldo
public class WalletController {

    public static double getBalance(int userId) throws SQLException {
        String sql = "SELECT wallet_balance FROM users WHERE id = ?";
        try (Connection conn = Database.getConnection();
             PreparedStatement ps = conn.prepareStatement(sql)) {
            ps.setInt(1, userId);
            ResultSet rs = ps.executeQuery();
            if (rs.next()) return rs.getDouble("wallet_balance");
        }
        return 0;
    }

    public static double topUp(int userId, double amount) throws SQLException {
        if (amount <= 0) throw new IllegalArgumentException("Nominal harus lebih dari 0");
        String sql = "UPDATE users SET wallet_balance = wallet_balance + ? WHERE id = ?";
        try (Connection conn = Database.getConnection();
             PreparedStatement ps = conn.prepareStatement(sql)) {
            ps.setDouble(1, amount);
            ps.setInt(2, userId);
            ps.executeUpdate();
        }
        return getBalance(userId);
    }

    public static double withdraw(int userId, double amount) throws SQLException {
        if (amount <= 0) throw new IllegalArgumentException("Nominal harus lebih dari 0");
        double current = getBalance(userId);
        if (current < amount) throw new IllegalStateException("Saldo tidak mencukupi");
        String sql = "UPDATE users SET wallet_balance = wallet_balance - ? WHERE id = ?";
        try (Connection conn = Database.getConnection();
             PreparedStatement ps = conn.prepareStatement(sql)) {
            ps.setDouble(1, amount);
            ps.setInt(2, userId);
            ps.executeUpdate();
        }
        return getBalance(userId);
    }

    public static void deductForRental(int userId, double amount) throws SQLException {
        double current = getBalance(userId);
        if (current < amount) throw new IllegalStateException("Saldo tidak mencukupi untuk melakukan peminjaman");
        String sql = "UPDATE users SET wallet_balance = wallet_balance - ? WHERE id = ?";
        try (Connection conn = Database.getConnection();
             PreparedStatement ps = conn.prepareStatement(sql)) {
            ps.setDouble(1, amount);
            ps.setInt(2, userId);
            ps.executeUpdate();
        }
    }

    public static void creditOwner(int ownerId, double amount) throws SQLException {
        String sql = "UPDATE users SET wallet_balance = wallet_balance + ? WHERE id = ?";
        try (Connection conn = Database.getConnection();
             PreparedStatement ps = conn.prepareStatement(sql)) {
            ps.setDouble(1, amount);
            ps.setInt(2, ownerId);
            ps.executeUpdate();
        }
    }
}
