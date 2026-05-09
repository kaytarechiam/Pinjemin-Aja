# Pinjemin Aja! — Python/PyQt6 Context

Platform peminjaman alat komunitas. Reimplementasi dari Java/JavaFX ke Python + PyQt6, mengikuti nama kelas dan use case dari dokumen DPPL/CD.

---

## Struktur Folder

```
python/
├── main.py                    # Entry point, App (QStackedWidget)
├── session.py                 # Session singleton
├── context.md                 # File ini
│
├── models/
│   ├── pengguna.py            # Pengguna
│   ├── alat.py                # Alat
│   ├── transaksi.py           # Transaksi
│   ├── dompet_digital.py      # DompetDigital
│   └── riwayat_transaksi.py   # RiwayatTransaksi
│
├── controllers/
│   ├── pengguna_controller.py # PenggunaController
│   ├── alat_controller.py     # AlatController
│   ├── transaksi_controller.py# TransaksiController
│   └── riwayat_controller.py  # RiwayatController
│
├── views/
│   ├── ui_helper.py           # Konstanta warna, widget factory, ShadowCard, Toast
│   ├── login_view.py          # LoginView + _LeftPanel + _FormCard (shared)
│   ├── registrasi_view.py     # RegistrasiView
│   ├── main_window.py         # MainWindow (top navbar + page stack)
│   ├── katalog_view.py        # KatalogView (sidebar kategori + grid kartu)
│   ├── katalog_saya_view.py   # KatalogSayaView (tabel + dialog tambah/edit)
│   ├── riwayat_view.py        # RiwayatView (tabel transaksi)
│   ├── wallet_view.py         # WalletView (sidebar akun + saldo + form)
│   ├── profil_view.py         # ProfilView (sidebar akun + edit profil)
│   └── peminjaman_view.py     # PeminjamanView (detail alat + form pinjam)
│
├── database/
│   ├── database.py            # initialize(), get_connection()
│   └── seeder.py              # seed() — data awal
│
└── resources/
    └── images/                # foto alat (waffle_maker.jpg, dst.)
```

---

## Models

### `Pengguna` (`models/pengguna.py`)
```
__init__(id_pengguna, nama_lengkap, no_wa, alamat, kata_sandi)

Getters: get_id_pengguna(), get_nama_lengkap(), get_no_wa(),
         get_alamat(), get_kata_sandi()
Setters: set_nama_lengkap(), set_no_wa(), set_alamat(), set_kata_sandi()
```

### `Alat` (`models/alat.py`)
```
__init__(id_alat, id_pemilik, nama_pemilik, nama_alat, deskripsi,
         kategori, harga_sewa, kondisi_alat, status_ketersediaan)

Getters: get_id_alat(), get_id_pemilik(), get_nama_pemilik(),
         get_nama_alat(), get_deskripsi(), get_kategori(),
         get_harga_sewa(), get_kondisi_alat(), get_status_ketersediaan()
Setters: set_status_ketersediaan(), set_harga_sewa(), set_deskripsi()

status_ketersediaan values: "Tersedia" | "Dipinjam"
kondisi_alat values: "Good" | "Cukup Baik" | "Perlu Perbaikan"
kategori values: "Kitchen" | "Tools" | "Cleaning" | "Electronics" | "Gardening"
```

### `Transaksi` (`models/transaksi.py`)
```
__init__(id_transaksi, id_peminjam, id_penyedia, id_alat,
         nama_alat, nama_peminjam, nama_penyedia,
         tanggal_transaksi, durasi, total_biaya, status)

Getters: get_id_transaksi(), get_id_peminjam(), get_id_penyedia(),
         get_id_alat(), get_nama_alat(), get_nama_peminjam(),
         get_nama_penyedia(), get_tanggal_transaksi(),
         get_durasi(), get_total_biaya(), get_status()
Setters: set_status()
get_detail() -> str

status values: "Berjalan" | "Selesai"
```

### `DompetDigital` (`models/dompet_digital.py`)
Diakses via PenggunaController, jarang diinstansiasi langsung di view.

