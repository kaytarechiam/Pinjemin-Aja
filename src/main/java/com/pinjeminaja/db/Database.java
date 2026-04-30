package com.pinjeminaja.db;

import java.sql.*;

public class Database {
    private static final String URL = "jdbc:sqlite:pinjeminaja.db";
    private static Connection connection;

    public static Connection getConnection() throws SQLException {
        if (connection == null || connection.isClosed()) {
            connection = DriverManager.getConnection(URL);
            connection.createStatement().execute("PRAGMA foreign_keys = ON");
        }
        return connection;
    }

    public static void initialize() {
        try (Connection conn = getConnection(); Statement stmt = conn.createStatement()) {
            stmt.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    full_name TEXT NOT NULL,
                    whatsapp TEXT UNIQUE NOT NULL,
                    address TEXT NOT NULL,
                    password TEXT NOT NULL,
                    wallet_balance REAL DEFAULT 0
                )
            """);
            stmt.execute("""
                CREATE TABLE IF NOT EXISTS items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    owner_id INTEGER NOT NULL,
                    title TEXT NOT NULL,
                    category TEXT NOT NULL,
                    price REAL NOT NULL,
                    condition TEXT NOT NULL,
                    description TEXT,
                    status TEXT DEFAULT 'AVAILABLE',
                    FOREIGN KEY (owner_id) REFERENCES users(id)
                )
            """);
            stmt.execute("""
                CREATE TABLE IF NOT EXISTS transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    item_id INTEGER NOT NULL,
                    renter_id INTEGER NOT NULL,
                    owner_id INTEGER NOT NULL,
                    start_date TEXT NOT NULL,
                    end_date TEXT NOT NULL,
                    total_price REAL NOT NULL,
                    status TEXT DEFAULT 'ONGOING',
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (item_id) REFERENCES items(id),
                    FOREIGN KEY (renter_id) REFERENCES users(id),
                    FOREIGN KEY (owner_id) REFERENCES users(id)
                )
            """);
        } catch (SQLException e) {
            throw new RuntimeException("Database initialization failed", e);
        }
    }
}
