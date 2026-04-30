package com.pinjeminaja.db;

import java.sql.*;

public class Seeder {

    public static void seed() {
        try (Connection conn = Database.getConnection()) {
            if (isAlreadySeeded(conn)) return;
            seedUsers(conn);
            seedItems(conn);
            seedTransactions(conn);
            System.out.println("Database seeded successfully.");
        } catch (SQLException e) {
            System.err.println("Seeding failed: " + e.getMessage());
        }
    }

    private static boolean isAlreadySeeded(Connection conn) throws SQLException {
        ResultSet rs = conn.createStatement().executeQuery("SELECT COUNT(*) FROM users");
        return rs.next() && rs.getInt(1) > 0;
    }

    // ── Users ─────────────────────────────────────────────────────────────────
    private static void seedUsers(Connection conn) throws SQLException {
        String sql = "INSERT INTO users (full_name, whatsapp, address, password, wallet_balance) VALUES (?,?,?,?,?)";
        Object[][] users = {
            {"Dadang Suherman",  "081234567890", "Komplek Mawar No. 5, Antapani, Kota Bandung",   "password123", 1_500_000},
            {"Diana Rahayu",     "082345678901", "Jl. Kebon Jeruk No. 12, Cicendo, Kota Bandung", "password123",   800_000},
            {"Riko Firmansyah",  "083456789012", "Jl. Pasir Kaliki No. 88, Sukajadi, Bandung",    "password123", 2_200_000},
            {"Salma Aulia",      "084567890123", "Perum Griya Asri Blok C7, Cimahi",              "password123",   350_000},
        };
        try (PreparedStatement ps = conn.prepareStatement(sql)) {
            for (Object[] u : users) {
                ps.setString(1, (String) u[0]);
                ps.setString(2, (String) u[1]);
                ps.setString(3, (String) u[2]);
                ps.setString(4, (String) u[3]);
                ps.setDouble(5, (double) ((Number) u[4]).doubleValue());
                ps.executeUpdate();
            }
        }
    }

    // ── Items ─────────────────────────────────────────────────────────────────
    private static void seedItems(Connection conn) throws SQLException {
        String sql = "INSERT INTO items (owner_id, title, category, price, condition, description, status) VALUES (?,?,?,?,?,?,?)";
        Object[][] items = {
            // Dadang (id=1) punya alat dapur & kebersihan
            {1, "Waffle Maker",        "Kitchen",   25_000, "Good",         "Buat waffle crispy di rumah. Kapasitas 2 buah sekaligus, anti lengket, mudah dibersihkan.",                              "AVAILABLE"},
            {1, "Slow Juicer",         "Kitchen",   50_000, "Good",         "Juicer lambat untuk sari buah murni tanpa panas berlebih. Cocok untuk diet sehat.",                                       "AVAILABLE"},
            {1, "High-Pressure Washer","Cleaning",  60_000, "Needs Repair", "Mesin cuci bertekanan tinggi. Cocok untuk cuci motor, mobil, atau teras. Selang 5 meter.",                               "AVAILABLE"},
            {1, "Wet & Dry Vacuum",    "Cleaning",  50_000, "Good",         "Vacuum cleaner serbaguna bisa menyedot debu kering maupun cairan. Kapasitas tangki 15 liter.",                           "AVAILABLE"},

            // Diana (id=2) punya elektronik & peralatan
            {2, "Cordless Power Drill", "Tools",    35_000, "Good",         "Bor nirkabel 18V dengan 2 baterai cadangan. Dilengkapi 20 mata bor berbagai ukuran.",                                   "AVAILABLE"},
            {2, "Step Ladder",          "Tools",    25_000, "Fair",         "Tangga lipat aluminium 5 anak tangga. Kuat hingga 150 kg. Ringan dan mudah disimpan.",                                   "AVAILABLE"},
            {2, "Electric Sander",      "Tools",    40_000, "Good",         "Mesin amplas orbital untuk penghalusan kayu atau dinding. Dilengkapi berbagai tingkat kekasaran amplas.",                "AVAILABLE"},
            {2, "Projector HD",         "Electronics", 80_000, "Good",      "Proyektor 1080p Full HD. Cocok untuk presentasi, nonton bareng, atau acara keluarga. Koneksi HDMI & USB.",              "AVAILABLE"},

            // Riko (id=3) punya peralatan dapur besar
            {3, "Food Processor",       "Kitchen",  45_000, "Fair",         "Chopper, slicer, dan blender dalam satu alat. Ideal untuk persiapan masak skala besar.",                                "AVAILABLE"},
            {3, "Ice Cream Maker",      "Kitchen",  60_000, "Good",         "Buat hingga 1.5 liter es krim homemade dalam 20-30 menit. Tangki beku terpisah, mudah dioperasikan.",                   "AVAILABLE"},
            {3, "Jumbo Rice Cooker",    "Kitchen",  20_000, "Good",         "Rice cooker kapasitas 5 liter. Cocok untuk hajatan kecil atau katering. Fungsi warm otomatis.",                         "UNAVAILABLE"},
            {3, "Artisan Stand Mixer",  "Kitchen",  40_000, "Good",         "Mixer duduk 5 liter 10 kecepatan. Dilengkapi hook, paddle, dan whisk. Ideal untuk membuat adonan kue dan roti.",        "AVAILABLE"},

            // Salma (id=4) punya peralatan kebun & rumah
            {4, "Foldable Hand Truck",  "Tools",    25_000, "Good",         "Troli lipat kapasitas 80 kg. Roda karet anti gores. Mudah disimpan di sudut sempit.",                                   "AVAILABLE"},
            {4, "Garden Hose Set",      "Gardening",15_000, "Good",         "Selang air 15 meter dengan 7 mode semprotan. Cocok untuk menyiram tanaman, taman, atau cuci kendaraan.",                "AVAILABLE"},
            {4, "Electric Lawn Mower",  "Gardening",55_000, "Fair",         "Mesin pemotong rumput listrik. Lebar potong 32 cm. Kabel 10 meter. Cocok untuk halaman ukuran sedang.",                 "AVAILABLE"},
            {4, "Portable Blower",      "Gardening",20_000, "Good",         "Blower listrik untuk membersihkan daun kering, debu di teras, atau kotoran di garasi. Ringan dan bertenaga.",           "AVAILABLE"},
        };
        try (PreparedStatement ps = conn.prepareStatement(sql)) {
            for (Object[] it : items) {
                ps.setInt(1, (int) it[0]);
                ps.setString(2, (String) it[1]);
                ps.setString(3, (String) it[2]);
                ps.setDouble(4, ((Number) it[3]).doubleValue());
                ps.setString(5, (String) it[4]);
                ps.setString(6, (String) it[5]);
                ps.setString(7, (String) it[6]);
                ps.executeUpdate();
            }
        }
    }