### `RiwayatTransaksi` (`models/riwayat_transaksi.py`)
Diakses via RiwayatController. Method penting: `get_daftar_transaksi() -> list[Transaksi]`

---

## Controllers

### `PenggunaController` (`controllers/pengguna_controller.py`)
Menangani UC01–UC08.

```python
# UC01 — Registrasi
proses_registrasi(data: dict) -> bool
  # data keys: nama_lengkap, no_wa, alamat, kata_sandi, konfirmasi_sandi
validasi_input(data: dict) -> bool

# UC02 — Login
proses_login(no_wa: str, sandi: str) -> bool
verifikasi_kredensial(no_wa: str, sandi: str) -> bool

# UC03/UC04 — Profil
ambil_data_profil(id_pengguna: int) -> Optional[Pengguna]
update_profil(id_pengguna: int, data: dict) -> bool
  # data keys: nama_lengkap, no_wa, alamat

# UC05 — Ubah Kata Sandi
ubah_kata_sandi(id_pengguna: int, sandi_lama: str, sandi_baru: str) -> bool

# UC06 — Lihat Saldo
lihat_saldo(id_pengguna: int) -> float

# UC07 — Top Up
proses_isi_ulang(id_pengguna: int, nominal: float) -> bool

# UC08 — Tarik Dana
proses_tarik_dana(id_pengguna: int, nominal: float) -> bool
```

> **Catatan:** View memanggil shorthand `self._ctrl.login()` dan `self._ctrl.registrasi()`.
> Pastikan ada alias/wrapper atau sesuaikan nama pemanggilan ke `proses_login` / `proses_registrasi`.

### `AlatController` (`controllers/alat_controller.py`)
```python
get_semua_alat() -> list[Alat]
get_alat_from_pengguna(id_pengguna: int) -> list[Alat]
get_detail_alat(id_alat: int) -> Optional[Alat]
cari_dan_filter(keyword: str, kategori: str) -> list[Alat]
  # kategori "Semua" = tidak filter kategori
tambah_alat(data: dict) -> bool
  # data keys: id_pengguna, nama_alat, harga_sewa, kategori, kondisi_alat, deskripsi
update_alat(id_alat: int, data: dict) -> bool
hapus_alat(id_alat: int) -> bool
```

### `TransaksiController` (`controllers/transaksi_controller.py`)
```python
proses_peminjaman(id_peminjam: int, id_alat: int, durasi: int) -> bool
cek_ketersediaan_alat(id_alat: int) -> bool
```

### `RiwayatController` (`controllers/riwayat_controller.py`)
```python
load_riwayat(id_pengguna: int) -> RiwayatTransaksi
load_detail_transaksi(id_transaksi: int) -> Optional[Transaksi]
proses_filter(riwayat: RiwayatTransaksi, jenis: str) -> list[Transaksi]
  # jenis: "semua" | "peminjam" | "penyedia"
konfirmasi_pengembalian(id_transaksi: int) -> bool
```

---

## Session (`session.py`)

```python
Session.login(pengguna: Pengguna)       # set current user
Session.logout()                         # clear current user
Session.get_current_user() -> Optional[Pengguna]
Session.is_logged_in() -> bool
```

Singleton class (classmethod semua), tidak perlu diinstansiasi.

---

## UI Layer

### Layout Keseluruhan

```
App (QStackedWidget)
├── [0] LoginView
├── [1] RegistrasiView
└── [2] MainWindow
         ├── Navbar (62px, top)
         └── QStackedWidget (_stack)
              ├── [0] KatalogView
              ├── [1] KatalogSayaView
              ├── [2] RiwayatView
              ├── [3] WalletView
              ├── [4] ProfilView
              └── [5] PeminjamanView  ← dinamis, dibuat saat open detail
```

### `App` (`main.py`)
- `QStackedWidget` sebagai root window
- `_fade_to(index)` — instant switch (NO animasi, untuk menghindari nested `QGraphicsEffect`)
- Login sukses → buat `MainWindow` baru, tambah ke stack di index 2
- Logout → kembali ke `LoginView`

### `MainWindow` (`views/main_window.py`)

