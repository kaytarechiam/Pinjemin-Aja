package com.pinjeminaja.controller;

import com.pinjeminaja.db.Database;
import com.pinjeminaja.model.User;
import org.sqlite.SQLiteException;

import java.sql.*;

// UC01: Registrasi Akun, UC02: Login, UC03: Melihat Profil, UC04: Edit Profil, UC05: Ubah Kata Sandi
public class AuthController {

    public static User login(String whatsapp, String password) throws SQLException {
        String sql = "SELECT * FROM users WHERE whatsapp = ? AND password = ?";
        try (Connection conn = Database.getConnection();
             PreparedStatement ps = conn.prepareStatement(sql)) {
            ps.setString(1, whatsapp);
            ps.setString(2, password);
            ResultSet rs = ps.executeQuery();
            if (rs.next()) {
                return mapUser(rs);
            }
        }
        return null;
    }

    public static boolean register(String fullName, String whatsapp, String address, String password) throws SQLException {
        String sql = "INSERT INTO users (full_name, whatsapp, address, password, wallet_balance) VALUES (?, ?, ?, ?, 0)";
        try (Connection conn = Database.getConnection();
             PreparedStatement ps = conn.prepareStatement(sql)) {
            ps.setString(1, fullName);
            ps.setString(2, whatsapp);
            ps.setString(3, address);
            ps.setString(4, password);
            ps.executeUpdate();
            return true;
        } catch (SQLiteException e) {
            if (e.getMessage().contains("UNIQUE")) return false;
            throw e;
        }
    }

    public static boolean updateProfile(int userId, String fullName, String whatsapp, String address) throws SQLException {
        String sql = "UPDATE users SET full_name = ?, whatsapp = ?, address = ? WHERE id = ?";
        try (Connection conn = Database.getConnection();
             PreparedStatement ps = conn.prepareStatement(sql)) {
            ps.setString(1, fullName);
            ps.setString(2, whatsapp);
            ps.setString(3, address);
            ps.setInt(4, userId);
            ps.executeUpdate();
            return true;
        }
    }

    public static boolean changePassword(int userId, String oldPassword, String newPassword) throws SQLException {
        String checkSql = "SELECT id FROM users WHERE id = ? AND password = ?";
        try (Connection conn = Database.getConnection();
             PreparedStatement ps = conn.prepareStatement(checkSql)) {
            ps.setInt(1, userId);
            ps.setString(2, oldPassword);
            ResultSet rs = ps.executeQuery();
            if (!rs.next()) return false;
        }
        String updateSql = "UPDATE users SET password = ? WHERE id = ?";
        try (Connection conn = Database.getConnection();
             PreparedStatement ps = conn.prepareStatement(updateSql)) {
            ps.setString(1, newPassword);
            ps.setInt(2, userId);
            ps.executeUpdate();
            return true;
        }
    }

    public static User getUserById(int id) throws SQLException {
        String sql = "SELECT * FROM users WHERE id = ?";
        try (Connection conn = Database.getConnection();
             PreparedStatement ps = conn.prepareStatement(sql)) {
            ps.setInt(1, id);
            ResultSet rs = ps.executeQuery();
            if (rs.next()) return mapUser(rs);
        }
        return null;
    }

    private static User mapUser(ResultSet rs) throws SQLException {
        return new User(
            rs.getInt("id"),
            rs.getString("full_name"),
            rs.getString("whatsapp"),
            rs.getString("address"),
            rs.getString("password"),
            rs.getDouble("wallet_balance")
        );
    }
}