    // ── Transactions ──────────────────────────────────────────────────────────
    private static void seedTransactions(Connection conn) throws SQLException {
        String sql = "INSERT INTO transactions (item_id, renter_id, owner_id, start_date, end_date, total_price, status, created_at) VALUES (?,?,?,?,?,?,?,?)";
        // item_id 11 = Jumbo Rice Cooker milik Riko (id=3) — status UNAVAILABLE
        Object[][] txns = {
            // Diana (2) pinjam Jumbo Rice Cooker dari Riko (3) — ongoing
            {11, 2, 3, "2026-04-26", "2026-04-27",  20_000, "ONGOING",   "2026-04-26 08:00:00"},
            // Dadang (1) pinjam Cordless Power Drill dari Diana (2) — selesai
            {5,  1, 2, "2026-04-21", "2026-04-23",  70_000, "COMPLETED", "2026-04-21 10:30:00"},
            // Salma (4) pinjam Step Ladder dari Diana (2) — selesai
            {6,  4, 2, "2026-04-20", "2026-04-21",  25_000, "COMPLETED", "2026-04-20 09:00:00"},
            // Riko (3) pinjam Garden Hose dari Salma (4) — selesai
            {14, 3, 4, "2026-04-19", "2026-04-21",  30_000, "COMPLETED", "2026-04-19 14:00:00"},
            // Dadang (1) pinjam Ice Cream Maker dari Riko (3) — selesai
            {10, 1, 3, "2026-04-26", "2026-04-29", 180_000, "COMPLETED", "2026-04-26 11:00:00"},
        };
        try (PreparedStatement ps = conn.prepareStatement(sql)) {
            for (Object[] t : txns) {
                ps.setInt(1, (int) t[0]);
                ps.setInt(2, (int) t[1]);
                ps.setInt(3, (int) t[2]);
                ps.setString(4, (String) t[3]);
                ps.setString(5, (String) t[4]);
                ps.setDouble(6, ((Number) t[5]).doubleValue());
                ps.setString(7, (String) t[6]);
                ps.setString(8, (String) t[7]);
                ps.executeUpdate();
            }
        }
    }
}