**Konstanta halaman:**
```python
PAGE_KATALOG    = 0
PAGE_KATALOG_SY = 1
PAGE_RIWAYAT    = 2
PAGE_WALLET     = 3
PAGE_PROFIL     = 4
PAGE_PEMINJAMAN = 5
```

**Komponen Navbar:**
- Logo emoji + nama app
- `_NavButton` (checkable) — Explore, My Items, History
- Search `QLineEdit` (220×36px, border-radius 18px)
- User avatar `QPushButton` dengan `QMenu` dropdown:
  - 👤 Profile → `_switch_page(PAGE_PROFIL)`
  - 💳 My Wallet → `_switch_page(PAGE_WALLET)`
  - ⏻ Logout → `_on_logout()`

**Signal connections:**
```python
katalog_view.open_detail    → _open_peminjaman(id_alat)
wallet_view.go_profil       → _switch_page(PAGE_PROFIL)
wallet_view.logout_requested→ _on_logout()
profil_view.go_wallet       → _switch_page(PAGE_WALLET)
profil_view.logout_requested→ _on_logout()
```

**Animasi halaman:**
- `QGraphicsOpacityEffect` pada `_stack` (bukan pada child widget)
- Fade out 100ms → switch → fade in 180ms
- Child widget **TIDAK BOLEH** punya `QGraphicsEffect` sendiri

### `LoginView` (`views/login_view.py`)

Layout: `QHBoxLayout` — kiri + kanan

