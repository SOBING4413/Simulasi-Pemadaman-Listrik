<div align="center">

# ⚡ Simulasi Blackout Area
### Sistem Distribusi Listrik + Serangan Siber & Dampak Sosial

![Version](https://img.shields.io/badge/version-2.1.0-blue?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.8+-yellow?style=for-the-badge&logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)
![License](https://img.shields.io/badge/License-Educational-green?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=for-the-badge)

<br/>

> **Simulasi edukasi interaktif** untuk memahami bagaimana serangan siber dapat melumpuhkan infrastruktur listrik, dampaknya terhadap masyarakat, serta cara pemulihannya.

<br/>

**Creator By [Sobing4413](https://github.com/Sobing4413) &nbsp;·&nbsp; Organization [Exter Interactive](#)**

</div>

---

## 📸 Preview

```
⚡ SIMULASI BLACKOUT AREA v2.1.0
┌─────────────────────────────────────────────────────┐
│  🗺️ PETA JARINGAN   │  📊 KONTROL  │  📜 LOG       │
│                      │              │               │
│   [GI Utara]━━━━[GI Timur]         │  [⚡ Blackout] │
│        ┃              ┃             │  [💀 Siber  ] │
│   [GI Barat]━━━━[GI Selatan]       │  [🔧 Pulihkan]│
│                                     │               │
│  🕐 Realtime Clock  📈 Load Chart  │  Timeline...  │
└─────────────────────────────────────────────────────┘
```

---

## 🎯 Tentang Proyek

**Simulasi Blackout Area** adalah aplikasi desktop edukasi berbasis Python yang mensimulasikan jaringan distribusi listrik sebuah kota. Pengguna dapat memicu blackout, melancarkan berbagai jenis serangan siber, menganalisis dampaknya terhadap ekonomi, sosial, dan kesehatan, lalu melakukan pemulihan sistem.

Proyek ini dibuat untuk keperluan **edukasi keamanan siber infrastruktur kritis**, cocok untuk:
- 🎓 Mahasiswa & pelajar IT / Teknik Elektro
- 🔐 Enthusiast keamanan siber
- 📚 Presentasi & demo edukasi
- 🧪 Research & simulasi skenario

---

## ✨ Fitur Utama

### 🗺️ Peta Jaringan Interaktif
- Visualisasi 4 Gardu Induk (GI Utara, Timur, Selatan, Barat) dengan koneksi antar gardu
- 14 area distribusi dengan prioritas berbeda (Rumah Sakit, Industri, Perumahan, dll)
- Ratusan rumah individual dengan generator, panel surya, dan peralatan medis
- Klik gardu/area untuk info detail dan trigger blackout manual
- Minimap di pojok canvas untuk navigasi cepat

### 💀 Simulasi Serangan Siber (6 Jenis)
| Serangan | Severity | Dampak |
|---|---|---|
| 🔓 SCADA System Hack | ⭐⭐⭐⭐⭐ | Remote control gardu induk |
| 🐀 RAT (Remote Access Trojan) | ⭐⭐⭐⭐⭐ | Kendali penuh komputer operator |
| 🦠 Firmware Malware (Stuxnet-style) | ⭐⭐⭐⭐⭐ | Merusak PLC/RTU secara permanen |
| 🕵️ Man-In-The-Middle Attack | ⭐⭐⭐⭐ | Memalsukan data sensor |
| 💣 DDoS Attack | ⭐⭐⭐ | Server monitoring crash |
| 🎣 Spear Phishing | ⭐⭐⭐ | Pintu masuk serangan lebih besar |

### 🌤️ Sistem Cuaca Dinamis
- ☀️ **Cerah** → Risiko rendah
- 🌧️ **Hujan** → Risiko sedang (korsleting, banjir)
- ⛈️ **Badai** → Risiko tinggi (petir, cascade failure 3x lebih sering)
- Mode Auto Cuaca — berubah otomatis setiap 300 tick

### 📊 Analisis Dampak Real-Time
- 💰 **Ekonomi** — estimasi kerugian per jam
- 👥 **Sosial** — jumlah jiwa terdampak, risiko kejahatan
- 🏥 **Kesehatan** — rumah sakit terdampak, pasien ICU berisiko
- 🏗️ **Infrastruktur** — status air, telekomunikasi, transportasi

### 📈 Monitoring & Logging
- Grafik load history 60 tick real-time (sparkline)
- Jam dinding aktual (🕐 realtime clock)
- Timeline kejadian lengkap dengan filter & export CSV
- Log panel dengan color-coded events
- Uptime Score berdasarkan performa sistem
- Export laporan `.txt` lengkap

---

## 🚀 Cara Install & Jalankan

### ✅ Cara Mudah (Recommended)
```
1. Download / clone repository ini
2. Pastikan semua file ada dalam 1 folder:
   📁 SimulasiBlackout/
    ├── main.py
    ├── jalankan.bat
    └── requirements.txt

3. Double-click → jalankan.bat
   (Otomatis cek Python, tkinter, lalu buka simulasi)
```

### 🐍 Cara Manual
```bash
# Pastikan Python 3.8+ sudah terinstall
python --version

# Jalankan langsung
python main.py
```

### 📦 Requirements
```
Tidak ada library eksternal yang perlu diinstall!
Semua menggunakan modul bawaan Python:

✅ tkinter    — GUI framework
✅ random     — Simulasi acak
✅ datetime   — Timestamp & sesi
✅ csv        — Export timeline
✅ json       — Format data
✅ os         — Operasi file
```

> **Belum punya Python?**
> Download di → [python.org/downloads](https://www.python.org/downloads/)
> ⚠️ Saat install, **centang "Add Python to PATH"**

---

## ⌨️ Keyboard Shortcuts

| Key | Fungsi |
|---|---|
| `F1` | Bantuan / Help |
| `F2` | Blackout Otomatis |
| `F3` | Serangan Siber |
| `F4` | Pemulihan Listrik |
| `F5` | Reset Simulasi |
| `F6` | Load Balance |
| `F7` | Scan Kerentanan |
| `F8` | Export Report |
| `F9` | Timeline History |
| `F10` | Toggle Minimap |
| `F11` | Credits |
| `Space` | Pause / Resume |
| `+` / `-` | Speed Up / Down |
| `Ctrl+Z` | Undo Aksi Terakhir |
| `Ctrl+S` | Export Log |
| `Ctrl+1~4` | Ganti View Tab |

---

## 🗂️ Struktur View

```
[Ctrl+1] 🗺️  Jaringan Listrik  — Peta gardu & area distribusi
[Ctrl+2] 🏘️  Denah Perumahan   — Detail rumah per blok
[Ctrl+3] 💀  Serangan Siber    — Topologi keamanan & attack vectors
[Ctrl+4] 📊  Dampak & Analisis — Kartu dampak ekonomi/sosial/health
```

---

## 🔒 Kerentanan yang Disimulasikan

| ID | Nama | Risk Level |
|---|---|---|
| `legacy_systems` | 🖥️ Sistem Lawas (Windows XP) | SANGAT TINGGI |
| `default_password` | 🔑 Password Default | KRITIS |
| `internet_facing` | 🌐 Terhubung Internet Langsung | KRITIS |
| `no_encryption` | 📡 Tanpa Enkripsi (Modbus) | TINGGI |
| `no_monitoring` | 👁️ Tidak Ada IDS/IPS | TINGGI |
| `usb_access` | 💾 Akses USB Bebas | TINGGI |

---

## 📁 Struktur File

```
📁 SimulasiBlackout/
 ├── 📄 main.py           — Source code utama (~2800 baris)
 ├── 🖱️ jalankan.bat      — One-click launcher (Windows)
 ├── 📋 requirements.txt  — Daftar dependensi
 └── 📖 README.md         — Dokumentasi ini
```

---

## 🗺️ Roadmap

- [ ] Simpan & Load state simulasi
- [ ] Lebih banyak jenis gardu & topologi jaringan
- [ ] Mode multiplayer (attacker vs defender)
- [ ] Sound effects & animasi lebih halus
- [ ] Export peta sebagai gambar
- [ ] Dark / Light theme toggle

---

## ⚠️ Disclaimer

> Proyek ini dibuat **semata-mata untuk tujuan edukasi**.
> Semua skenario serangan yang ada hanya simulasi dalam lingkungan virtual tertutup.
> **Tidak ada koneksi ke sistem nyata.**
> Penggunaan teknik atau pengetahuan dari simulasi ini untuk tujuan ilegal adalah tanggung jawab pengguna sepenuhnya dan melanggar hukum yang berlaku.

---

## 👤 Credits

<div align="center">

| | |
|---|---|
| **Creator** | Sobing4413 |
| **Organization** | Exter Interactive |
| **Versi** | 2.1.0 |
| **Bahasa** | Python 3 + Tkinter |
| **Kategori** | Edukasi / Simulasi / Cybersecurity |

<br/>

*Made with ❤️ by Sobing4413 · Exter Interactive*

</div>
