package com.pinjeminaja.controller;

import com.pinjeminaja.db.Database;
import com.pinjeminaja.model.Item;

import java.sql.*;
import java.util.ArrayList;
import java.util.List;

// UC09: Melihat Katalog, UC10: Katalog Saya, UC11: Tambah, UC12: Hapus, UC13: Edit, UC14: Cari, UC15: Filter, UC16: Detail
public class ItemController {

    public static List<Item> getAllItems() throws SQLException {
        return queryItems("SELECT i.*, u.full_name as owner_name FROM items i JOIN users u ON i.owner_id = u.id WHERE i.status != 'DELETED' ORDER BY i.id DESC", null);
    }

    public static List<Item> searchItems(String keyword) throws SQLException {
        String sql = "SELECT i.*, u.full_name as owner_name FROM items i JOIN users u ON i.owner_id = u.id WHERE i.status != 'DELETED' AND (LOWER(i.title) LIKE LOWER(?) OR LOWER(i.description) LIKE LOWER(?)) ORDER BY i.id DESC";
        List<Object> params = List.of("%" + keyword + "%", "%" + keyword + "%");
        return queryItems(sql, params);
    }

    public static List<Item> filterByCategory(String category) throws SQLException {
        String sql = "SELECT i.*, u.full_name as owner_name FROM items i JOIN users u ON i.owner_id = u.id WHERE i.status != 'DELETED' AND i.category = ? ORDER BY i.id DESC";
        return queryItems(sql, List.of(category));
    }

    public static List<Item> searchAndFilter(String keyword, String category) throws SQLException {
        if ((keyword == null || keyword.isBlank()) && (category == null || category.isBlank())) return getAllItems();
        if (category == null || category.isBlank()) return searchItems(keyword);
        if (keyword == null || keyword.isBlank()) return filterByCategory(category);
        String sql = "SELECT i.*, u.full_name as owner_name FROM items i JOIN users u ON i.owner_id = u.id WHERE i.status != 'DELETED' AND i.category = ? AND (LOWER(i.title) LIKE LOWER(?) OR LOWER(i.description) LIKE LOWER(?)) ORDER BY i.id DESC";
        return queryItems(sql, List.of(category, "%" + keyword + "%", "%" + keyword + "%"));
    }

    public static List<Item> getMyItems(int ownerId) throws SQLException {
        String sql = "SELECT i.*, u.full_name as owner_name FROM items i JOIN users u ON i.owner_id = u.id WHERE i.owner_id = ? AND i.status != 'DELETED' ORDER BY i.id DESC";
        return queryItems(sql, List.of(ownerId));
    }

    public static Item getItemById(int id) throws SQLException {
        String sql = "SELECT i.*, u.full_name as owner_name FROM items i JOIN users u ON i.owner_id = u.id WHERE i.id = ?";
        List<Item> result = queryItems(sql, List.of(id));
        return result.isEmpty() ? null : result.get(0);
    }

    public static void addItem(int ownerId, String title, String category, double price, String condition, String description) throws SQLException {
        String sql = "INSERT INTO items (owner_id, title, category, price, condition, description, status) VALUES (?, ?, ?, ?, ?, ?, 'AVAILABLE')";
        try (Connection conn = Database.getConnection();
             PreparedStatement ps = conn.prepareStatement(sql)) {
            ps.setInt(1, ownerId);
            ps.setString(2, title);
            ps.setString(3, category);
            ps.setDouble(4, price);
            ps.setString(5, condition);
            ps.setString(6, description);
            ps.executeUpdate();
        }
    }

    public static void updateItem(int id, String title, String category, double price, String condition, String description) throws SQLException {
        String sql = "UPDATE items SET title = ?, category = ?, price = ?, condition = ?, description = ? WHERE id = ?";
        try (Connection conn = Database.getConnection();
             PreparedStatement ps = conn.prepareStatement(sql)) {
            ps.setString(1, title);
            ps.setString(2, category);
            ps.setDouble(3, price);
            ps.setString(4, condition);
            ps.setString(5, description);
            ps.setInt(6, id);
            ps.executeUpdate();
        }
    }

    public static void deleteItem(int id) throws SQLException {
        String sql = "UPDATE items SET status = 'DELETED' WHERE id = ?";
        try (Connection conn = Database.getConnection();
             PreparedStatement ps = conn.prepareStatement(sql)) {
            ps.setInt(1, id);
            ps.executeUpdate();
        }
    }

    public static void updateStatus(int id, String status) throws SQLException {
        String sql = "UPDATE items SET status = ? WHERE id = ?";
        try (Connection conn = Database.getConnection();
             PreparedStatement ps = conn.prepareStatement(sql)) {
            ps.setString(1, status);
            ps.setInt(2, id);
            ps.executeUpdate();
        }
    }

    private static List<Item> queryItems(String sql, List<Object> params) throws SQLException {
        List<Item> items = new ArrayList<>();
        try (Connection conn = Database.getConnection();
             PreparedStatement ps = conn.prepareStatement(sql)) {
            if (params != null) {
                for (int i = 0; i < params.size(); i++) {
                    ps.setObject(i + 1, params.get(i));
                }
            }
            ResultSet rs = ps.executeQuery();
            while (rs.next()) {
                items.add(new Item(
                    rs.getInt("id"),
                    rs.getInt("owner_id"),
                    rs.getString("owner_name"),
                    rs.getString("title"),
                    rs.getString("category"),
                    rs.getDouble("price"),
                    rs.getString("condition"),
                    rs.getString("description"),
                    rs.getString("status")
                ));
            }
        }
        return items;
    }
}