**Komponen yang di-export (dipakai `registrasi_view.py`):**
- `_LeftPanel(QWidget)` — gradient biru (#3D5AF1 → #6B8EFF), lebar 480px
- `_FormCard(QWidget)` — kartu putih rounded, shadow via `paintEvent`

**Signals:**
```python
login_success = pyqtSignal(object)  # emit Pengguna
go_register   = pyqtSignal()
```

**Public methods:**
```python
showFormLogin()         # clear fields + hide error
showPesanError(pesan)   # tampilkan label error merah
```

### `RegistrasiView` (`views/registrasi_view.py`)
Import `_LeftPanel`, `_FormCard` dari `login_view`. Layout identik dua panel.

**Signal:** `go_login = pyqtSignal()`

**Public methods:**
```python
showFormRegistrasi()    # clear semua field
showPesanError(pesan)
```

### `KatalogView` (`views/katalog_view.py`)

Layout: `QHBoxLayout` — sidebar kiri (210px) + konten kanan

**Sidebar kiri:** `_CatButton` (checkable) untuk tiap kategori:
- 📦 All Items, 🍳 Kitchen, 🔧 Tools, 🧹 Cleaning, 📱 Electronics, 🌱 Gardening

**Signal:** `open_detail = pyqtSignal(int)` (emit `id_alat`)

**Public methods:**
```python
showKatalog(daftar_alat=None)   # reset ke semua, load dari controller jika None
search(kw: str)                  # dipanggil oleh MainWindow navbar search
showPesanKosong()
refresh()
```

**Kartu item:** `_HoverCard(QWidget)` — ukuran 210×220px, shadow biru on hover via `paintEvent`

### `KatalogSayaView` (`views/katalog_saya_view.py`)

**Public methods:**
```python
showKatalogSaya(daftar=None)
showFormTambahAlat()
showFormEditAlat(alat: Alat)
showPesanSukses(pesan), showPesanError(pesan)
```

Dialog internal: `_AlatFormDialog(QDialog)` — dipakai untuk tambah dan edit alat.

### `RiwayatView` (`views/riwayat_view.py`)

**Public methods:**
```python
showRiwayat(riwayat=None)       # UC19
showFilterRiwayat(jenis: str)   # UC20 — "semua"|"peminjam"|"penyedia"
showDetailTransaksi(id: int)    # UC21 — buka _DetailDialog
showPesanSukses(pesan), showPesanError(pesan)
```

Tombol "✓ Selesai" muncul hanya kalau user adalah penyedia dan status "Berjalan".

### `WalletView` (`views/wallet_view.py`)

Layout: `QHBoxLayout` — sidebar kiri (220px) + scroll kanan

**Sidebar kiri:** My Wallet (aktif), Profile → emit signal, Logout → emit signal

**Signals:**
```python
go_profil        = pyqtSignal()
logout_requested = pyqtSignal()
```

**Public methods:**
```python
showSaldo(saldo=None)       # refresh dari controller jika None
showFormIsiUlang()          # mode topup
showFormTarikDana()         # mode tarik
showPesanSukses(pesan), showPesanError(pesan)
```

### `ProfilView` (`views/profil_view.py`)

Layout: `QHBoxLayout` — sidebar kiri (220px) + scroll kanan

**Sidebar kiri:** Profile (aktif), My Wallet → emit signal, Logout → emit signal

**Signals:**
```python
go_wallet        = pyqtSignal()
logout_requested = pyqtSignal()
```

**Public methods:**
```python
showProfil(pengguna=None)
showFormEditProfil(pengguna=None)
showFormUbahKataSandi()
showPesanSukses(pesan), showPesanError(pesan)
```

### `PeminjamanView` (`views/peminjaman_view.py`)

Dibuat dinamis di `MainWindow._open_peminjaman(id_alat)`, bukan di `__init__`.
Layout: `QScrollArea` → breadcrumb + `QHBoxLayout` (gambar kiri 400×300px + `ShadowCard` kanan)

**Signals:**
```python
go_back    = pyqtSignal()   # kembali ke KatalogView
go_riwayat = pyqtSignal()   # setelah peminjaman sukses → RiwayatView
```

---

## UI Helper (`views/ui_helper.py`)

### Warna Brand
```python
BLUE        = "#3D5AF1"
BLUE_DARK   = "#2D46D6"
BLUE_LIGHT  = "#EEF1FF"
GREEN       = "#10B981"
GREEN_LIGHT = "#D1FAE5"
RED         = "#EF4444"
RED_LIGHT   = "#FEE2E2"
AMBER       = "#F59E0B"
AMBER_LIGHT = "#FEF3C7"
LIGHT_BG    = "#F7F8FC"
BORDER      = "#E8EAF0"
TEXT_DARK   = "#1A1D2E"
TEXT_MID    = "#4B5563"
TEXT_GRAY   = "#9CA3AF"
WHITE       = "#FFFFFF"
CARD_BG     = "#FFFFFF"
```

### Widget Factories
```python
primary_button(text) -> QPushButton    # gradient biru, hover darken
outline_button(text) -> QPushButton    # border biru, hover fill
styled_input(placeholder) -> QLineEdit # border 1.5px, focus biru
styled_password(placeholder)-> QLineEdit # styled_input + EchoMode.Password
styled_textarea(placeholder)-> QTextEdit
heading(text) -> QLabel                # 22px bold, TEXT_DARK
subheading(text) -> QLabel             # 15px semibold, TEXT_DARK
separator() -> QFrame                  # horizontal 1px BORDER
badge(text, bg, fg) -> QLabel          # pill label tinggi 22px
available_badge()   -> QLabel          # "● Tersedia" hijau
unavailable_badge() -> QLabel          # "● Dipinjam" merah
ongoing_badge()     -> QLabel          # "● Berjalan" amber
completed_badge()   -> QLabel          # "● Selesai"  hijau
```

### Kelas Khusus
```python
ShadowCard(QWidget, radius=14)
```
Kartu putih rounded dengan shadow yang dilukis via `paintEvent` (layered semi-transparent rounded rect offset). **Aman dipakai di dalam `QGraphicsOpacityEffect` parent** karena tidak menggunakan `QGraphicsEffect` sendiri.

```python
add_shadow(widget, **kwargs) -> None
```
**No-op stub.** Jangan hapus pemanggilan ini di tempat lain — keberadaannya mencegah error jika ada kode lama yang masih memanggilnya.

### Dialogs & Toast
```python
show_alert(title, message, parent=None)     # QMessageBox.information
show_error(title, message, parent=None)     # QMessageBox.critical
show_confirm(message, parent=None) -> bool  # Yes/No dialog
show_toast(message, parent, kind="success") # Slide-in toast pojok kanan atas
  # kind: "success" | "error" | "warning" | "info"
```

### Image Map
```python
get_item_pixmap(nama_alat: str, w: int, h: int) -> QPixmap | None
```
Mapping nama alat → file gambar di `resources/images/`. Nama alat harus persis sama dengan key di `ITEM_IMAGE_MAP`.

---

## Constraint Teknis Penting

### Nested `QGraphicsEffect` — DILARANG

Qt tidak mengizinkan `QGraphicsEffect` bersarang. Jika parent widget punya `QGraphicsOpacityEffect`, **semua child/descendant tidak boleh** punya `QGraphicsEffect` apapun (termasuk `QGraphicsDropShadowEffect`).

Situasi di project ini:
- `MainWindow._stack` punya `QGraphicsOpacityEffect` (untuk animasi fade halaman)
- Semua widget di dalam `_stack` (KatalogView, WalletView, dll.) **dilarang** pakai `QGraphicsEffect`
- Shadow diganti dengan `ShadowCard` yang melukis shadow manual di `paintEvent`
- `App._fade_to()` sengaja dibuat instant (no animation) agar tidak menambah layer `QGraphicsEffect` di atas `MainWindow`

**Error yang muncul jika dilanggar:**
```
QPainter::begin: A paint device can only be painted by one painter at a time
QPainter::setWorldTransform: Painter not active
```

### `QRectF` wajib untuk `drawRoundedRect`

PyQt6 tidak menerima argumen float individual:
```python
# SALAH — TypeError
painter.drawRoundedRect(x, y, w, h, rx, ry)

# BENAR
from PyQt6.QtCore import QRectF
painter.drawRoundedRect(QRectF(x, y, w, h), rx, ry)
```

### QSS — selector harus dibungkus `WidgetClass { }`

```python
# SALAH — parse error
btn.setStyleSheet("color: red; QPushButton:hover { color: blue; }")

# BENAR
btn.setStyleSheet("QPushButton { color: red; } QPushButton:hover { color: blue; }")
```

---

## Use Case → File Mapping

| UC   | Deskripsi                   | Controller          | View                   |
|------|-----------------------------|---------------------|------------------------|
| UC01 | Registrasi                  | PenggunaController  | RegistrasiView         |
| UC02 | Login                       | PenggunaController  | LoginView              |
| UC03 | Lihat Profil                | PenggunaController  | ProfilView             |
| UC04 | Edit Profil                 | PenggunaController  | ProfilView             |
| UC05 | Ubah Kata Sandi             | PenggunaController  | ProfilView             |
| UC06 | Lihat Saldo                 | PenggunaController  | WalletView             |
| UC07 | Top Up                      | PenggunaController  | WalletView             |
| UC08 | Tarik Dana                  | PenggunaController  | WalletView             |
| UC09 | Lihat Katalog               | AlatController      | KatalogView            |
| UC10 | Tambah Alat                 | AlatController      | KatalogSayaView        |
| UC11 | Edit Alat                   | AlatController      | KatalogSayaView        |
| UC12 | Hapus Alat                  | AlatController      | KatalogSayaView        |
| UC13 | Lihat Katalog Saya          | AlatController      | KatalogSayaView        |
| UC14 | Cari Alat                   | AlatController      | KatalogView            |
| UC15 | Filter Kategori             | AlatController      | KatalogView            |
| UC16 | Lihat Detail Alat           | AlatController      | PeminjamanView         |
| UC17 | Proses Peminjaman           | TransaksiController | PeminjamanView         |
| UC18 | Konfirmasi Pengembalian     | RiwayatController   | RiwayatView            |
| UC19 | Lihat Riwayat               | RiwayatController   | RiwayatView            |
| UC20 | Filter Riwayat              | RiwayatController   | RiwayatView            |
| UC21 | Detail Transaksi            | RiwayatController   | RiwayatView            |

---

## Database

SQLite, file tunggal. `initialize()` buat tabel jika belum ada. `seed()` insert data awal.

Tabel utama: `pengguna`, `alat`, `transaksi`, `dompet_digital`

Koneksi via `get_connection()` — context manager, auto-commit.
