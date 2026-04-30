package com.pinjeminaja.controller;

import com.pinjeminaja.db.Database;
import com.pinjeminaja.model.Transaction;

import java.sql.*;
import java.util.ArrayList;
import java.util.List;

// UC17: Peminjaman, UC18: Konfirmasi Pengembalian, UC19: Riwayat, UC20: Filter, UC21: Detail
public class TransactionController {

    public static Transaction createTransaction(int itemId, int renterId, int ownerId,
                                                String startDate, String endDate, double totalPrice) throws SQLException {
        String sql = "INSERT INTO transactions (item_id, renter_id, owner_id, start_date, end_date, total_price, status) VALUES (?, ?, ?, ?, ?, ?, 'ONGOING')";
        try (Connection conn = Database.getConnection();
             PreparedStatement ps = conn.prepareStatement(sql, Statement.RETURN_GENERATED_KEYS)) {
            ps.setInt(1, itemId);
            ps.setInt(2, renterId);
            ps.setInt(3, ownerId);
            ps.setString(4, startDate);
            ps.setString(5, endDate);
            ps.setDouble(6, totalPrice);
            ps.executeUpdate();
            ResultSet keys = ps.getGeneratedKeys();
            if (keys.next()) return getTransactionById(keys.getInt(1));
        }
        return null;
    }

    // UC18: Konfirmasi Pengembalian Alat — dipanggil oleh penyedia
    public static void confirmReturn(int transactionId) throws SQLException {
        try (Connection conn = Database.getConnection()) {
            Transaction t = getTransactionById(transactionId);
            if (t == null) return;
            // Update status transaksi
            PreparedStatement ps1 = conn.prepareStatement("UPDATE transactions SET status = 'COMPLETED' WHERE id = ?");
            ps1.setInt(1, transactionId);
            ps1.executeUpdate();
            // Kembalikan status alat ke AVAILABLE
            PreparedStatement ps2 = conn.prepareStatement("UPDATE items SET status = 'AVAILABLE' WHERE id = ?");
            ps2.setInt(1, t.getItemId());
            ps2.executeUpdate();
        }
    }

    // UC19: Riwayat Transaksi — semua transaksi user (sebagai peminjam atau penyedia)
    public static List<Transaction> getAllTransactions(int userId) throws SQLException {
        String sql = """
            SELECT t.*, i.title as item_title, r.full_name as renter_name, o.full_name as owner_name
            FROM transactions t
            JOIN items i ON t.item_id = i.id
            JOIN users r ON t.renter_id = r.id
            JOIN users o ON t.owner_id = o.id
            WHERE t.renter_id = ? OR t.owner_id = ?
            ORDER BY t.created_at DESC
        """;
        return queryTransactions(sql, List.of(userId, userId));
    }

    // UC20: Filter Riwayat — sebagai peminjam
    public static List<Transaction> getRentalHistory(int renterId) throws SQLException {
        String sql = """
            SELECT t.*, i.title as item_title, r.full_name as renter_name, o.full_name as owner_name
            FROM transactions t
            JOIN items i ON t.item_id = i.id
            JOIN users r ON t.renter_id = r.id
            JOIN users o ON t.owner_id = o.id
            WHERE t.renter_id = ?
            ORDER BY t.created_at DESC
        """;
        return queryTransactions(sql, List.of(renterId));
    }

    // UC20: Filter Riwayat — sebagai penyedia
    public static List<Transaction> getLendingHistory(int ownerId) throws SQLException {
        String sql = """
            SELECT t.*, i.title as item_title, r.full_name as renter_name, o.full_name as owner_name
            FROM transactions t
            JOIN items i ON t.item_id = i.id
            JOIN users r ON t.renter_id = r.id
            JOIN users o ON t.owner_id = o.id
            WHERE t.owner_id = ?
            ORDER BY t.created_at DESC
        """;
        return queryTransactions(sql, List.of(ownerId));
    }

    public static List<Transaction> getRecentTransactions(int userId, int limit) throws SQLException {
        String sql = """
            SELECT t.*, i.title as item_title, r.full_name as renter_name, o.full_name as owner_name
            FROM transactions t
            JOIN items i ON t.item_id = i.id
            JOIN users r ON t.renter_id = r.id
            JOIN users o ON t.owner_id = o.id
            WHERE t.renter_id = ? OR t.owner_id = ?
            ORDER BY t.created_at DESC LIMIT ?
        """;
        return queryTransactions(sql, List.of(userId, userId, limit));
    }

    public static Transaction getTransactionById(int id) throws SQLException {
        String sql = """
            SELECT t.*, i.title as item_title, r.full_name as renter_name, o.full_name as owner_name
            FROM transactions t
            JOIN items i ON t.item_id = i.id
            JOIN users r ON t.renter_id = r.id
            JOIN users o ON t.owner_id = o.id
            WHERE t.id = ?
        """;
        List<Transaction> result = queryTransactions(sql, List.of(id));
        return result.isEmpty() ? null : result.get(0);
    }

    private static List<Transaction> queryTransactions(String sql, List<Object> params) throws SQLException {
        List<Transaction> list = new ArrayList<>();
        try (Connection conn = Database.getConnection();
             PreparedStatement ps = conn.prepareStatement(sql)) {
            for (int i = 0; i < params.size(); i++) ps.setObject(i + 1, params.get(i));
            ResultSet rs = ps.executeQuery();
            while (rs.next()) {
                list.add(new Transaction(
                    rs.getInt("id"),
                    rs.getInt("item_id"),
                    rs.getInt("renter_id"),
                    rs.getInt("owner_id"),
                    rs.getString("item_title"),
                    rs.getString("renter_name"),
                    rs.getString("owner_name"),
                    rs.getString("start_date"),
                    rs.getString("end_date"),
                    rs.getDouble("total_price"),
                    rs.getString("status"),
                    rs.getString("created_at")
                ));
            }
        }
        return list;
    }
}
