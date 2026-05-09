from database.database import get_connection


def seed():
    with get_connection() as conn:
        count = conn.execute("SELECT COUNT(*) FROM pengguna").fetchone()[0]
        if count > 0:
            return  # already seeded

        # ── Pengguna ──────────────────────────────────────────────────────────
        users = [
            ("Dadang Suherman",  "081234567890", "Komplek Mawar No. 5, Antapani, Kota Bandung",   "password123"),
            ("Diana Rahayu",     "082345678901", "Jl. Kebon Jeruk No. 12, Cicendo, Kota Bandung", "password123"),
            ("Riko Firmansyah",  "083456789012", "Jl. Pasir Kaliki No. 88, Sukajadi, Bandung",    "password123"),
            ("Salma Aulia",      "084567890123", "Perum Griya Asri Blok C7, Cimahi",              "password123"),
        ]
        for u in users:
            conn.execute(
                "INSERT INTO pengguna (nama_lengkap, no_wa, alamat, kata_sandi) VALUES (?,?,?,?)", u
            )

        # ── Dompet Digital ────────────────────────────────────────────────────
        saldo_awal = [1_500_000, 800_000, 2_200_000, 350_000]
        for i, saldo in enumerate(saldo_awal, start=1):
            conn.execute(
                "INSERT INTO dompet_digital (id_pengguna, saldo) VALUES (?,?)", (i, saldo)
            )

        # ── Alat ──────────────────────────────────────────────────────────────
        alat_data = [
            # Dadang (1)
            (1, "Waffle Maker",        "Kitchen",     25_000, "Good",         "Buat waffle crispy di rumah. Kapasitas 2 buah sekaligus, anti lengket, mudah dibersihkan.",                              "Tersedia"),
            (1, "Slow Juicer",         "Kitchen",     50_000, "Good",         "Juicer lambat untuk sari buah murni tanpa panas berlebih. Cocok untuk diet sehat.",                                       "Tersedia"),
            (1, "High-Pressure Washer","Cleaning",    60_000, "Perlu Perbaikan","Mesin cuci bertekanan tinggi. Cocok untuk cuci motor, mobil, atau teras. Selang 5 meter.",                              "Tersedia"),
            (1, "Wet & Dry Vacuum",    "Cleaning",    50_000, "Good",         "Vacuum cleaner serbaguna bisa menyedot debu kering maupun cairan. Kapasitas tangki 15 liter.",                           "Tersedia"),
            # Diana (2)
            (2, "Cordless Power Drill", "Tools",      35_000, "Good",         "Bor nirkabel 18V dengan 2 baterai cadangan. Dilengkapi 20 mata bor berbagai ukuran.",                                   "Tersedia"),
            (2, "Step Ladder",          "Tools",      25_000, "Cukup Baik",   "Tangga lipat aluminium 5 anak tangga. Kuat hingga 150 kg. Ringan dan mudah disimpan.",                                   "Tersedia"),
            (2, "Electric Sander",      "Tools",      40_000, "Good",         "Mesin amplas orbital untuk penghalusan kayu atau dinding. Dilengkapi berbagai tingkat kekasaran amplas.",                "Tersedia"),
            (2, "Projector HD",         "Electronics",80_000, "Good",         "Proyektor 1080p Full HD. Cocok untuk presentasi, nonton bareng, atau acara keluarga. Koneksi HDMI & USB.",              "Tersedia"),
            # Riko (3)
            (3, "Food Processor",       "Kitchen",    45_000, "Cukup Baik",   "Chopper, slicer, dan blender dalam satu alat. Ideal untuk persiapan masak skala besar.",                                "Tersedia"),
            (3, "Ice Cream Maker",      "Kitchen",    60_000, "Good",         "Buat hingga 1.5 liter es krim homemade dalam 20-30 menit. Tangki beku terpisah, mudah dioperasikan.",                   "Tersedia"),
            (3, "Jumbo Rice Cooker",    "Kitchen",    20_000, "Good",         "Rice cooker kapasitas 5 liter. Cocok untuk hajatan kecil atau katering. Fungsi warm otomatis.",                         "Sedang Dipinjam"),
            (3, "Artisan Stand Mixer",  "Kitchen",    40_000, "Good",         "Mixer duduk 5 liter 10 kecepatan. Dilengkapi hook, paddle, dan whisk. Ideal untuk membuat adonan kue dan roti.",        "Tersedia"),
            # Salma (4)
            (4, "Foldable Hand Truck",  "Tools",      25_000, "Good",         "Troli lipat kapasitas 80 kg. Roda karet anti gores. Mudah disimpan di sudut sempit.",                                   "Tersedia"),
            (4, "Garden Hose Set",      "Gardening",  15_000, "Good",         "Selang air 15 meter dengan 7 mode semprotan. Cocok untuk menyiram tanaman, taman, atau cuci kendaraan.",                "Tersedia"),
            (4, "Electric Lawn Mower",  "Gardening",  55_000, "Cukup Baik",   "Mesin pemotong rumput listrik. Lebar potong 32 cm. Kabel 10 meter. Cocok untuk halaman ukuran sedang.",                "Tersedia"),
            (4, "Portable Blower",      "Gardening",  20_000, "Good",         "Blower listrik untuk membersihkan daun kering, debu di teras, atau kotoran di garasi. Ringan dan bertenaga.",           "Tersedia"),
        ]
        conn.executemany(
            "INSERT INTO alat (id_pengguna, nama_alat, kategori, harga_sewa, kondisi_alat, deskripsi, status_ketersediaan) VALUES (?,?,?,?,?,?,?)",
            alat_data
        )

        # ── Transaksi ─────────────────────────────────────────────────────────
        # id_alat 11 = Jumbo Rice Cooker (Sedang Dipinjam)
        transaksi_data = [
            (2, 3, 11, "2026-04-26",  1,  20_000, "Berjalan"),   # Diana pinjam dari Riko
            (1, 2,  5, "2026-04-21",  2,  70_000, "Selesai"),    # Dadang pinjam dari Diana
            (4, 2,  6, "2026-04-20",  1,  25_000, "Selesai"),    # Salma pinjam dari Diana
            (3, 4, 14, "2026-04-19",  2,  30_000, "Selesai"),    # Riko pinjam dari Salma
            (1, 3, 10, "2026-04-26",  3, 180_000, "Selesai"),    # Dadang pinjam dari Riko
        ]
        conn.executemany(
            "INSERT INTO transaksi (id_peminjam, id_penyedia, id_alat, tanggal_transaksi, durasi, total_biaya, status) VALUES (?,?,?,?,?,?,?)",
            transaksi_data
        )

        print("Database seeded successfully.")
