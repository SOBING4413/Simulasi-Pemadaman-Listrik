import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import random
import math
import time
import re
import os
import json
import csv
from datetime import datetime
from collections import defaultdict

# ============================================================
# VERSION
# ============================================================
VERSION = "2.1.0"
CREATOR  = "Sobing4413"
ORG      = "Exter Interactive"

# ============================================================
# KONFIGURASI WARNA
# ============================================================
C = {
    "bg_dark": "#0b0e17", "bg_medium": "#131829", "bg_panel": "#1a1f35",
    "bg_card": "#222845", "accent_blue": "#3b82f6", "accent_cyan": "#06b6d4",
    "accent_green": "#10b981", "accent_yellow": "#f59e0b", "accent_orange": "#f97316",
    "accent_red": "#ef4444", "accent_purple": "#8b5cf6", "accent_pink": "#ec4899",
    "text_primary": "#f1f5f9", "text_secondary": "#94a3b8", "text_muted": "#64748b",
    "grid_line": "#1e2642", "line_active": "#10b981", "line_dead": "#ef4444",
    "gardu_active": "#f59e0b", "gardu_dead": "#ef4444", "area_active": "#10b981",
    "area_dead": "#6b2121", "house_active": "#22c55e", "house_dead": "#7f1d1d",
    "road": "#374151", "road_line": "#6b7280",
    "cyber_red": "#ff2d55", "cyber_green": "#00ff88", "cyber_blue": "#00d4ff",
    "cyber_purple": "#bf5af2", "cyber_yellow": "#ffd60a", "cyber_pink": "#ff6eb4",
    "statusbar_bg": "#0d1120", "minimap_bg": "#0a0d18",
    "notify_bg": "#1e2640", "notify_border": "#3b82f6",
}

# ============================================================
# DATABASE SERANGAN SIBER
# ============================================================
CYBER_ATTACKS = {
    "scada_hack": {
        "name": "🔓 SCADA System Hack",
        "short": "Hacker menguasai 'otak' gardu induk (sistem SCADA) dan mematikan trafo secara remote",
        "severity": 5,
        "impact_economy": "Kerugian Rp 50-500 Miliar",
        "impact_social": "Panik massal, kejahatan naik 300%",
        "impact_health": "RS kehilangan daya, pasien ICU berisiko",
        "technique": "1. Scan jaringan SCADA\n2. Buat malware khusus (Stuxnet-like)\n3. Phishing ke operator\n4. Eksploitasi vulnerability HMI\n5. Install backdoor\n6. Remote control via C2\n7. Matikan proteksi & trip breaker",
        "layman": (
            "🔧 APA ITU SCADA?\n"
            "SCADA = Supervisory Control and Data Acquisition\n"
            "Bayangkan SCADA seperti 'otak' yang mengontrol\n"
            "seluruh jaringan listrik secara otomatis.\n\n"
            "🦠 SERANGAN:\n"
            "Hacker masuk ke sistem SCADA dan mengambil\n"
            "alih kendali gardu induk. Mereka BISA:\n"
            "• Mematikan trafo secara remote\n"
            "• Mengubah setting proteksi\n"
            "• Memalsukan data sensor\n\n"
            "📖 KASUS NYATA:\n"
            "2015: Hacker Rusia mematikan listrik di Ukraina\n"
            "(230.000 orang kehilangan listrik).\n\n"
            "🛡️ PERTAHANAN:\n"
            "• Firewall khusus jaringan SCADA\n"
            "• Sistem deteksi intrusi (IDS)\n"
            "• Update software rutin\n"
            "• Training keamanan operator"
        ),
    },
    "mitm": {
        "name": "🕵️ Man-In-The-Middle Attack",
        "short": "Hacker menyadap komunikasi sensor-kontrol dan memalsukan data tegangan listrik",
        "severity": 4,
        "impact_economy": "Kerugian Rp 20-200 Miliar",
        "impact_social": "Ketidakpercayaan terhadap PLN",
        "impact_health": "Peralatan medis rusak karena overvoltage",
        "technique": "1. ARP Spoofing jaringan internal\n2. Intercept komunikasi Modbus/TCP\n3. Modifikasi data sensor\n4. Inject perintah palsu ke RTU\n5. Delay response untuk cover-up",
        "layman": (
            "🔧 APA ITU MITM?\n"
            "MITM = Man In The Middle (Orang Di Tengah)\n"
            "Bayangkan Anda telepon, tapi ada orang\n"
            "MENYADAP dan mengubah pesan tanpa Anda sadari.\n\n"
            "🦠 SERANGAN PADA GRID:\n"
            "• Sensor kirim: 'Tegangan normal 220V'\n"
            "• Hacker ubah: tetap '220V' (padahal 380V!)\n"
            "• Operator tidak tahu ada masalah\n"
            "• Trafo kelebihan beban → MELEDAK\n\n"
            "📖 KASUS NYATA:\n"
            "2016: Serangan MITM pada jaringan listrik\n"
            "Ukraina, memalsukan data telemetry RTU.\n\n"
            "🛡️ PERTAHANAN:\n"
            "• Enkripsi end-to-end (TLS/SSL)\n"
            "• Certificate pinning\n"
            "• Network segmentation"
        ),
    },
    "ddos": {
        "name": "💣 DDoS Attack",
        "short": "Jutaan data sampah dikirim ke server listrik sampai crash, operator menjadi BUTA",
        "severity": 3,
        "impact_economy": "Kerugian Rp 10-100 Miliar/jam",
        "impact_social": "Kacau, transportasi macet, komunikasi putus",
        "impact_health": "Lift macet, alat medis offline",
        "technique": "1. Rekrut botnet (IoT devices zombie)\n2. SYN Flood ke server HMI/SCADA\n3. UDP Amplification attack\n4. HTTP Flood ke web interface\n5. Bandwidth exhaustion link komunikasi",
        "layman": (
            "🔧 APA ITU DDoS?\n"
            "DDoS = Distributed Denial of Service\n"
            "Bayangkan 10.000 orang menelepon nomor yang sama\n"
            "secara bersamaan. Nomor pasti SIBUK!\n\n"
            "🦠 SERANGAN PADA GRID:\n"
            "• Server monitoring tidak bisa diakses\n"
            "• Operator BUTA - tidak bisa lihat data\n"
            "• Sistem otomatis tidak bisa merespon\n"
            "• Emergency shutdown gagal\n\n"
            "📖 KASUS NYATA:\n"
            "2019: DDoS pada utilitas listrik AS,\n"
            "botnet Mirai kirim 1.2 Tbps ke server SCADA.\n\n"
            "🛡️ PERTAHANAN:\n"
            "• DDoS mitigation service\n"
            "• Rate limiting pada firewall\n"
            "• Redundant server & failover"
        ),
    },
    "rat": {
        "name": "🐀 RAT (Remote Access Trojan)",
        "short": "Hacker 'nongkrong' di komputer operator, bisa lihat layar & kontrol dari jauh",
        "severity": 5,
        "impact_economy": "Kerugian Rp 100-500 Miliar",
        "impact_social": "Krisis kepercayaan publik, hoaks menyebar",
        "impact_health": "Sistem keselamatan dinonaktifkan - BAHAYA",
        "technique": "1. Spear phishing ke engineer\n2. Dropper tersembunyi di dokumen\n3. Persistence via Registry\n4. Keylogger capture kredensial\n5. Lateral movement ke HMI\n6. Remote control via C2\n7. Disable SIS (Safety System)",
        "layman": (
            "🔧 APA ITU RAT?\n"
            "RAT = Remote Access Trojan\n"
            "Bayangkan ada ORANG ASING yang bisa mengontrol\n"
            "komputer Anda dari jauh - melihat layar,\n"
            "mengetik, mengklik - tanpa Anda ketahui!\n\n"
            "🦠 SERANGAN PADA GRID:\n"
            "• Hacker lihat layar operator LIVE\n"
            "• Rekam password & akses login\n"
            "• Ambil alih mouse & keyboard\n"
            "• Matikan breaker/pemutus sirkuit\n"
            "• Hapus log agar tidak terlacak\n\n"
            "📖 KASUS NYATA:\n"
            "2017: Malware Triton di sistem SIS Saudi,\n"
            "dirancang menonaktifkan sistem keselamatan.\n\n"
            "🛡️ PERTAHANAN:\n"
            "• Endpoint Detection & Response\n"
            "• Application whitelisting\n"
            "• Air-gap network"
        ),
    },
    "firmware": {
        "name": "🦠 Firmware Malware (Stuxnet-style)",
        "short": "Virus yang mengganti 'DNA' perangkat, trafo dibiarkan overheat tanpa peringatan",
        "severity": 5,
        "impact_economy": "Kerugian Rp 500M - 1 Triliun",
        "impact_social": "Bencana nasional, darurat sipil",
        "impact_health": "Kerusakan permanen infrastruktur medis",
        "technique": "1. Supply chain compromise\n2. USB drop attack di fasilitas\n3. Exploit zero-day pada PLC/RTU\n4. Rootkit di firmware level\n5. Manipulasi logic PLC stealth\n6. Replay attack untuk cover-up",
        "layman": (
            "🔧 APA ITU FIRMWARE MALWARE?\n"
            "Firmware = software tertanam di hardware.\n"
            "Seperti 'DNA' yang membuat perangkat berfungsi.\n\n"
            "Firmware malware = virus yang MENGGANTI DNA!\n"
            "Perangkat tetap bekerja TAPI dengan cara salah.\n\n"
            "🦠 SERANGAN PADA GRID:\n"
            "• Proteksi relay dimatikan diam-diam\n"
            "• Trafo dibiarkan overheat tanpa peringatan\n"
            "• Breaker tidak trip saat harusnya trip\n"
            "• Data ke operator DIPALSUKAN\n"
            "• Semuanya terlihat NORMAL padahal BAHAYA\n\n"
            "📖 KASUS NYATA:\n"
            "2010: Stuxnet menghancurkan 1.000 centrifuge\n"
            "nuklir Iran. Virus infeksi PLC Siemens,\n"
            "tidak terdeteksi selama BULANAN.\n\n"
            "🛡️ PERTAHANAN:\n"
            "• Firmware integrity verification\n"
            "• Secure boot chain\n"
            "• Regular firmware audit"
        ),
    },
    "phishing": {
        "name": "🎣 Spear Phishing Attack",
        "short": "Email palsu yang menyamar dari atasan, operator klik → komputer terinfeksi malware",
        "severity": 3,
        "impact_economy": "Rp 5-50 Miliar (pintu masuk serangan besar)",
        "impact_social": "Karyawan menjadi korban, trauma",
        "impact_health": "Langkah awal serangan yang lebih besar",
        "technique": "1. OSINT: kumpulkan info target dari LinkedIn\n2. Buat email palsu yang meyakinkan\n3. Sisipkan malicious attachment/link\n4. Social engineering: buat target panik\n5. Setelah klik → malware terinstal\n6. Lateral movement ke jaringan SCADA",
        "layman": (
            "🔧 APA ITU PHISHING?\n"
            "Phishing = Penipuan digital.\n"
            "Bayangkan email TAMPIL dari atasan,\n"
            "meminta klik link update password.\n"
            "Tapi sebenarnya dari HACKER!\n\n"
            "Spear Phishing = Phishing yang DITARGETKAN\n"
            "ke orang tertentu (operator gardu, engineer).\n\n"
            "🦠 SERANGAN PADA GRID:\n"
            "• Email palsu dari 'IT Department'\n"
            "• Lampiran dokumen berisi malware\n"
            "• Link login palsu curi password\n"
            "• Setelah klik, komputer TERINFEKSI\n\n"
            "📖 KASUS NYATA:\n"
            "2015: Serangan Ukraina dimulai dari\n"
            "spear phishing. Email berisi Word dengan\n"
            "macro malicious → BlackEnergy malware.\n\n"
            "🛡️ PERTAHANAN:\n"
            "• Security awareness training\n"
            "• Email filtering & sandboxing\n"
            "• Multi-factor authentication (MFA)"
        ),
    },
}

# ============================================================
# DATABASE KERENTANAN
# ============================================================
VULNS = {
    "legacy_systems": {
        "name": "🖥️ Sistem Lawas (Legacy)",
        "desc": "Software Windows XP/7 yang tidak diupdate. Seperti rumah yang pintunya tidak bisa dikunci.",
        "risk": "SANGAT TINGGI",
        "fix": "Upgrade ke sistem modern, patch management rutin",
    },
    "default_password": {
        "name": "🔑 Password Default",
        "desc": "Perangkat SCADA pakai password bawaan pabrik (admin/admin). Seperti gembok dengan kunci universal!",
        "risk": "KRITIS",
        "fix": "Ganti password segera, gunakan MFA",
    },
    "no_encryption": {
        "name": "📡 Tanpa Enkripsi",
        "desc": "Data sensor dikirim tanpa enkripsi. Seperti surat terbuka yang bisa dibaca siapa saja.",
        "risk": "TINGGI",
        "fix": "Implementasi TLS/SSL untuk semua komunikasi",
    },
    "internet_facing": {
        "name": "🌐 Terhubung Internet Langsung",
        "desc": "HMI bisa diakses dari internet tanpa VPN. Seperti brankas di halaman depan rumah.",
        "risk": "KRITIS",
        "fix": "Air-gap, VPN, firewall, network segmentation",
    },
    "no_monitoring": {
        "name": "👁️ Tidak Ada Monitoring",
        "desc": "Tidak ada sistem pantau aktivitas mencurigakan. Seperti rumah tanpa CCTV dan alarm.",
        "risk": "TINGGI",
        "fix": "Pasang IDS/IPS, SIEM, 24/7 SOC monitoring",
    },
    "usb_access": {
        "name": "💾 Akses USB Bebas",
        "desc": "Operator bisa colok USB bebas di komputer kontrol. Stuxnet menyebar lewat USB!",
        "risk": "TINGGI",
        "fix": "Disable USB, device control policy",
    },
}

# ============================================================
# KEYBOARD SHORTCUTS CONFIG
# ============================================================
SHORTCUTS = {
    "<F1>": ("Bantuan / Help", "_show_help"),
    "<F2>": ("Blackout Otomatis", "_auto_blackout"),
    "<F3>": ("Serangan Siber", "_launch_cyber_attack"),
    "<F4>": ("Pemulihan Listrik", "_start_restoration"),
    "<F5>": ("Reset Simulasi", "_reset_simulation"),
    "<F6>": ("Load Balance", "_load_balance"),
    "<F7>": ("Scan Kerentanan", "_scan_vulnerabilities"),
    "<F8>": ("Export Report", "_export_report"),
    "<F9>": ("Timeline History", "_show_timeline"),
    "<F10>": ("Toggle Minimap", "_toggle_minimap"),
    "<Control-s>": ("Export Log", "_export_log"),
    "<Control-r>": ("Reset", "_reset_simulation"),
    "<Control-z>": ("Undo Aksi Terakhir", "_undo_last_action"),
    "<Control-l>": ("Clear Log", "_clear_log"),
    "<Control-m>": ("Toggle Minimap", "_toggle_minimap"),
    "<Control-1>": ("View: Jaringan", None),
    "<Control-2>": ("View: Perumahan", None),
    "<Control-3>": ("View: Serangan Siber", None),
    "<Control-4>": ("View: Dampak", None),
    "<F11>": ("Credits", "_show_credits"),
    "<space>": ("Pause/Resume", "_toggle_pause"),
    "<plus>": ("Speed +", "_speed_up"),
    "<minus>": ("Speed Down", "_speed_down"),
}


# ============================================================
# KELAS UTAMA
# ============================================================
class BlackoutSimulation:
    def __init__(self, root):
        self.root = root
        self.root.title(f"⚡ Simulasi Blackout Area v{VERSION} | {CREATOR} · {ORG}")
        self.root.geometry("1600x980")
        self.root.minsize(1400, 880)
        self.root.configure(bg=C["bg_dark"])

        # Core state
        self.gardus = []
        self.areas = []
        self.houses = []
        self.running = False
        self.restoring = False
        self.paused = False
        self.simulation_time = 0
        self.simulation_speed = 1.0
        self.weather = "cerah"
        self.total_blackouts = 0
        self.total_restorations = 0
        self.cascade_count = 0
        self.cyber_attacks_count = 0
        self.animation_frame = 0
        self.pulse_phase = 0
        self.lightning_flash = False
        self.tooltip_window = None
        self.show_legend = True
        self.show_connections = True
        self.show_labels = True
        self.active_attacks = []
        self.cyber_defense_level = 50
        self.view_mode = "network"
        self.show_minimap = True

        # Timeline history
        self.timeline_events = []
        self.undo_stack = []  # For undo support

        # Real-time load history chart (last 60 ticks)
        self.load_history: list[float] = [0.0] * 60
        self.load_history_idx = 0

        # Dirty flag – only redraw canvas when something changed
        self._dirty = True

        # Notification queue
        self.notification_queue = []
        self.notification_active = False
        self.notification_window = None

        # Score / uptime tracking
        self.session_start = datetime.now()
        self.uptime_score = 100.0
        self.total_downtime_seconds = 0
        self.blackout_start_time = None

        # Progress bar animation
        self.progress_value = 0
        self.progress_direction = 1
        self.progress_active = False

        self._build_ui()
        self._init_default_data()
        self._bind_shortcuts()
        self._start_animation_loop()

    # ============================================================
    # KEYBOARD SHORTCUTS
    # ============================================================
    def _bind_shortcuts(self):
        self.root.bind("<F1>", lambda e: self._show_help())
        self.root.bind("<F2>", lambda e: self._auto_blackout())
        self.root.bind("<F3>", lambda e: self._launch_cyber_attack())
        self.root.bind("<F4>", lambda e: self._start_restoration())
        self.root.bind("<F5>", lambda e: self._reset_simulation())
        self.root.bind("<F6>", lambda e: self._load_balance())
        self.root.bind("<F7>", lambda e: self._scan_vulnerabilities())
        self.root.bind("<F8>", lambda e: self._export_report())
        self.root.bind("<F9>", lambda e: self._show_timeline())
        self.root.bind("<F10>", lambda e: self._toggle_minimap())
        self.root.bind("<F11>", lambda e: self._show_credits())
        self.root.bind("<Control-s>", lambda e: self._export_log())
        self.root.bind("<Control-r>", lambda e: self._reset_simulation())
        self.root.bind("<Control-z>", lambda e: self._undo_last_action())
        self.root.bind("<Control-l>", lambda e: self._clear_log())
        self.root.bind("<Control-m>", lambda e: self._toggle_minimap())
        self.root.bind("<Control-Key-1>", lambda e: self._switch_view("network"))
        self.root.bind("<Control-Key-2>", lambda e: self._switch_view("housing"))
        self.root.bind("<Control-Key-3>", lambda e: self._switch_view("cyber"))
        self.root.bind("<Control-Key-4>", lambda e: self._switch_view("impact"))
        self.root.bind("<space>", lambda e: self._toggle_pause())
        self.root.bind("<plus>", lambda e: self._speed_up())
        self.root.bind("<minus>", lambda e: self._speed_down())
        self.root.bind("<KP_Add>", lambda e: self._speed_up())
        self.root.bind("<KP_Subtract>", lambda e: self._speed_down())

    def _toggle_pause(self):
        self.paused = not self.paused
        state = "⏸ PAUSE" if self.paused else "▶ RESUME"
        self.lbl_pause_status.config(
            text=state,
            fg=C["accent_yellow"] if self.paused else C["accent_green"]
        )
        self._notify("⏸ Simulasi dijeda" if self.paused else "▶ Simulasi dilanjutkan",
                     color=C["accent_yellow"] if self.paused else C["accent_green"])

    def _speed_up(self):
        new_speed = min(3.0, round(self.simulation_speed + 0.5, 1))
        self.simulation_speed = new_speed
        self.speed_var.set(new_speed)
        self._notify(f"🏃 Speed: {new_speed}x", color=C["accent_cyan"])

    def _speed_down(self):
        new_speed = max(0.5, round(self.simulation_speed - 0.5, 1))
        self.simulation_speed = new_speed
        self.speed_var.set(new_speed)
        self._notify(f"🐌 Speed: {new_speed}x", color=C["accent_cyan"])

    def _undo_last_action(self):
        if not self.undo_stack:
            self._notify("⚠️ Tidak ada aksi untuk di-undo", color=C["accent_yellow"])
            return
        action = self.undo_stack.pop()
        action_type = action.get("type")
        if action_type == "blackout":
            g_id = action["gardu_id"]
            for g in self.gardus:
                if g["id"] == g_id:
                    g["status"] = True
                    g["trip_count"] = max(0, g["trip_count"] - 1)
                    for area in self.areas:
                        if area["gardu_id"] == g_id:
                            area["status"] = True
                    self._add_log(f"↩️ Undo: {g['name']} dipulihkan", "restore")
                    break
            self._draw_all()
            self._update_all()
            self._dirty = True
            self._notify("↩️ Undo berhasil!", color=C["accent_green"])
        else:
            self._notify("↩️ Undo tidak tersedia untuk aksi ini", color=C["accent_yellow"])

    # ============================================================
    # NOTIFICATION SYSTEM
    # ============================================================
    def _notify(self, message, color=None, duration=2500):
        """Queue a non-blocking popup notification."""
        if color is None:
            color = C["accent_cyan"]
        self.notification_queue.append({"msg": message, "color": color, "duration": duration})
        if not self.notification_active:
            self._show_next_notification()

    def _show_next_notification(self):
        if not self.notification_queue:
            self.notification_active = False
            return
        self.notification_active = True
        data = self.notification_queue.pop(0)

        # Destroy previous notification if any
        if self.notification_window and self.notification_window.winfo_exists():
            self.notification_window.destroy()

        nw = tk.Toplevel(self.root)
        nw.wm_overrideredirect(True)
        nw.attributes("-topmost", True)
        nw.configure(bg=C["notify_bg"])

        # Position: bottom-right of root window
        rx = self.root.winfo_x() + self.root.winfo_width() - 350
        ry = self.root.winfo_y() + self.root.winfo_height() - 120

        nw.wm_geometry(f"340x55+{rx}+{ry}")

        outer = tk.Frame(nw, bg=data["color"], padx=2, pady=2)
        outer.pack(fill=tk.BOTH, expand=True)
        inner = tk.Frame(outer, bg=C["notify_bg"], padx=12, pady=8)
        inner.pack(fill=tk.BOTH, expand=True)

        tk.Label(inner, text=data["msg"], font=("Segoe UI", 10, "bold"),
                 fg=data["color"], bg=C["notify_bg"], anchor=tk.W).pack(fill=tk.X)

        self.notification_window = nw

        # Auto close
        self.root.after(data["duration"], lambda: self._close_notification(nw))

    def _close_notification(self, nw):
        try:
            if nw and nw.winfo_exists():
                nw.destroy()
        except Exception:
            pass
        self.notification_active = False
        if self.notification_queue:
            self.root.after(200, self._show_next_notification)

    # ============================================================
    # TIMELINE HISTORY
    # ============================================================
    def _add_timeline_event(self, event_type, description, severity="info"):
        ts = datetime.now().strftime("%H:%M:%S")
        sim_time = self._format_sim_time()
        self.timeline_events.append({
            "timestamp": ts,
            "sim_time": sim_time,
            "type": event_type,
            "description": description,
            "severity": severity,
            "blackouts": self.total_blackouts,
            "restorations": self.total_restorations,
            "cyber": self.cyber_attacks_count,
            "weather": self.weather,
        })

    def _format_sim_time(self):
        h = self.simulation_time // 3600
        m = (self.simulation_time % 3600) // 60
        s = self.simulation_time % 60
        return f"{h:02d}:{m:02d}:{s:02d}"

    def _show_timeline(self):
        tw = tk.Toplevel(self.root)
        tw.title("📅 Timeline Kejadian")
        tw.geometry("800x600")
        tw.configure(bg=C["bg_dark"])

        tk.Label(tw, text="📅 TIMELINE KEJADIAN SIMULASI",
                 font=("Segoe UI", 14, "bold"), fg=C["accent_cyan"], bg=C["bg_dark"]).pack(pady=10)

        # Filter frame
        ff = tk.Frame(tw, bg=C["bg_panel"])
        ff.pack(fill=tk.X, padx=10, pady=(0, 5))
        tk.Label(ff, text="Filter:", font=("Segoe UI", 9), fg=C["text_secondary"], bg=C["bg_panel"]).pack(side=tk.LEFT, padx=5)
        filter_var = tk.StringVar(value="all")
        for txt, val in [("Semua", "all"), ("Blackout", "blackout"), ("Siber", "cyber"), ("Pemulihan", "restore"), ("Cuaca", "weather")]:
            tk.Radiobutton(ff, text=txt, variable=filter_var, value=val,
                           bg=C["bg_panel"], fg=C["text_primary"], selectcolor=C["bg_dark"],
                           font=("Segoe UI", 8), command=lambda: self._refresh_timeline(tlist, filter_var.get())
                           ).pack(side=tk.LEFT, padx=4)

        # Count badge
        count_lbl = tk.Label(ff, text=f"Total: {len(self.timeline_events)} kejadian",
                              font=("Segoe UI", 9, "bold"), fg=C["accent_yellow"], bg=C["bg_panel"])
        count_lbl.pack(side=tk.RIGHT, padx=10)

        # Timeline list
        tc = tk.Frame(tw, bg=C["bg_dark"])
        tc.pack(fill=tk.BOTH, expand=True, padx=10)

        tlist = tk.Text(tc, bg=C["bg_dark"], fg=C["text_primary"], font=("Consolas", 9),
                        wrap=tk.WORD, relief=tk.FLAT, padx=6, pady=6)
        ts_scroll = tk.Scrollbar(tc, command=tlist.yview)
        tlist.configure(yscrollcommand=ts_scroll.set)
        ts_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        tlist.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Color tags
        tlist.tag_configure("header", foreground=C["accent_cyan"], font=("Consolas", 9, "bold"))
        tlist.tag_configure("blackout", foreground=C["accent_red"])
        tlist.tag_configure("cyber", foreground=C["cyber_pink"])
        tlist.tag_configure("restore", foreground=C["accent_green"])
        tlist.tag_configure("weather", foreground=C["accent_purple"])
        tlist.tag_configure("info", foreground=C["text_secondary"])
        tlist.tag_configure("ts", foreground=C["text_muted"])

        self._refresh_timeline(tlist, "all")

        btn_row = tk.Frame(tw, bg=C["bg_dark"])
        btn_row.pack(fill=tk.X, padx=10, pady=5)
        tk.Button(btn_row, text="💾 Export CSV", command=lambda: self._export_timeline_csv(),
                  bg=C["accent_blue"], fg="white", font=("Segoe UI", 9, "bold"),
                  cursor="hand2", relief=tk.FLAT, padx=15, pady=4).pack(side=tk.LEFT, padx=4)
        tk.Button(btn_row, text="🗑️ Hapus History", command=lambda: (self.timeline_events.clear(), self._refresh_timeline(tlist, "all")),
                  bg=C["accent_red"], fg="white", font=("Segoe UI", 9, "bold"),
                  cursor="hand2", relief=tk.FLAT, padx=15, pady=4).pack(side=tk.LEFT, padx=4)
        tk.Button(btn_row, text="✅ Tutup", command=tw.destroy,
                  bg=C["bg_card"], fg="white", font=("Segoe UI", 9, "bold"),
                  cursor="hand2", relief=tk.FLAT, padx=15, pady=4).pack(side=tk.RIGHT, padx=4)

    def _refresh_timeline(self, tlist, filter_type="all"):
        tlist.config(state=tk.NORMAL)
        tlist.delete("1.0", tk.END)
        events = self.timeline_events
        if filter_type != "all":
            events = [e for e in events if e["type"] == filter_type]

        if not events:
            tlist.insert(tk.END, "Belum ada kejadian tercatat.\n", "info")
        else:
            tlist.insert(tk.END, f"{'#':<4} {'Waktu':<10} {'SimTime':<10} {'Tipe':<12} Deskripsi\n", "header")
            tlist.insert(tk.END, "─" * 70 + "\n", "ts")
            for i, ev in enumerate(reversed(events), 1):
                tag = ev["type"]
                prefix = {
                    "blackout": "⚡", "cyber": "💀", "restore": "🔧",
                    "weather": "🌤️", "info": "ℹ️"
                }.get(tag, "•")
                tlist.insert(tk.END, f"{i:<4} ", "ts")
                tlist.insert(tk.END, f"{ev['timestamp']:<10} {ev['sim_time']:<10} ", "ts")
                tlist.insert(tk.END, f"{ev['type']:<12} ", tag)
                tlist.insert(tk.END, f"{prefix} {ev['description']}\n", tag)

        tlist.config(state=tk.DISABLED)
        tlist.see(tk.END)

    def _export_timeline_csv(self):
        fp = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV", "*.csv"), ("All", "*.*")],
            title="Export Timeline CSV"
        )
        if fp:
            with open(fp, "w", newline="", encoding="utf-8") as f:
                w = csv.DictWriter(f, fieldnames=["timestamp", "sim_time", "type", "description",
                                                   "severity", "blackouts", "restorations", "cyber", "weather"])
                w.writeheader()
                w.writerows(self.timeline_events)
            self._notify("💾 Timeline diekspor ke CSV!", color=C["accent_green"])

    # ============================================================
    # EXPORT REPORT
    # ============================================================
    def _export_report(self):
        fp = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Report", "*.txt"), ("All", "*.*")],
            title="Export Laporan Simulasi"
        )
        if not fp:
            return

        now = datetime.now()
        session_dur = now - self.session_start
        active_gardu = sum(1 for g in self.gardus if g["status"])
        active_areas = sum(1 for a in self.areas if a["status"] and self.gardus[a["gardu_id"]]["status"])
        total_pop = sum(a.get("population", 0) for a in self.areas)
        affected_pop = sum(a.get("population", 0) for a in self.areas if not (a["status"] and self.gardus[a["gardu_id"]]["status"]))
        total_vuln = sum(len(g["vulnerabilities"]) for g in self.gardus)
        total_cap = sum(g["capacity"] for g in self.gardus)
        total_load = sum(g["load"] for g in self.gardus if g["status"])
        compromised = sum(1 for g in self.gardus if g.get("compromised"))

        lines = [
            "=" * 60,
            f"  LAPORAN SIMULASI BLACKOUT v{VERSION}",
            f"  Tanggal: {now.strftime('%d %B %Y %H:%M:%S')}",
            "=" * 60,
            "",
            "📋 INFORMASI SESI",
            f"  Mulai sesi   : {self.session_start.strftime('%H:%M:%S')}",
            f"  Durasi sesi  : {str(session_dur).split('.')[0]}",
            f"  Waktu simulasi: {self._format_sim_time()}",
            f"  Speed terakhir: {self.simulation_speed}x",
            "",
            "⚡ STATISTIK INSIDEN",
            f"  Total Blackout   : {self.total_blackouts}",
            f"  Cascade Failure  : {self.cascade_count}",
            f"  Serangan Siber   : {self.cyber_attacks_count}",
            f"  Pemulihan        : {self.total_restorations}",
            "",
            "🏭 STATUS JARINGAN SAAT INI",
            f"  Gardu Aktif  : {active_gardu}/{len(self.gardus)}",
            f"  Area Nyala   : {active_areas}/{len(self.areas)}",
            f"  Total Kapasitas: {total_cap} MW",
            f"  Beban Aktif  : {total_load} MW",
            f"  Utilisasi    : {(total_load/total_cap*100) if total_cap else 0:.1f}%",
            f"  Gardu Dihack : {compromised}",
            "",
            "👥 DAMPAK SOSIAL",
            f"  Total Populasi : {total_pop:,} jiwa",
            f"  Terdampak      : {affected_pop:,} jiwa",
            f"  Persentase     : {(affected_pop/total_pop*100) if total_pop else 0:.1f}%",
            "",
            "🔒 KEAMANAN SIBER",
            f"  Level Pertahanan   : {self.cyber_defense_level}%",
            f"  Total Kerentanan   : {total_vuln}",
            f"  Gardu Terkompromi  : {compromised}",
            "",
            "🌤️ KONDISI CUACA",
            f"  Cuaca Saat Ini : {self.weather.upper()}",
            "",
            "📊 DETAIL GARDU",
        ]

        for g in self.gardus:
            lp = (g["load"] / g["capacity"] * 100) if g["capacity"] > 0 else 0
            status = "AKTIF" if g["status"] else "MATI"
            comp = " [DIHACK]" if g.get("compromised") else ""
            lines.append(f"  {g['name']:15} | {status}{comp:10} | {g['load']:3}/{g['capacity']:3} MW ({lp:5.1f}%) | Trip:{g['trip_count']}x | Vuln:{len(g['vulnerabilities'])}")

        lines += [
            "",
            "📅 TIMELINE KEJADIAN (10 Terakhir)",
        ]
        recent = self.timeline_events[-10:] if self.timeline_events else []
        if recent:
            for ev in reversed(recent):
                lines.append(f"  [{ev['timestamp']}] [{ev['type'].upper():10}] {ev['description']}")
        else:
            lines.append("  (tidak ada kejadian)")

        lines += [
            "",
            "=" * 60,
            f"  ⚠️ INI HANYA SIMULASI EDUKASI",
            f"  Creator  : {CREATOR}",
            f"  Organization: {ORG}",
            f"  Versi    : v{VERSION}",
            "=" * 60,
        ]

        with open(fp, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

        self._add_log(f"📄 Laporan diekspor: {os.path.basename(fp)}", "success")
        self._notify("📄 Laporan berhasil diekspor!", color=C["accent_green"])

    # ============================================================
    # BUILD UI
    # ============================================================
    def _build_ui(self):
        # TOP BAR
        top = tk.Frame(self.root, bg=C["bg_panel"], height=55)
        top.pack(fill=tk.X)
        top.pack_propagate(False)

        tf = tk.Frame(top, bg=C["bg_panel"])
        tf.pack(side=tk.LEFT, padx=15, fill=tk.Y)

        tk.Label(tf, text=f"⚡ SIMULASI BLACKOUT AREA v{VERSION}",
                 font=("Segoe UI", 15, "bold"), fg=C["accent_cyan"], bg=C["bg_panel"]).pack(anchor=tk.W, pady=(6, 0))
        tk.Label(tf, text=f"Sistem Distribusi Listrik + Serangan Siber & Dampak Sosial | F1=Bantuan | F11=Credits | by {CREATOR} · {ORG}",
                 font=("Segoe UI", 8), fg=C["text_muted"], bg=C["bg_panel"]).pack(anchor=tk.W)

        # STATUS FRAME
        sf = tk.Frame(top, bg=C["bg_panel"])
        sf.pack(side=tk.RIGHT, padx=15, fill=tk.Y)

        self.lbl_top_status = tk.Label(sf, text="🟢 SISTEM NORMAL",
                                        font=("Segoe UI", 11, "bold"), fg=C["accent_green"], bg=C["bg_panel"])
        self.lbl_top_status.pack(anchor=tk.E, pady=(6, 0))

        self.lbl_top_time = tk.Label(sf, text="⏱ 00:00:00",
                                      font=("Segoe UI", 8), fg=C["text_muted"], bg=C["bg_panel"])
        self.lbl_top_time.pack(anchor=tk.E)

        # Real-time wall clock
        self.lbl_realtime_clock = tk.Label(sf, text="🕐 --:--:--",
                                            font=("Segoe UI", 8, "bold"), fg=C["accent_cyan"], bg=C["bg_panel"])
        self.lbl_realtime_clock.pack(anchor=tk.E)

        # Credits button
        tk.Button(sf, text=f"© {ORG}", command=self._show_credits,
                  bg=C["bg_dark"], fg=C["accent_purple"], font=("Segoe UI", 7, "bold"),
                  relief=tk.FLAT, cursor="hand2", padx=4, pady=1).pack(anchor=tk.E, pady=(0, 3))

        # PAUSE STATUS
        self.lbl_pause_status = tk.Label(sf, text="▶ RUNNING",
                                          font=("Segoe UI", 8, "bold"), fg=C["accent_green"], bg=C["bg_panel"])
        self.lbl_pause_status.pack(anchor=tk.E)

        # WEATHER FRAME
        wf = tk.Frame(top, bg=C["bg_panel"])
        wf.pack(side=tk.RIGHT, padx=15, fill=tk.Y)

        self.lbl_weather = tk.Label(wf, text="☀️ Cerah",
                                     font=("Segoe UI", 10, "bold"), fg=C["accent_yellow"], bg=C["bg_panel"])
        self.lbl_weather.pack(anchor=tk.E, pady=(6, 0))

        self.lbl_weather_risk = tk.Label(wf, text="Risiko: Rendah",
                                          font=("Segoe UI", 8), fg=C["accent_green"], bg=C["bg_panel"])
        self.lbl_weather_risk.pack(anchor=tk.E)

        # CYBER FRAME
        cf = tk.Frame(top, bg=C["bg_panel"])
        cf.pack(side=tk.RIGHT, padx=15, fill=tk.Y)

        self.lbl_cyber_threat = tk.Label(cf, text="🔒 Ancaman: RENDAH",
                                          font=("Segoe UI", 10, "bold"), fg=C["accent_green"], bg=C["bg_panel"])
        self.lbl_cyber_threat.pack(anchor=tk.E, pady=(6, 0))

        self.lbl_active_attacks = tk.Label(cf, text="Serangan aktif: 0",
                                            font=("Segoe UI", 8), fg=C["text_muted"], bg=C["bg_panel"])
        self.lbl_active_attacks.pack(anchor=tk.E)

        # ============================================================
        # VIEW TABS + DEFENSE SLIDER
        # ============================================================
        tab_frame = tk.Frame(self.root, bg=C["bg_medium"], height=40)
        tab_frame.pack(fill=tk.X)
        tab_frame.pack_propagate(False)

        self.view_buttons = {}
        view_tabs = [
            ("🗺️ Jaringan [Ctrl+1]", "network"),
            ("🏘️ Perumahan [Ctrl+2]", "housing"),
            ("💀 Serangan Siber [Ctrl+3]", "cyber"),
            ("📊 Dampak [Ctrl+4]", "impact")
        ]
        for text, mode in view_tabs:
            btn = tk.Button(tab_frame, text=text,
                            command=lambda m=mode: self._switch_view(m),
                            bg=C["accent_blue"] if mode == "network" else C["bg_card"],
                            fg="white" if mode == "network" else C["text_secondary"],
                            font=("Segoe UI", 9, "bold"), relief=tk.FLAT, cursor="hand2",
                            padx=12, pady=4,
                            activebackground=C["accent_blue"], activeforeground="white")
            btn.pack(side=tk.LEFT, padx=2, pady=3)
            self.view_buttons[mode] = btn

        # DEFENSE SLIDER
        df = tk.Frame(tab_frame, bg=C["bg_medium"])
        df.pack(side=tk.RIGHT, padx=10, fill=tk.Y)

        tk.Label(df, text="🛡️ Pertahanan Siber:",
                 font=("Segoe UI", 8), fg=C["text_muted"], bg=C["bg_medium"]).pack(side=tk.LEFT, pady=5)
        self.defense_var = tk.IntVar(value=50)
        tk.Scale(df, from_=0, to=100, orient=tk.HORIZONTAL,
                 variable=self.defense_var, bg=C["bg_medium"], fg=C["text_primary"],
                 troughcolor=C["bg_dark"], highlightthickness=0, font=("Segoe UI", 7),
                 length=120, command=self._on_defense_change).pack(side=tk.LEFT, pady=3)
        self.lbl_defense = tk.Label(df, text="50%", font=("Segoe UI", 8, "bold"),
                                     fg=C["accent_yellow"], bg=C["bg_medium"])
        self.lbl_defense.pack(side=tk.LEFT, padx=3)

        # ============================================================
        # PROGRESS BAR (animated, shows during operations)
        # ============================================================
        self.progress_frame = tk.Frame(self.root, bg=C["bg_medium"], height=4)
        self.progress_frame.pack(fill=tk.X)
        self.progress_bar_canvas = tk.Canvas(self.progress_frame, bg=C["bg_dark"],
                                              height=4, highlightthickness=0)
        self.progress_bar_canvas.pack(fill=tk.X)

        # ============================================================
        # MAIN CONTAINER
        # ============================================================
        main = tk.Frame(self.root, bg=C["bg_dark"])
        main.pack(fill=tk.BOTH, expand=True, padx=8, pady=(0, 0))

        self._build_canvas(main)
        self._build_center(main)
        self._build_right(main)

        # ============================================================
        # STATUS BAR (bottom)
        # ============================================================
        self._build_status_bar()

    def _build_status_bar(self):
        """Professional status bar at the bottom."""
        sb = tk.Frame(self.root, bg=C["statusbar_bg"], height=26,
                      highlightbackground=C["bg_card"], highlightthickness=1)
        sb.pack(fill=tk.X, side=tk.BOTTOM)
        sb.pack_propagate(False)

        # Left: shortcuts hint
        self.lbl_sb_hint = tk.Label(sb, text="F2:Blackout | F3:Siber | F4:Pulihkan | F8:Report | F9:Timeline | F11:Credits | Ctrl+Z:Undo",
                                     font=("Segoe UI", 7), fg=C["text_muted"], bg=C["statusbar_bg"])
        self.lbl_sb_hint.pack(side=tk.LEFT, padx=8)

        # Separator
        tk.Label(sb, text="|", fg=C["bg_card"], bg=C["statusbar_bg"]).pack(side=tk.LEFT)

        # Realtime clock (wall time)
        self.lbl_sb_realtime = tk.Label(sb, text="🕐 --:--:--",
                                         font=("Segoe UI", 7, "bold"), fg=C["accent_cyan"], bg=C["statusbar_bg"])
        self.lbl_sb_realtime.pack(side=tk.LEFT, padx=6)

        # Right: version + score
        self.lbl_sb_score = tk.Label(sb, text="Uptime Score: 100.0%",
                                      font=("Segoe UI", 7, "bold"), fg=C["accent_green"], bg=C["statusbar_bg"])
        self.lbl_sb_score.pack(side=tk.RIGHT, padx=10)

        tk.Label(sb, text="|", fg=C["bg_card"], bg=C["statusbar_bg"]).pack(side=tk.RIGHT)

        # Credits in status bar
        self.lbl_sb_credits = tk.Label(sb, text=f"© {CREATOR} · {ORG}",
                                        font=("Segoe UI", 7, "bold"), fg=C["accent_purple"], bg=C["statusbar_bg"],
                                        cursor="hand2")
        self.lbl_sb_credits.pack(side=tk.RIGHT, padx=8)
        self.lbl_sb_credits.bind("<Button-1>", lambda e: self._show_credits())

        tk.Label(sb, text="|", fg=C["bg_card"], bg=C["statusbar_bg"]).pack(side=tk.RIGHT)

        self.lbl_sb_speed = tk.Label(sb, text="Speed: 1.0x",
                                      font=("Segoe UI", 7), fg=C["text_secondary"], bg=C["statusbar_bg"])
        self.lbl_sb_speed.pack(side=tk.RIGHT, padx=8)

        tk.Label(sb, text="|", fg=C["bg_card"], bg=C["statusbar_bg"]).pack(side=tk.RIGHT)

        self.lbl_sb_session = tk.Label(sb, text="Sesi: 00:00:00",
                                        font=("Segoe UI", 7), fg=C["text_secondary"], bg=C["statusbar_bg"])
        self.lbl_sb_session.pack(side=tk.RIGHT, padx=8)

        tk.Label(sb, text="|", fg=C["bg_card"], bg=C["statusbar_bg"]).pack(side=tk.RIGHT)

        self.lbl_sb_weather = tk.Label(sb, text="☀️ Cerah",
                                        font=("Segoe UI", 7), fg=C["accent_yellow"], bg=C["statusbar_bg"])
        self.lbl_sb_weather.pack(side=tk.RIGHT, padx=8)

        tk.Label(sb, text="|", fg=C["bg_card"], bg=C["statusbar_bg"]).pack(side=tk.RIGHT)

        self.lbl_sb_mode = tk.Label(sb, text=f"v{VERSION}",
                                     font=("Segoe UI", 7), fg=C["text_muted"], bg=C["statusbar_bg"])
        self.lbl_sb_mode.pack(side=tk.RIGHT, padx=8)

    def _build_canvas(self, parent):
        outer = tk.Frame(parent, bg=C["bg_card"],
                         highlightbackground=C["accent_blue"], highlightthickness=1)
        outer.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 4))

        hdr = tk.Frame(outer, bg=C["bg_medium"], height=32)
        hdr.pack(fill=tk.X)
        hdr.pack_propagate(False)
        self.lbl_canvas_title = tk.Label(hdr, text="🗺️ PETA JARINGAN LISTRIK",
                                         font=("Segoe UI", 9, "bold"),
                                         fg=C["accent_cyan"], bg=C["bg_medium"])
        self.lbl_canvas_title.pack(side=tk.LEFT, padx=10, pady=4)

        # Canvas controls
        btn_data = [
            ("📋 Legenda", self._toggle_legend),
            ("🔗 Koneksi", self._toggle_connections),
            ("🏷️ Label", self._toggle_labels),
            ("🗺️ Minimap", self._toggle_minimap),
        ]
        for text, cmd in btn_data:
            tk.Button(hdr, text=text, command=cmd, bg=C["bg_card"],
                      fg=C["text_secondary"], font=("Segoe UI", 7),
                      relief=tk.FLAT, cursor="hand2", padx=4).pack(side=tk.RIGHT, padx=2, pady=2)

        # Canvas + minimap frame
        canvas_container = tk.Frame(outer, bg=C["bg_dark"])
        canvas_container.pack(fill=tk.BOTH, expand=True, padx=3, pady=3)

        self.canvas = tk.Canvas(canvas_container, bg=C["bg_dark"],
                                 highlightthickness=0, cursor="crosshair")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.bind("<Button-1>", self._on_canvas_click)
        self.canvas.bind("<Motion>", self._on_canvas_hover)
        self.canvas.bind("<Leave>", self._hide_tooltip)

        # Minimap
        self.minimap_frame = tk.Frame(canvas_container, bg=C["minimap_bg"],
                                       highlightbackground=C["accent_blue"], highlightthickness=1,
                                       width=160, height=110)
        self.minimap_frame.place(relx=1.0, rely=0.0, anchor=tk.NE, x=-4, y=4)
        self.minimap_canvas = tk.Canvas(self.minimap_frame, bg=C["minimap_bg"],
                                         width=160, height=110, highlightthickness=0)
        self.minimap_canvas.pack()
        tk.Label(self.minimap_frame, text="MINIMAP", font=("Segoe UI", 6, "bold"),
                 fg=C["text_muted"], bg=C["minimap_bg"]).place(x=4, y=2)

    def _build_center(self, parent):
        center = tk.Frame(parent, bg=C["bg_panel"], width=335,
                          highlightbackground=C["accent_blue"], highlightthickness=1)
        center.pack(side=tk.LEFT, fill=tk.Y, padx=4)
        center.pack_propagate(False)

        cs = tk.Canvas(center, bg=C["bg_panel"], highlightthickness=0)
        sb = tk.Scrollbar(center, orient=tk.VERTICAL, command=cs.yview)
        sf = tk.Frame(cs, bg=C["bg_panel"])
        sf.bind("<Configure>", lambda e: cs.configure(scrollregion=cs.bbox("all")))
        cs.create_window((0, 0), window=sf, anchor=tk.NW, width=315)
        cs.configure(yscrollcommand=sb.set)
        sb.pack(side=tk.RIGHT, fill=tk.Y)
        cs.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # KONTROL
        ctrl = tk.LabelFrame(sf, text="🎮 KONTROL [Shortcuts tersedia]",
                              font=("Segoe UI", 9, "bold"),
                              bg=C["bg_card"], fg=C["accent_cyan"], padx=10, pady=8)
        ctrl.pack(fill=tk.X, padx=6, pady=(6, 3))

        # Main action buttons with shortcut hints
        self.btn_auto = tk.Button(ctrl, text="⚡ BLACKOUT OTOMATIS  [F2]",
                                   command=self._auto_blackout,
                                   bg=C["accent_red"], fg="white",
                                   font=("Segoe UI", 9, "bold"), height=2,
                                   cursor="hand2", relief=tk.FLAT)
        self.btn_auto.pack(fill=tk.X, pady=2)

        self.btn_cyber = tk.Button(ctrl, text="💀 SERANGAN SIBER  [F3]",
                                    command=self._launch_cyber_attack,
                                    bg=C["cyber_red"], fg="white",
                                    font=("Segoe UI", 9, "bold"), height=2,
                                    cursor="hand2", relief=tk.FLAT)
        self.btn_cyber.pack(fill=tk.X, pady=2)

        self.btn_restore = tk.Button(ctrl, text="🔧 PEMULIHAN LISTRIK  [F4]",
                                      command=self._start_restoration,
                                      bg=C["accent_green"], fg="white",
                                      font=("Segoe UI", 9, "bold"), height=2,
                                      cursor="hand2", relief=tk.FLAT)
        self.btn_restore.pack(fill=tk.X, pady=2)

        r1 = tk.Frame(ctrl, bg=C["bg_card"])
        r1.pack(fill=tk.X, pady=2)
        tk.Button(r1, text="⚖️ Load [F6]", command=self._load_balance,
                  bg=C["accent_purple"], fg="white", font=("Segoe UI", 8, "bold"),
                  cursor="hand2", relief=tk.FLAT).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 1))
        tk.Button(r1, text="🔍 Scan [F7]", command=self._scan_vulnerabilities,
                  bg=C["accent_orange"], fg="white", font=("Segoe UI", 8, "bold"),
                  cursor="hand2", relief=tk.FLAT).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=1)
        tk.Button(r1, text="📅 Timeline [F9]", command=self._show_timeline,
                  bg=C["accent_pink"], fg="white", font=("Segoe UI", 8, "bold"),
                  cursor="hand2", relief=tk.FLAT).pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(1, 0))

        r2 = tk.Frame(ctrl, bg=C["bg_card"])
        r2.pack(fill=tk.X, pady=2)
        tk.Button(r2, text="📄 Report [F8]", command=self._export_report,
                  bg=C["accent_blue"], fg="white", font=("Segoe UI", 8, "bold"),
                  cursor="hand2", relief=tk.FLAT).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 1))
        tk.Button(r2, text="↩️ Undo [Ctrl+Z]", command=self._undo_last_action,
                  bg=C["bg_medium"], fg=C["text_primary"], font=("Segoe UI", 8, "bold"),
                  cursor="hand2", relief=tk.FLAT).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=1)
        tk.Button(r2, text="❓ Help [F1]", command=self._show_help,
                  bg=C["bg_medium"], fg=C["text_primary"], font=("Segoe UI", 8, "bold"),
                  cursor="hand2", relief=tk.FLAT).pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(1, 0))

        r3 = tk.Frame(ctrl, bg=C["bg_card"])
        r3.pack(fill=tk.X, pady=2)
        tk.Button(r3, text="🔄 Reset [F5]", command=self._reset_simulation,
                  bg=C["accent_red"], fg="white", font=("Segoe UI", 8, "bold"),
                  cursor="hand2", relief=tk.FLAT).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 1))

        self.btn_pause = tk.Button(r3, text="⏸ Pause [Space]", command=self._toggle_pause,
                                    bg=C["accent_yellow"], fg=C["bg_dark"], font=("Segoe UI", 8, "bold"),
                                    cursor="hand2", relief=tk.FLAT)
        self.btn_pause.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(1, 0))

        # SPEED
        spf = tk.Frame(ctrl, bg=C["bg_card"])
        spf.pack(fill=tk.X, pady=3)
        tk.Label(spf, text="🏃 Speed [+/-]:", font=("Segoe UI", 8),
                 fg=C["text_secondary"], bg=C["bg_card"]).pack(side=tk.LEFT)
        self.speed_var = tk.DoubleVar(value=1.0)
        tk.Scale(spf, from_=0.5, to=3.0, resolution=0.5, orient=tk.HORIZONTAL,
                 variable=self.speed_var, bg=C["bg_card"], fg=C["text_primary"],
                 troughcolor=C["bg_medium"], highlightthickness=0, font=("Segoe UI", 7),
                 command=lambda v: self._on_speed_change(float(v))
                 ).pack(side=tk.LEFT, fill=tk.X, expand=True)

        # CUACA
        wf = tk.LabelFrame(sf, text="🌤️ CUACA", font=("Segoe UI", 9, "bold"),
                            bg=C["bg_card"], fg=C["accent_cyan"], padx=10, pady=6)
        wf.pack(fill=tk.X, padx=6, pady=3)
        self.weather_var = tk.StringVar(value="cerah")
        for text, value in [("☀️ Cerah", "cerah"), ("🌧️ Hujan", "hujan"), ("⛈️ Badai", "badai")]:
            tk.Radiobutton(wf, text=text, variable=self.weather_var, value=value,
                           command=self._on_weather_change, bg=C["bg_card"],
                           fg=C["text_primary"], selectcolor=C["bg_medium"],
                           font=("Segoe UI", 8)).pack(anchor=tk.W)
        self.auto_weather_var = tk.BooleanVar(value=True)
        tk.Checkbutton(wf, text="🔄 Auto cuaca", variable=self.auto_weather_var,
                       bg=C["bg_card"], fg=C["text_secondary"],
                       selectcolor=C["bg_medium"], font=("Segoe UI", 7)).pack(anchor=tk.W)

        # STATUS
        stf = tk.LabelFrame(sf, text="📊 STATUS SISTEM", font=("Segoe UI", 9, "bold"),
                             bg=C["bg_card"], fg=C["accent_cyan"], padx=10, pady=6)
        stf.pack(fill=tk.X, padx=6, pady=3)
        self.lbl_status = tk.Label(stf, text="✅ SEMUA AMAN",
                                   font=("Segoe UI", 11, "bold"),
                                   bg=C["bg_card"], fg=C["accent_green"])
        self.lbl_status.pack(anchor=tk.W, pady=1)
        self.lbl_stats_areas = tk.Label(stf, text="💡 Area Nyala: 0/0",
                                        font=("Segoe UI", 9), bg=C["bg_card"], fg=C["text_primary"])
        self.lbl_stats_areas.pack(anchor=tk.W)
        self.lbl_stats_gardu = tk.Label(stf, text="🏭 Gardu Aktif: 0/0",
                                        font=("Segoe UI", 9), bg=C["bg_card"], fg=C["text_primary"])
        self.lbl_stats_gardu.pack(anchor=tk.W)
        self.lbl_stats_load = tk.Label(stf, text="⚡ Beban: 0 MW",
                                       font=("Segoe UI", 9), bg=C["bg_card"], fg=C["text_primary"])
        self.lbl_stats_load.pack(anchor=tk.W)
        self.load_canvas = tk.Canvas(stf, bg=C["bg_medium"], height=20, highlightthickness=0)
        self.load_canvas.pack(fill=tk.X, pady=3)

        # Real-time load history mini-chart
        tk.Label(stf, text="📈 Load History (60 tick):", font=("Segoe UI", 7),
                 fg=C["text_muted"], bg=C["bg_card"]).pack(anchor=tk.W)
        self.chart_canvas = tk.Canvas(stf, bg=C["bg_medium"], height=40, highlightthickness=0)
        self.chart_canvas.pack(fill=tk.X, pady=(0, 3))

        # Uptime score
        self.lbl_uptime = tk.Label(stf, text="📈 Uptime Score: 100.0%",
                                    font=("Segoe UI", 8, "bold"), bg=C["bg_card"], fg=C["accent_green"])
        self.lbl_uptime.pack(anchor=tk.W)

        # GARDU DETAIL
        gf = tk.LabelFrame(sf, text="🏭 DETAIL GARDU", font=("Segoe UI", 9, "bold"),
                            bg=C["bg_card"], fg=C["accent_cyan"], padx=10, pady=6)
        gf.pack(fill=tk.X, padx=6, pady=3)
        self.gardu_widgets = []
        for i in range(5):
            fr = tk.Frame(gf, bg=C["bg_medium"])
            fr.pack(fill=tk.X, pady=1)
            ln = tk.Label(fr, text=f"Gardu {i+1}", font=("Segoe UI", 8, "bold"),
                          bg=C["bg_medium"], fg=C["text_primary"], anchor=tk.W)
            ln.pack(fill=tk.X, padx=4, pady=(2, 0))
            ld = tk.Label(fr, text="---", font=("Segoe UI", 7),
                          bg=C["bg_medium"], fg=C["text_secondary"], anchor=tk.W)
            ld.pack(fill=tk.X, padx=4, pady=(0, 1))
            bar = tk.Canvas(fr, bg=C["bg_dark"], height=6, highlightthickness=0)
            bar.pack(fill=tk.X, padx=4, pady=(0, 2))
            self.gardu_widgets.append({"frame": fr, "name": ln, "detail": ld, "bar": bar})

        # STATISTIK
        st2 = tk.LabelFrame(sf, text="📈 STATISTIK", font=("Segoe UI", 9, "bold"),
                             bg=C["bg_card"], fg=C["accent_cyan"], padx=10, pady=6)
        st2.pack(fill=tk.X, padx=6, pady=3)
        self.lbl_stat_blackouts = tk.Label(st2, text="⚡ Blackout: 0", font=("Segoe UI", 8),
                                           bg=C["bg_card"], fg=C["text_secondary"])
        self.lbl_stat_blackouts.pack(anchor=tk.W)
        self.lbl_stat_cascades = tk.Label(st2, text="🔥 Cascade: 0", font=("Segoe UI", 8),
                                          bg=C["bg_card"], fg=C["text_secondary"])
        self.lbl_stat_cascades.pack(anchor=tk.W)
        self.lbl_stat_cyber = tk.Label(st2, text="💀 Serangan Siber: 0", font=("Segoe UI", 8),
                                       bg=C["bg_card"], fg=C["text_secondary"])
        self.lbl_stat_cyber.pack(anchor=tk.W)
        self.lbl_stat_restorations = tk.Label(st2, text="🔧 Pemulihan: 0", font=("Segoe UI", 8),
                                              bg=C["bg_card"], fg=C["text_secondary"])
        self.lbl_stat_restorations.pack(anchor=tk.W)

        # INFO
        inf = tk.LabelFrame(sf, text="ℹ️ INFO TERSELEKSI", font=("Segoe UI", 9, "bold"),
                             bg=C["bg_card"], fg=C["accent_cyan"], padx=10, pady=6)
        inf.pack(fill=tk.X, padx=6, pady=3)
        self.lbl_info = tk.Label(inf, text="Klik gardu/area di peta untuk detail.",
                                 font=("Segoe UI", 8), bg=C["bg_card"], fg=C["text_secondary"],
                                 justify=tk.LEFT, wraplength=270)
        self.lbl_info.pack(anchor=tk.W)

    def _build_right(self, parent):
        right = tk.Frame(parent, bg=C["bg_panel"], width=330,
                         highlightbackground=C["accent_blue"], highlightthickness=1)
        right.pack(side=tk.RIGHT, fill=tk.Y, padx=(4, 0))
        right.pack_propagate(False)

        lh = tk.Frame(right, bg=C["bg_medium"], height=32)
        lh.pack(fill=tk.X)
        lh.pack_propagate(False)
        tk.Label(lh, text="📜 LOG KEJADIAN", font=("Segoe UI", 9, "bold"),
                 fg=C["accent_cyan"], bg=C["bg_medium"]).pack(side=tk.LEFT, padx=8, pady=4)

        # Log buttons with shortcuts
        for txt, cmd in [("📄 Report [F8]", self._export_report),
                         ("💾 Log [Ctrl+S]", self._export_log),
                         ("🗑️", self._clear_log)]:
            tk.Button(lh, text=txt, command=cmd, bg=C["bg_card"],
                      fg=C["text_secondary"], font=("Segoe UI", 7), relief=tk.FLAT,
                      cursor="hand2").pack(side=tk.RIGHT, padx=2, pady=2)

        lc = tk.Frame(right, bg=C["bg_dark"])
        lc.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)
        self.log_text = tk.Text(lc, bg=C["bg_dark"], fg=C["text_primary"],
                                font=("Consolas", 8), wrap=tk.WORD,
                                insertbackground=C["text_primary"],
                                selectbackground=C["accent_blue"],
                                relief=tk.FLAT, padx=6, pady=6)
        ls = tk.Scrollbar(lc, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=ls.set)
        ls.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        for tag, color in [("timestamp", C["text_muted"]), ("info", C["accent_blue"]),
                           ("success", C["accent_green"]), ("warning", C["accent_yellow"]),
                           ("danger", C["accent_red"]), ("critical", "#ff6b6b"),
                           ("restore", C["accent_cyan"]), ("weather", C["accent_purple"]),
                           ("separator", C["text_muted"]), ("cyber", C["cyber_pink"]),
                           ("cyber_warn", C["cyber_yellow"]), ("cyber_info", C["cyber_blue"]),
                           ("defense", C["cyber_green"])]:
            kw = {"foreground": color}
            if tag == "critical":
                kw["font"] = ("Consolas", 8, "bold")
            self.log_text.tag_configure(tag, **kw)

        # SHORTCUT REFERENCE
        gf = tk.LabelFrame(right, text="⌨️ KEYBOARD SHORTCUTS", font=("Segoe UI", 9, "bold"),
                            bg=C["bg_card"], fg=C["accent_cyan"], padx=8, pady=5)
        gf.pack(fill=tk.X, padx=4, pady=(0, 4))
        shortcuts_display = [
            ("F2", "Blackout Otomatis"),
            ("F3", "Serangan Siber"),
            ("F4", "Pemulihan"),
            ("F5", "Reset"),
            ("F6", "Load Balance"),
            ("F7", "Scan Kerentanan"),
            ("F8", "Export Report"),
            ("F9", "Timeline"),
            ("F10", "Toggle Minimap"),
            ("F11", "Credits"),
            ("Space", "Pause/Resume"),
            ("+/-", "Speed Up/Down"),
            ("Ctrl+Z", "Undo"),
            ("Ctrl+1~4", "Ganti View"),
        ]
        for key, desc in shortcuts_display:
            row = tk.Frame(gf, bg=C["bg_card"])
            row.pack(fill=tk.X, pady=0)
            tk.Label(row, text=f"[{key}]", font=("Consolas", 7, "bold"),
                     fg=C["accent_yellow"], bg=C["bg_card"], width=10, anchor=tk.W).pack(side=tk.LEFT)
            tk.Label(row, text=desc, font=("Segoe UI", 7),
                     fg=C["text_secondary"], bg=C["bg_card"], anchor=tk.W).pack(side=tk.LEFT)

    # ============================================================
    # DATA INIT
    # ============================================================
    def _init_default_data(self):
        self.gardus.clear()
        self.areas.clear()
        self.houses.clear()
        self.canvas.delete("all")
        self.simulation_time = 0
        self.total_blackouts = 0
        self.total_restorations = 0
        self.cascade_count = 0
        self.cyber_attacks_count = 0
        self.active_attacks.clear()
        self.timeline_events.clear()
        self.undo_stack.clear()
        self.uptime_score = 100.0
        self.session_start = datetime.now()
        self.blackout_start_time = None

        gardu_data = [
            {"name": "GI Utara", "x": 180, "y": 160, "capacity": 150,
             "desc": "Wilayah utara kota", "protocol": "IEC 61850",
             "os": "Windows Server 2019", "firewall": True, "ids": True},
            {"name": "GI Timur", "x": 460, "y": 130, "capacity": 120,
             "desc": "Wilayah timur & industri", "protocol": "Modbus TCP",
             "os": "Windows 7 SP1", "firewall": False, "ids": False},
            {"name": "GI Selatan", "x": 580, "y": 340, "capacity": 140,
             "desc": "Wilayah selatan & pusat kota", "protocol": "DNP3",
             "os": "Linux RHEL 8", "firewall": True, "ids": True},
            {"name": "GI Barat", "x": 150, "y": 380, "capacity": 100,
             "desc": "Wilayah barat & perumahan", "protocol": "IEC 104",
             "os": "Windows XP Embedded", "firewall": False, "ids": False},
        ]

        for i, gd in enumerate(gardu_data):
            vulns = []
            if "XP" in gd["os"]:
                vulns.append("legacy_systems")
            if not gd["firewall"]:
                vulns.extend(["internet_facing", "default_password"])
            if not gd["ids"]:
                vulns.append("no_monitoring")
            if gd["protocol"] == "Modbus TCP":
                vulns.append("no_encryption")
            vulns.append("usb_access")

            self.gardus.append({
                "id": i, "name": gd["name"], "x": gd["x"], "y": gd["y"],
                "capacity": gd["capacity"], "load": 0, "status": True,
                "desc": gd["desc"], "protocol": gd["protocol"], "os": gd["os"],
                "firewall": gd["firewall"], "ids": gd["ids"], "trip_count": 0,
                "vulnerabilities": vulns, "scada_online": True, "compromised": False,
            })

        area_data = [
            ("RS Umum Kota", 200, 90, 0, 25, 1, "⭐", "Rumah Sakit Utama", 0),
            ("Pabrik Timur", 380, 90, 1, 40, 2, "🏭", "Kawasan Industri", 0),
            ("Pasar Swalayan", 500, 180, 2, 30, 2, "🛒", "Pusat Perbelanjaan", 0),
            ("Perumahan Utara A", 120, 260, 0, 20, 3, "🏠", "Komplek Perumahan", 150),
            ("Perumahan Utara B", 250, 290, 0, 15, 3, "🏠", "Komplek Perumahan", 100),
            ("Kantor PLN", 340, 220, 1, 10, 2, "🏢", "Kantor Pusat PLN", 0),
            ("Perumahan Timur", 440, 250, 1, 18, 3, "🏠", "Komplek Perumahan", 120),
            ("RS Rujukan", 560, 220, 2, 22, 1, "🏥", "Rumah Sakit Rujukan", 0),
            ("Pusat Kota", 490, 330, 2, 35, 2, "🏙️", "Pusat Bisnis", 0),
            ("Perumahan Selatan", 630, 390, 2, 16, 3, "🏠", "Komplek Perumahan", 90),
            ("Sekolah Negeri", 220, 410, 3, 8, 3, "🏫", "Kompleks Sekolah", 0),
            ("Perumahan Barat A", 100, 450, 3, 12, 3, "🏠", "Komplek Perumahan", 80),
            ("Perumahan Barat B", 220, 490, 3, 10, 3, "🏠", "Komplek Perumahan", 60),
            ("Masjid & Fasos", 350, 410, 3, 5, 3, "🕌", "Fasilitas Sosial", 0),
        ]

        for i, (name, ax, ay, gid, load, pri, icon, desc, hc) in enumerate(area_data):
            pl = {1: "Kritis", 2: "Penting", 3: "Normal"}[pri]
            self.areas.append({
                "id": i, "name": name, "x": ax, "y": ay,
                "gardu_id": gid, "load": load, "status": True,
                "type": "area", "priority": pri, "priority_label": pl,
                "icon": icon, "desc": desc, "original_gardu_id": gid,
                "house_count": hc, "population": hc * 4 if hc else 0,
            })
            self.gardus[gid]["load"] += load

        # GENERATE HOUSES
        self.houses.clear()
        for area in self.areas:
            if area["house_count"] > 0 and "Perumahan" in area["name"]:
                nb = max(1, area["house_count"] // 10)
                hpb = area["house_count"] // nb
                for blk in range(nb):
                    for h in range(hpb):
                        self.houses.append({
                            "id": len(self.houses),
                            "area_id": area["id"],
                            "area_name": area["name"],
                            "block": blk + 1,
                            "number": f"B{blk+1}-{h+1:03d}",
                            "status": True,
                            "family_size": random.randint(2, 7),
                            "has_generator": random.random() < 0.05,
                            "has_solar": random.random() < 0.08,
                            "has_medical_equipment": random.random() < 0.03,
                        })

        self._draw_all()
        self._update_all()
        self._add_log(f"⚡ Simulasi Blackout v{VERSION} dimulai.", "info")
        self._add_log(f"✅ {len(self.gardus)} gardu, {len(self.areas)} area, {len(self.houses)} rumah.", "success")
        self._add_log("💡 Tekan F1 untuk melihat semua keyboard shortcuts!", "cyber_info")
        self._add_log("─" * 40, "separator")
        self._add_timeline_event("info", f"Simulasi dimulai v{VERSION}", "info")
        self._notify(f"⚡ Simulasi Blackout v{VERSION} siap!", color=C["accent_cyan"], duration=3000)

    # ============================================================
    # VIEW SWITCHING
    # ============================================================
    def _switch_view(self, mode):
        self.view_mode = mode
        for m, btn in self.view_buttons.items():
            btn.config(
                bg=C["accent_blue"] if m == mode else C["bg_card"],
                fg="white" if m == mode else C["text_secondary"]
            )
        titles = {
            "network": "🗺️ PETA JARINGAN LISTRIK",
            "housing": "🏘️ DENAH PERUMAHAN DETAIL",
            "cyber": "💀 PETA SERANGAN SIBER",
            "impact": "📊 DAMPAK & ANALISIS"
        }
        self.lbl_canvas_title.config(text=titles.get(mode, ""))
        self._draw_all()

    # ============================================================
    # DRAWING
    # ============================================================
    def _draw_all(self):
        self.canvas.delete("all")
        W = self.canvas.winfo_width() or 750
        H = self.canvas.winfo_height() or 550
        for x in range(0, W, 40):
            self.canvas.create_line(x, 0, x, H, fill=C["grid_line"])
        for y in range(0, H, 40):
            self.canvas.create_line(0, y, W, y, fill=C["grid_line"])

        if self.paused:
            self.canvas.create_text(W // 2, H // 2, text="⏸ PAUSE",
                                    font=("Segoe UI", 48, "bold"), fill=C["accent_yellow"],
                                    stipple="gray50")

        if self.view_mode == "network":
            self._draw_network(W, H)
        elif self.view_mode == "housing":
            self._draw_housing(W, H)
        elif self.view_mode == "cyber":
            self._draw_cyber(W, H)
        elif self.view_mode == "impact":
            self._draw_impact(W, H)

        # Draw minimap
        if self.show_minimap and self.view_mode == "network":
            self._draw_minimap()

        # Progress bar animation
        self._draw_progress_bar()

    def _draw_minimap(self):
        mc = self.minimap_canvas
        mc.delete("all")
        # Scale factor
        W = self.canvas.winfo_width() or 750
        H = self.canvas.winfo_height() or 550
        mw, mh = 160, 110
        sx = mw / max(W, 1)
        sy = mh / max(H, 1)

        mc.create_rectangle(0, 0, mw, mh, fill=C["minimap_bg"], outline="")

        # Draw connections
        for area in self.areas:
            g = self.gardus[area["gardu_id"]]
            active = g["status"] and area["status"]
            color = C["line_active"] if active else C["line_dead"]
            mc.create_line(g["x"] * sx, g["y"] * sy + 10,
                           area["x"] * sx, area["y"] * sy + 10,
                           fill=color, width=1)

        # Draw gardus
        for g in self.gardus:
            mx, my = g["x"] * sx, g["y"] * sy + 10
            color = C["gardu_active"] if g["status"] else C["gardu_dead"]
            if g.get("compromised"):
                color = C["cyber_red"]
            mc.create_rectangle(mx - 5, my - 4, mx + 5, my + 4, fill=color, outline="")

        # Draw areas
        for area in self.areas:
            ax, ay = area["x"] * sx, area["y"] * sy + 10
            g = self.gardus[area["gardu_id"]]
            active = g["status"] and area["status"]
            color = C["area_active"] if active else C["area_dead"]
            mc.create_oval(ax - 3, ay - 3, ax + 3, ay + 3, fill=color, outline="")

        mc.create_text(mw // 2, 6, text="MINIMAP", font=("Segoe UI", 5, "bold"),
                       fill=C["text_muted"])

    def _draw_progress_bar(self):
        """Animated progress bar during active operations."""
        pb = self.progress_bar_canvas
        pb.delete("all")
        pw = self.progress_bar_canvas.winfo_width() or 800

        if self.progress_active:
            # Animated moving bar
            bar_w = 200
            x = self.progress_value
            color = C["cyber_red"] if self.running else C["accent_green"] if self.restoring else C["accent_blue"]
            pb.create_rectangle(x, 0, min(x + bar_w, pw), 4, fill=color, outline="")
            if x + bar_w > pw:
                pb.create_rectangle(0, 0, (x + bar_w) - pw, 4, fill=color, outline="")
        else:
            # Static full bar when idle
            ga = sum(1 for g in self.gardus if g["status"])
            total = max(len(self.gardus), 1)
            ratio = ga / total
            color = C["accent_green"] if ratio == 1.0 else C["accent_yellow"] if ratio > 0.5 else C["accent_red"]
            pb.create_rectangle(0, 0, pw * ratio, 4, fill=color, outline="")

    def _draw_network(self, W, H):
        self._draw_weather(W, H)
        if self.show_connections:
            self._draw_connections()
        self._draw_gardus()
        self._draw_areas()
        if self.show_legend:
            self._draw_legend(W, H)
        if self.lightning_flash:
            self.canvas.create_rectangle(0, 0, W, H, fill="white", stipple="gray25")

    def _draw_weather(self, W, H):
        if self.weather == "hujan":
            for _ in range(25):
                rx, ry = random.randint(0, W), random.randint(0, H)
                self.canvas.create_line(rx, ry, rx - 3, ry + 10, fill="#4a6fa5")
        elif self.weather == "badai":
            for _ in range(50):
                rx, ry = random.randint(0, W), random.randint(0, H)
                self.canvas.create_line(rx, ry, rx - 5, ry + 15, fill="#6b8fc7")
            self.canvas.create_rectangle(0, 0, W, H, fill="#000000", stipple="gray12")

    def _draw_connections(self):
        for area in self.areas:
            g = self.gardus[area["gardu_id"]]
            active = g["status"] and area["status"]
            kw = {"fill": C["line_active"] if active else C["line_dead"],
                  "width": 2 if active else 1}
            if not active:
                kw["dash"] = (5, 5)
            self.canvas.create_line(g["x"], g["y"] + 30, area["x"], area["y"] - 20, **kw)
            if active and self.pulse_phase % 20 < 10:
                mx = (g["x"] + area["x"]) / 2
                my = (g["y"] + 30 + area["y"] - 22) / 2
                self.canvas.create_oval(mx - 2, my - 2, mx + 2, my + 2,
                                        fill=C["accent_cyan"], outline="")

    def _draw_gardus(self):
        for g in self.gardus:
            x, y = g["x"], g["y"]
            active = g["status"]
            if active:
                gr = 48 + (self.pulse_phase % 8)
                self.canvas.create_oval(x - gr, y - gr + 5, x + gr, y + gr + 5,
                                        fill="", outline=C["accent_yellow"], width=1, stipple="gray25")
            bc = C["gardu_active"] if active else C["gardu_dead"]
            oc = "#f59e0b" if active else "#991b1b"
            self.canvas.create_rectangle(x - 40, y - 28, x + 40, y + 28,
                                         fill=bc, outline=oc, width=3)
            if active:
                self.canvas.create_text(x, y - 5, text="⚡", font=("Segoe UI", 16))
                lp = (g["load"] / g["capacity"]) * 100 if g["capacity"] > 0 else 0
                lc = C["accent_green"] if lp < 70 else C["accent_yellow"] if lp < 100 else C["accent_red"]
                self.canvas.create_text(x, y + 16, text=f"{g['load']}/{g['capacity']} MW",
                                        font=("Consolas", 7, "bold"), fill=lc)
            else:
                self.canvas.create_text(x, y - 5, text="☠️", font=("Segoe UI", 14))
                self.canvas.create_text(x, y + 14, text="BLACKOUT",
                                        font=("Segoe UI", 7, "bold"), fill="white")
                self.canvas.create_line(x - 25, y - 18, x + 25, y + 8, fill=C["accent_red"], width=3)
                self.canvas.create_line(x + 25, y - 18, x - 25, y + 8, fill=C["accent_red"], width=3)
            if g.get("compromised"):
                self.canvas.create_rectangle(x - 42, y - 30, x + 42, y + 30,
                                             fill="", outline=C["cyber_red"], width=2, dash=(3, 3))
                self.canvas.create_text(x, y - 42, text="💀 HACKED",
                                        font=("Segoe UI", 7, "bold"), fill=C["cyber_red"])
            self.canvas.create_line(x, y + 28, x, y + 4, fill="#6b7280", width=4)
            self.canvas.create_line(x - 12, y + 48, x + 12, y + 48, fill="#6b7280", width=3)
            if self.show_labels:
                self.canvas.create_text(x, y - 40, text=g["name"],
                                        font=("Segoe UI", 8, "bold"), fill=C["text_primary"])
                st = "🟢 AKTIF" if active else "🔴 MATI"
                self.canvas.create_text(x, y - 52, text=st, font=("Segoe UI", 6),
                                        fill=C["accent_green"] if active else C["accent_red"])

    def _draw_areas(self):
        for area in self.areas:
            x, y = area["x"], area["y"]
            g = self.gardus[area["gardu_id"]]
            active = g["status"] and area["status"]
            r = 16
            fill = C["area_active"] if active else C["area_dead"]
            outline = "#34d399" if active else "#7f1d1d"
            icon = area["icon"] if active else "🌑"
            self.canvas.create_oval(x - r, y - r, x + r, y + r,
                                    fill=fill, outline=outline, width=2)
            self.canvas.create_text(x, y, text=icon, font=("Segoe UI", 12))
            if area["priority"] == 1:
                self.canvas.create_text(x + r + 4, y - r - 4, text="⭐", font=("Segoe UI", 8))
            if self.show_labels:
                self.canvas.create_text(x, y + r + 9, text=area["name"],
                                        font=("Segoe UI", 6), fill=C["text_primary"], width=70)
                self.canvas.create_text(x, y + r + 19, text=f"{area['load']} MW",
                                        font=("Consolas", 5), fill=C["text_muted"])

    def _draw_legend(self, W, H):
        lx, ly = 10, H - 120
        self.canvas.create_rectangle(lx, ly, lx + 175, ly + 110,
                                     fill=C["bg_card"], outline=C["accent_blue"])
        self.canvas.create_text(lx + 87, ly + 10, text="📋 LEGENDA",
                                font=("Segoe UI", 7, "bold"), fill=C["accent_cyan"])
        for i, (ic, txt, cl) in enumerate([
            ("🟢", "Area Nyala", C["accent_green"]),
            ("🔴", "Area Padam", C["accent_red"]),
            ("⚡", "Gardu Aktif", C["accent_yellow"]),
            ("☠️", "Gardu Mati", C["accent_red"]),
            ("💀", "Gardu Dihack", C["cyber_red"]),
            ("⭐", "Prioritas Kritis", C["accent_orange"]),
        ]):
            iy = ly + 24 + i * 15
            self.canvas.create_text(lx + 12, iy, text=ic, font=("Segoe UI", 7), fill=cl)
            self.canvas.create_text(lx + 25, iy, text=txt, font=("Segoe UI", 6),
                                    fill=C["text_secondary"], anchor=tk.W)

    def _draw_housing(self, W, H):
        self.canvas.create_text(W // 2, 20,
                                text="🏘️ DENAH PERUMAHAN - Klik Area untuk Detail",
                                font=("Segoe UI", 12, "bold"), fill=C["accent_cyan"])
        housing = [a for a in self.areas if a["house_count"] > 0]
        cols = min(4, len(housing))
        rows = math.ceil(len(housing) / cols) if cols > 0 else 1
        cw = (W - 40) // cols if cols > 0 else W - 40
        ch = (H - 60) // rows

        for idx, area in enumerate(housing):
            col = idx % cols
            row = idx // cols
            cx = 20 + col * cw
            cy = 45 + row * ch
            active = area["status"] and self.gardus[area["gardu_id"]]["status"]
            bg = C["bg_card"] if active else "#1a0a0a"
            border = C["accent_green"] if active else C["accent_red"]
            self.canvas.create_rectangle(cx + 3, cy + 3, cx + cw - 3, cy + ch - 3,
                                         fill=bg, outline=border, width=2)
            self.canvas.create_text(cx + cw // 2, cy + 14,
                                    text=f"{area['icon']} {area['name']}",
                                    font=("Segoe UI", 8, "bold"), fill=C["text_primary"])
            st = "🟢 NYALA" if active else "🔴 PADAM"
            self.canvas.create_text(cx + cw // 2, cy + 28, text=st,
                                    font=("Segoe UI", 7, "bold"),
                                    fill=C["accent_green"] if active else C["accent_red"])
            ah = [h for h in self.houses if h["area_id"] == area["id"]]
            if not ah:
                continue
            blocks = defaultdict(list)
            for h in ah:
                blocks[h["block"]].append(h)
            bkeys = sorted(blocks.keys())
            bcols = min(3, len(bkeys))
            brows = math.ceil(len(bkeys) / bcols) if bcols > 0 else 1
            ix = cx + 8
            iy2 = cy + 38
            iw = cw - 16
            ih = ch - 50
            rh = 6
            for br in range(brows + 1):
                ry = iy2 + br * (ih // max(brows, 1))
                self.canvas.create_rectangle(ix, ry - rh // 2, ix + iw, ry + rh // 2,
                                             fill=C["road"], outline="")
                for dx in range(0, iw, 12):
                    self.canvas.create_line(ix + dx, ry, ix + dx + 6, ry,
                                            fill=C["road_line"], width=1)
            for bi, bn in enumerate(bkeys):
                bc = bi % bcols
                br2 = bi // bcols
                bx = ix + bc * (iw // bcols) + 4
                by = iy2 + br2 * (ih // brows) + rh
                bh = blocks[bn]
                hc2 = min(5, len(bh))
                hr2 = math.ceil(len(bh) / hc2)
                hw = min(12, (iw // bcols - 8) // hc2)
                hh = min(10, (ih // brows - rh - 4) // hr2)
                for hi, house in enumerate(bh):
                    hcol = hi % hc2
                    hrow = hi // hc2
                    hx = bx + hcol * (hw + 2)
                    hy = by + hrow * (hh + 2)
                    if active and house["status"]:
                        hfill = C["house_active"]
                    elif house["has_generator"] and not active:
                        hfill = C["accent_yellow"]
                    elif house["has_solar"] and not active:
                        hfill = C["accent_cyan"]
                    else:
                        hfill = C["house_dead"]
                    self.canvas.create_rectangle(hx, hy + 2, hx + hw, hy + hh,
                                                 fill=hfill, outline="#333")
                    self.canvas.create_polygon(hx - 1, hy + 2, hx + hw // 2, hy - 2,
                                               hx + hw + 1, hy + 2,
                                               fill="#555" if active else "#2a1a1a", outline="")
            pop = sum(h["family_size"] for h in ah)
            gs = sum(1 for h in ah if h["has_generator"])
            sl = sum(1 for h in ah if h["has_solar"])
            md = sum(1 for h in ah if h["has_medical_equipment"])
            st2 = f"🏠{len(ah)} 👥{pop} ⚡{gs} ☀️{sl}"
            if md > 0:
                st2 += f" 🏥{md}"
            self.canvas.create_text(cx + cw // 2, cy + ch - 10, text=st2,
                                    font=("Segoe UI", 6), fill=C["text_muted"])

    def _draw_cyber(self, W, H):
        self.canvas.create_text(W // 2, 20,
                                text="💀 PETA SERANGAN SIBER - Infrastruktur Grid Listrik",
                                font=("Segoe UI", 12, "bold"), fill=C["cyber_red"])
        # INTERNET
        self.canvas.create_oval(W // 2 - 60, 50, W // 2 + 60, 100,
                                fill="#1a1a3e", outline=C["cyber_blue"], width=2)
        self.canvas.create_text(W // 2, 75, text="☁️ INTERNET",
                                font=("Segoe UI", 9, "bold"), fill=C["cyber_blue"])
        # FIREWALL
        fy = 130
        self.canvas.create_rectangle(W // 2 - 80, fy - 15, W // 2 + 80, fy + 15,
                                     fill="#1a2a1a", outline=C["cyber_green"], width=2)
        self.canvas.create_text(W // 2, fy, text="🛡️ FIREWALL",
                                font=("Segoe UI", 8, "bold"), fill=C["cyber_green"])
        self.canvas.create_line(W // 2, 100, W // 2, fy - 15,
                                fill=C["cyber_blue"], width=2, dash=(4, 4))
        # DMZ
        dy = 180
        self.canvas.create_rectangle(W // 2 - 120, dy - 12, W // 2 + 120, dy + 12,
                                     fill="#1a1a2e", outline=C["cyber_purple"], width=1)
        self.canvas.create_text(W // 2, dy, text="📡 DMZ - HMI Web Interface",
                                font=("Segoe UI", 7), fill=C["cyber_purple"])
        # SCADA
        sy = 240
        self.canvas.create_rectangle(50, sy - 15, W - 50, sy + 15,
                                     fill="#1a2a2e", outline=C["accent_cyan"], width=2)
        self.canvas.create_text(W // 2, sy, text="🖥️ SCADA / HMI System",
                                font=("Segoe UI", 9, "bold"), fill=C["accent_cyan"])
        # GARDU
        gx_positions = []
        n = len(self.gardus)
        for i, g in enumerate(self.gardus):
            gx = 80 + i * ((W - 160) // max(n - 1, 1))
            gy = 310
            gx_positions.append((gx, gy))
            active = g["status"]
            comp = g.get("compromised", False)
            gc = C["cyber_red"] if comp else (C["gardu_active"] if active else C["gardu_dead"])
            self.canvas.create_line(W // 2, sy + 15, gx, gy - 20,
                                    fill=C["text_muted"], width=1, dash=(3, 3))
            self.canvas.create_rectangle(gx - 35, gy - 20, gx + 35, gy + 20,
                                         fill=C["bg_card"], outline=gc, width=2)
            icon = "💀" if comp else ("⚡" if active else "☠️")
            self.canvas.create_text(gx, gy - 5, text=icon, font=("Segoe UI", 12))
            self.canvas.create_text(gx, gy + 8, text=g["name"],
                                    font=("Segoe UI", 6, "bold"), fill=gc)
            vuln_txt = f"{len(g['vulnerabilities'])} vuln"
            self.canvas.create_text(gx, gy + 30, text=vuln_txt,
                                    font=("Segoe UI", 6), fill=C["accent_red"] if len(g["vulnerabilities"]) >= 3 else C["text_muted"])
            # OS tag
            self.canvas.create_text(gx, gy + 42, text=g["os"][:15],
                                    font=("Segoe UI", 5), fill=C["text_muted"])

        # Attack vectors
        if self.active_attacks:
            for atk in self.active_attacks:
                self.canvas.create_text(W // 2, H - 40,
                                        text=f"⚠️ SERANGAN AKTIF: {atk.get('type', '?')} → {atk.get('target', '?')}",
                                        font=("Segoe UI", 10, "bold"), fill=C["cyber_red"])

        # Defense level indicator
        dl = self.cyber_defense_level
        dc = C["cyber_green"] if dl >= 70 else C["cyber_yellow"] if dl >= 40 else C["cyber_red"]
        self.canvas.create_text(W - 80, H - 30, text=f"🛡️ Defense: {dl}%",
                                font=("Segoe UI", 9, "bold"), fill=dc)

    def _draw_impact(self, W, H):
        self.canvas.create_text(W // 2, 20, text="📊 ANALISIS DAMPAK BLACKOUT",
                                font=("Segoe UI", 12, "bold"), fill=C["accent_cyan"])
        tpop = sum(a.get("population", 0) for a in self.areas if not (a["status"] and self.gardus[a["gardu_id"]]["status"]))
        tload = sum(a["load"] for a in self.areas if not (a["status"] and self.gardus[a["gardu_id"]]["status"]))
        hrs = sum(1 for a in self.areas if a["priority"] == 1 and not (a["status"] and self.gardus[a["gardu_id"]]["status"]))
        eco_loss = tload * 2.5
        cards = [
            ("💰 EKONOMI", C["accent_yellow"], [
                f"Beban padam: {tload} MW",
                f"Kerugian est: Rp {eco_loss:.0f}M/jam",
                f"Industri terdampak: {sum(1 for a in self.areas if a['type'] == 'area' and not a['status'])}",
                f"Pasar offline: {'YA' if any(a['name']=='Pasar Swalayan' and not a['status'] for a in self.areas) else 'TIDAK'}",
            ]),
            ("👥 SOSIAL", C["accent_blue"], [
                f"Jiwa terdampak: {tpop:,}",
                f"Risiko kejahatan: {'TINGGI' if tpop > 1000 else 'SEDANG' if tpop > 0 else 'RENDAH'}",
                f"Komunikasi: {'GANGGUAN' if tload > 50 else 'NORMAL'}",
                f"Uptime Score: {self.uptime_score:.1f}%",
            ]),
            ("🏥 KESEHATAN", C["accent_red"], [
                f"RS terdampak: {hrs}",
                f"Pasien ICU berisiko: {hrs * 25} orang",
                f"Vaksin terancam: {'YA' if hrs > 0 else 'TIDAK'}",
                f"Ambulans: {'OFFLINE' if hrs > 0 else 'NORMAL'}",
            ]),
            ("🏗️ INFRASTRUKTUR", C["accent_purple"], [
                f"Beban hilang: {tload} MW",
                f"Gardu mati: {sum(1 for g in self.gardus if not g['status'])}/{len(self.gardus)}",
                f"Air: {'MATI' if tload > 80 else 'RISIKO' if tload > 30 else 'NORMAL'}",
                f"Telekomunikasi: {'GANGGUAN' if tload > 60 else 'NORMAL'}",
            ]),
        ]
        cw2 = (W - 50) // 2
        ch2 = (H - 80) // 2
        for idx, (title, color, items) in enumerate(cards):
            col = idx % 2
            row = idx // 2
            cx = 15 + col * (cw2 + 20)
            cy = 45 + row * (ch2 + 10)
            self.canvas.create_rectangle(cx, cy, cx + cw2, cy + ch2,
                                         fill=C["bg_card"], outline=color, width=2)
            self.canvas.create_text(cx + cw2 // 2, cy + 15, text=title,
                                    font=("Segoe UI", 10, "bold"), fill=color)
            for i, item in enumerate(items):
                self.canvas.create_text(cx + 15, cy + 38 + i * 22, text=item,
                                        font=("Segoe UI", 8), fill=C["text_primary"], anchor=tk.W)
        sev = 0
        if tpop > 0:
            sev += 25
        if tpop > 500:
            sev += 25
        if hrs > 0:
            sev += 25
        if sum(1 for g in self.gardus if not g["status"]) > 1:
            sev += 25
        sc = [C["accent_green"], C["accent_yellow"], C["accent_orange"], C["accent_red"]]
        sl2 = ["NORMAL", "WASPADA", "BAHAYA", "KRITIS"]
        si = min(sev // 25, 3)
        self.canvas.create_text(W // 2, H - 25,
                                text=f"⚠️ LEVEL KEADAAN: {sl2[si]} ({sev}%)",
                                font=("Segoe UI", 11, "bold"), fill=sc[si])

    # ============================================================
    # UPDATE
    # ============================================================
    def _update_all(self):
        ta = len(self.areas)
        ny = sum(1 for a in self.areas if a["status"] and self.gardus[a["gardu_id"]]["status"])
        ga = sum(1 for g in self.gardus if g["status"])
        tl = sum(g["load"] for g in self.gardus if g["status"])
        tc = sum(g["capacity"] for g in self.gardus if g["status"])

        self.lbl_stats_areas.config(text=f"💡 Area Nyala: {ny}/{ta}")
        self.lbl_stats_gardu.config(text=f"🏭 Gardu Aktif: {ga}/{len(self.gardus)}")
        self.lbl_stats_load.config(text=f"⚡ Beban: {tl} MW")

        if ga == len(self.gardus) and ny == ta:
            self.lbl_top_status.config(text="🟢 SISTEM NORMAL", fg=C["accent_green"])
            self.lbl_status.config(text="✅ SEMUA AMAN", fg=C["accent_green"])
        elif ga == 0:
            self.lbl_top_status.config(text="🔴 TOTAL BLACKOUT!", fg=C["accent_red"])
            self.lbl_status.config(text="💀 TOTAL BLACKOUT!", fg=C["accent_red"])
        else:
            p = ta - ny
            self.lbl_top_status.config(text=f"🟡 {p} AREA PADAM", fg=C["accent_yellow"])
            self.lbl_status.config(text=f"⚠️ {p} area terdampak", fg=C["accent_yellow"])

        # Load bar
        self.load_canvas.delete("all")
        w = self.load_canvas.winfo_width() or 250
        pct = (tl / tc * 100) if tc > 0 else 0
        fw = min(w, pct / 100 * w)
        fc = C["accent_green"] if pct < 70 else C["accent_yellow"] if pct < 100 else C["accent_red"]
        if fw > 0:
            self.load_canvas.create_rectangle(0, 0, fw, 20, fill=fc, outline="")
        self.load_canvas.create_text(w // 2, 10, text=f"{tl}/{tc} MW ({pct:.0f}%)",
                                     font=("Consolas", 7, "bold"), fill="white")

        # Gardu widgets
        for i, gw in enumerate(self.gardu_widgets):
            if i < len(self.gardus):
                g = self.gardus[i]
                gw["frame"].pack(fill=tk.X, pady=1)
                si = "💀" if g.get("compromised") else "🟢" if g["status"] else "🔴"
                gw["name"].config(text=f"{si} {g['name']}")
                lp = (g["load"] / g["capacity"] * 100) if g["capacity"] > 0 else 0
                if g["status"]:
                    gw["detail"].config(
                        text=f"{g['load']}/{g['capacity']}MW ({lp:.0f}%) | {g['protocol']}",
                        fg=C["accent_green"] if lp < 70 else C["accent_yellow"])
                else:
                    gw["detail"].config(
                        text=f"☠️ MATI | Trip:{g['trip_count']}x | Vuln:{len(g['vulnerabilities'])}",
                        fg=C["accent_red"])
                bar = gw["bar"]
                bar.delete("all")
                bw = bar.winfo_width() or 250
                bfw = min(bw, lp / 100 * bw) if g["status"] else 0
                bc = C["accent_green"] if lp < 70 else C["accent_yellow"] if lp < 100 else C["accent_red"]
                if bfw > 0:
                    bar.create_rectangle(0, 0, bfw, 6, fill=bc, outline="")
            else:
                gw["frame"].pack_forget()

        self.lbl_stat_blackouts.config(text=f"⚡ Blackout: {self.total_blackouts}")
        self.lbl_stat_cascades.config(text=f"🔥 Cascade: {self.cascade_count}")
        self.lbl_stat_cyber.config(text=f"💀 Serangan Siber: {self.cyber_attacks_count}")
        self.lbl_stat_restorations.config(text=f"🔧 Pemulihan: {self.total_restorations}")

        if self.active_attacks:
            self.lbl_cyber_threat.config(text=f"🔴 SERANGAN: {len(self.active_attacks)}",
                                         fg=C["accent_red"])
            self.lbl_active_attacks.config(
                text=f"Target: {' '.join(a.get('target', '?') for a in self.active_attacks)}")
        else:
            comp = sum(1 for g in self.gardus if g.get("compromised"))
            self.lbl_cyber_threat.config(
                text="🟡 TERKOMPROMI" if comp else "🔒 Ancaman: RENDAH",
                fg=C["accent_yellow"] if comp else C["accent_green"])
            self.lbl_active_attacks.config(text="Serangan aktif: 0")

        # Uptime score calculation
        ny_ratio = ny / ta if ta > 0 else 1.0
        if ny_ratio < 1.0:
            self.uptime_score = max(0.0, self.uptime_score - (1.0 - ny_ratio) * 0.05)
        else:
            self.uptime_score = min(100.0, self.uptime_score + 0.01)
        score_color = C["accent_green"] if self.uptime_score >= 80 else C["accent_yellow"] if self.uptime_score >= 50 else C["accent_red"]
        self.lbl_uptime.config(text=f"📈 Uptime Score: {self.uptime_score:.1f}%", fg=score_color)

        # Simulation time
        h = self.simulation_time // 3600
        m = (self.simulation_time % 3600) // 60
        s = self.simulation_time % 60
        self.lbl_top_time.config(text=f"⏱ {h:02d}:{m:02d}:{s:02d}")

        # Real-time wall clock
        now_str = datetime.now().strftime("%H:%M:%S")
        self.lbl_realtime_clock.config(text=f"🕐 {now_str}")

        # Status bar updates
        session_elapsed = datetime.now() - self.session_start
        self.lbl_sb_session.config(text=f"Sesi: {str(session_elapsed).split('.')[0]}")
        self.lbl_sb_speed.config(text=f"Speed: {self.simulation_speed}x")
        self.lbl_sb_weather.config(text=f"{'☀️' if self.weather == 'cerah' else '🌧️' if self.weather == 'hujan' else '⛈️'} {self.weather.capitalize()}")
        self.lbl_sb_score.config(text=f"Uptime: {self.uptime_score:.1f}%", fg=score_color)
        self.lbl_sb_realtime.config(text=f"🕐 {now_str}")

        # Update load history chart
        self.load_history[self.load_history_idx] = pct
        self.load_history_idx = (self.load_history_idx + 1) % 60
        self._draw_load_chart()

        # Progress active state
        self.progress_active = self.running or self.restoring

    # ============================================================
    # LOGGING
    # ============================================================
    def _add_log(self, msg, tag="info"):
        ts = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{ts}] ", "timestamp")
        self.log_text.insert(tk.END, f"{msg}\n", tag)
        self.log_text.see(tk.END)

    def _clear_log(self):
        self.log_text.delete("1.0", tk.END)
        self._add_log("🗑️ Log dihapus.", "info")

    # ============================================================
    # REALTIME LOAD CHART
    # ============================================================
    def _draw_load_chart(self):
        """Draw a compact sparkline of load% history."""
        c = self.chart_canvas
        c.delete("all")
        w = c.winfo_width() or 250
        h = c.winfo_height() or 40

        # Background grid lines
        for pct_line in (25, 50, 75, 100):
            y = h - int(pct_line / 100 * h)
            c.create_line(0, y, w, y, fill=C["grid_line"], dash=(2, 4))

        # Build ordered history (oldest → newest)
        ordered = self.load_history[self.load_history_idx:] + self.load_history[:self.load_history_idx]

        n = len(ordered)
        if n < 2:
            return

        step = w / (n - 1)
        pts = []
        for i, val in enumerate(ordered):
            x = int(i * step)
            y = h - int(min(val, 100) / 100 * h) - 1
            pts.append((x, y))

        # Filled area under curve
        poly_pts = [0, h]
        for x, y in pts:
            poly_pts += [x, y]
        poly_pts += [w, h]
        c.create_polygon(poly_pts, fill="#0d3d2a", outline="")

        # Line
        for i in range(len(pts) - 1):
            x1, y1 = pts[i]
            x2, y2 = pts[i + 1]
            val = ordered[i + 1]
            col = C["accent_green"] if val < 70 else C["accent_yellow"] if val < 100 else C["accent_red"]
            c.create_line(x1, y1, x2, y2, fill=col, width=1)

        # Latest value label
        last_val = ordered[-1]
        col = C["accent_green"] if last_val < 70 else C["accent_yellow"] if last_val < 100 else C["accent_red"]
        c.create_text(w - 3, 3, text=f"{last_val:.0f}%", font=("Consolas", 6, "bold"),
                      fill=col, anchor=tk.NE)

    # ============================================================
    # CREDITS
    # ============================================================
    def _show_credits(self):
        """Show credits window."""
        cw = tk.Toplevel(self.root)
        cw.title("© Credits")
        cw.geometry("480x380")
        cw.resizable(False, False)
        cw.configure(bg=C["bg_dark"])
        cw.grab_set()

        # Outer glow border
        border = tk.Frame(cw, bg=C["accent_purple"], padx=2, pady=2)
        border.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        inner = tk.Frame(border, bg=C["bg_panel"], padx=20, pady=20)
        inner.pack(fill=tk.BOTH, expand=True)

        # Logo / title
        tk.Label(inner, text="⚡", font=("Segoe UI", 36), fg=C["accent_cyan"],
                 bg=C["bg_panel"]).pack(pady=(5, 0))
        tk.Label(inner, text=f"Simulasi Blackout Area",
                 font=("Segoe UI", 16, "bold"), fg=C["accent_cyan"], bg=C["bg_panel"]).pack()
        tk.Label(inner, text=f"v{VERSION}",
                 font=("Segoe UI", 10), fg=C["text_secondary"], bg=C["bg_panel"]).pack()

        tk.Frame(inner, bg=C["accent_purple"], height=1).pack(fill=tk.X, pady=12)

        # Creator row
        cf2 = tk.Frame(inner, bg=C["bg_card"], padx=15, pady=10)
        cf2.pack(fill=tk.X)
        tk.Label(cf2, text="👤 Creator", font=("Segoe UI", 8),
                 fg=C["text_muted"], bg=C["bg_card"]).pack(anchor=tk.W)
        tk.Label(cf2, text=CREATOR,
                 font=("Segoe UI", 14, "bold"), fg=C["cyber_yellow"], bg=C["bg_card"]).pack(anchor=tk.W)

        tk.Frame(inner, bg=C["bg_medium"], height=1).pack(fill=tk.X, pady=8)

        # Organization row
        of = tk.Frame(inner, bg=C["bg_card"], padx=15, pady=10)
        of.pack(fill=tk.X)
        tk.Label(of, text="🏢 Organization", font=("Segoe UI", 8),
                 fg=C["text_muted"], bg=C["bg_card"]).pack(anchor=tk.W)
        tk.Label(of, text=ORG,
                 font=("Segoe UI", 14, "bold"), fg=C["accent_purple"], bg=C["bg_card"]).pack(anchor=tk.W)

        tk.Frame(inner, bg=C["bg_medium"], height=1).pack(fill=tk.X, pady=8)

        # Tech stack
        tk.Label(inner, text="🛠️  Python 3 · Tkinter · Simulasi Edukasi Keamanan Siber",
                 font=("Segoe UI", 8), fg=C["text_muted"], bg=C["bg_panel"]).pack()

        tk.Frame(inner, bg=C["bg_medium"], height=1).pack(fill=tk.X, pady=8)

        # Disclaimer
        tk.Label(inner,
                 text="⚠️  Ini adalah simulasi edukasi semata.\nTidak untuk tujuan ilegal.",
                 font=("Segoe UI", 8), fg=C["accent_red"], bg=C["bg_panel"],
                 justify=tk.CENTER).pack()

        tk.Button(inner, text="✅  Tutup  [F11]", command=cw.destroy,
                  bg=C["accent_purple"], fg="white", font=("Segoe UI", 10, "bold"),
                  cursor="hand2", relief=tk.FLAT, padx=20, pady=6).pack(pady=(12, 0))

    def _export_log(self):
        fp = filedialog.asksaveasfilename(defaultextension=".txt",
                                          filetypes=[("Text", "*.txt"), ("All", "*.*")],
                                          title="Export Log")
        if fp:
            with open(fp, "w", encoding="utf-8") as f:
                f.write(f"Log Simulasi Blackout v{VERSION}\nExport: {datetime.now()}\n{'=' * 50}\n\n")
                f.write(self.log_text.get("1.0", tk.END))
            self._add_log("💾 Log diekspor.", "success")
            self._notify("💾 Log berhasil diekspor!", color=C["accent_green"])

    # ============================================================
    # AUTO BLACKOUT
    # ============================================================
    def _auto_blackout(self):
        if self.running or self.restoring or self.paused:
            return
        aktif = [g for g in self.gardus if g["status"]]
        if not aktif:
            messagebox.showinfo("Info", "Semua gardu sudah padam!")
            return
        self.running = True
        self.btn_auto.config(state=tk.DISABLED, text="⏳ BERLANGSUNG...", bg=C["bg_medium"])
        target = random.choice(aktif)
        reasons = {
            "cerah": [f"🔧 Gangguan mekanis {target['name']}", f"💥 Kabel {target['name']} putus",
                      f"🔥 Trafo {target['name']} terbakar"],
            "hujan": [f"🌧️ Hubungan pendek {target['name']}", f"💧 Banjir {target['name']}",
                      f"⚡ Petir {target['name']}"],
            "badai": [f"⛈️ Badai rusak {target['name']}", f"🌪️ Tiang roboh {target['name']}",
                      f"⚡ Sambaran {target['name']}"],
        }
        reason = random.choice(reasons.get(self.weather, reasons["cerah"]))
        self._add_log(reason, "danger")
        self._add_log(f"⚠️ {target['name']} gagal!", "warning")
        self.total_blackouts += 1
        self.lbl_status.config(text=f"⚠️ BLACKOUT: {target['name']}!", fg=C["accent_red"])

        # Save undo state
        self.undo_stack.append({"type": "blackout", "gardu_id": target["id"], "reason": reason})
        if len(self.undo_stack) > 20:
            self.undo_stack.pop(0)

        # Add timeline event
        self._add_timeline_event("blackout", f"{reason} → {target['name']} trip", "danger")
        self._notify(f"⚡ BLACKOUT: {target['name']}!", color=C["accent_red"], duration=3000)
        self.root.after(600, lambda: self._cascade(target))

    def _cascade(self, fg):
        fg["status"] = False
        fg["trip_count"] += 1
        fg["scada_online"] = False
        self._draw_all()
        self._update_all()
        self.root.update()
        self._add_log(f"☠️ {fg['name']} TRIP! OS:{fg['os']} Proto:{fg['protocol']}", "critical")

        affected = sorted([a for a in self.areas if a["gardu_id"] == fg["id"]],
                          key=lambda a: a["priority"], reverse=True)
        for area in affected:
            area["status"] = False
            for h in self.houses:
                if (h["area_id"] == area["id"] and not h["has_generator"] and not h["has_solar"]):
                    h["status"] = False
            pl = {1: "KRITIS", 2: "PENTING", 3: "NORMAL"}[area["priority"]]
            pop = area.get("population", 0)
            self._add_log(f"🌑 {area['icon']} {area['name']} [{pl}] - {pop} jiwa", "danger")
            self._draw_all()
            self._update_all()
            self.root.update()
            time.sleep(0.1 / self.simulation_speed)

        cascade = False
        for g in self.gardus:
            if g["id"] != fg["id"] and g["status"]:
                g["load"] = sum(a["load"] for a in self.areas if a["gardu_id"] == g["id"] and a["status"])
                pct = (g["load"] / g["capacity"]) * 100 if g["capacity"] > 0 else 0
                if pct > 100:
                    self._add_log(f"🔥 {g['name']} OVERLOAD! {g['load']}/{g['capacity']}MW ({pct:.0f}%)", "warning")
                    if pct > 130:
                        self.cascade_count += 1
                        self._add_log(f"💥 CASCADE! {g['name']} ikut trip!", "critical")
                        cascade = True
                        self._add_timeline_event("blackout", f"CASCADE: {g['name']} trip!", "critical")
                        self.root.after(800, lambda g2=g: self._cascade(g2))

        self._draw_all()
        self._update_all()
        tp = sum(1 for a in self.areas if not a["status"])
        tg = sum(1 for g in self.gardus if not g["status"])
        tpop = sum(a.get("population", 0) for a in self.areas if not a["status"])
        self._add_log(f"📊 {tg} gardu mati, {tp} area padam, {tpop} jiwa terdampak", "warning")

        if not cascade:
            self._add_log("─" * 40, "separator")
            self.running = False
            self.btn_auto.config(state=tk.NORMAL, text="⚡ BLACKOUT OTOMATIS  [F2]", bg=C["accent_red"])
            self.btn_cyber.config(state=tk.NORMAL, text="💀 SERANGAN SIBER  [F3]", bg=C["cyber_red"])
            if tg > 0:
                self._notify(f"⚡ {tg} gardu mati, {tpop:,} jiwa terdampak!", color=C["accent_red"], duration=4000)

    # ============================================================
    # CYBER ATTACK
    # ============================================================
    def _launch_cyber_attack(self):
        if self.running or self.restoring or self.paused:
            return
        aktif = [g for g in self.gardus if g["status"]]
        if not aktif:
            messagebox.showinfo("Info", "Semua gardu sudah padam!")
            return

        aw = tk.Toplevel(self.root)
        aw.title("💀 Pilih Serangan Siber")
        aw.geometry("700x560")
        aw.configure(bg=C["bg_dark"])

        tk.Label(aw, text="💀 PILIH TEKNIK SERANGAN SIBER",
                 font=("Segoe UI", 14, "bold"), fg=C["cyber_red"], bg=C["bg_dark"]).pack(pady=8)
        tk.Label(aw, text="⚠️ Ini hanya simulasi edukasi! Serangan siber ke infrastruktur listrik adalah KEJAHATAN.",
                 font=("Segoe UI", 9, "bold"), fg=C["accent_yellow"], bg=C["bg_dark"]).pack(pady=3)

        ct = tk.Frame(aw, bg=C["bg_dark"])
        ct.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        cs = tk.Canvas(ct, bg=C["bg_dark"], highlightthickness=0)
        sb_scroll = tk.Scrollbar(ct, orient=tk.VERTICAL, command=cs.yview)
        sf = tk.Frame(cs, bg=C["bg_dark"])
        sf.bind("<Configure>", lambda e: cs.configure(scrollregion=cs.bbox("all")))
        cs.create_window((0, 0), window=sf, anchor=tk.NW, width=660)
        cs.configure(yscrollcommand=sb_scroll.set)
        sb_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        cs.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        for ak, ad in CYBER_ATTACKS.items():
            fr = tk.Frame(sf, bg=C["bg_card"],
                          highlightbackground=C["cyber_red"] if ad["severity"] >= 5 else C["cyber_yellow"],
                          highlightthickness=2)
            fr.pack(fill=tk.X, pady=3, padx=5)
            tk.Label(fr, text=f"{ad['name']}  {'⭐' * ad['severity']}",
                     font=("Segoe UI", 10, "bold"),
                     fg=C["cyber_red"] if ad["severity"] >= 5 else C["cyber_yellow"],
                     bg=C["bg_card"]).pack(anchor=tk.W, padx=8, pady=(5, 0))
            tk.Label(fr, text=ad["short"], font=("Segoe UI", 8),
                     fg=C["text_secondary"], bg=C["bg_card"]).pack(anchor=tk.W, padx=8)
            tk.Label(fr, text=f"💰 {ad['impact_economy']}  |  🏥 {ad['impact_health']}",
                     font=("Segoe UI", 7), fg=C["accent_yellow"], bg=C["bg_card"]).pack(anchor=tk.W, padx=8, pady=(2, 0))

            def launch(key=ak, win=aw):
                win.destroy()
                self._exec_cyber(key)

            tk.Button(fr, text="💀 LANCARKAN", command=launch,
                      bg=C["cyber_red"], fg="white", font=("Segoe UI", 8, "bold"),
                      cursor="hand2", relief=tk.FLAT, padx=10, pady=3).pack(anchor=tk.E, padx=8, pady=5)

        tk.Button(aw, text="❌ Batal", command=aw.destroy,
                  bg=C["bg_card"], fg=C["text_primary"], font=("Segoe UI", 10, "bold"),
                  cursor="hand2", relief=tk.FLAT, padx=20, pady=5).pack(pady=8)

    def _exec_cyber(self, atk_type):
        ad = CYBER_ATTACKS.get(atk_type)
        if not ad:
            return
        self.running = True
        self.btn_auto.config(state=tk.DISABLED)
        self.btn_cyber.config(state=tk.DISABLED, text="⏳ MENYERANG...", bg=C["bg_medium"])
        self.cyber_attacks_count += 1

        vuln_g = [g for g in self.gardus if g["status"] and len(g["vulnerabilities"]) >= 2]
        if not vuln_g:
            vuln_g = [g for g in self.gardus if g["status"]]
        if not vuln_g:
            self.running = False
            self.btn_auto.config(state=tk.NORMAL, text="⚡ BLACKOUT OTOMATIS  [F2]", bg=C["accent_red"])
            self.btn_cyber.config(state=tk.NORMAL, text="💀 SERANGAN SIBER  [F3]", bg=C["cyber_red"])
            return

        target = random.choice(vuln_g)

        # Defense check
        if random.random() < (self.cyber_defense_level / 100) * 0.6:
            self._add_log("🛡️ PERTAHANAN BERHASIL MENCEGAH SERANGAN!", "defense")
            self._add_log(f"🛡️ {ad['name']} diblokir sebelum mencapai {target['name']}", "defense")
            self._add_log(f"📋 Defense level {self.cyber_defense_level}% berhasil mendeteksi", "defense")
            self._add_log("─" * 40, "separator")
            self.running = False
            self.btn_auto.config(state=tk.NORMAL, text="⚡ BLACKOUT OTOMATIS  [F2]", bg=C["accent_red"])
            self.btn_cyber.config(state=tk.NORMAL, text="💀 SERANGAN SIBER  [F3]", bg=C["cyber_red"])
            self._notify("🛡️ Serangan DIBLOKIR oleh pertahanan!", color=C["cyber_green"], duration=3000)
            return

        self.active_attacks.append({"type": atk_type, "target": target["name"], "start": self.simulation_time})
        self._add_log("═" * 40, "cyber")
        self._add_log("💀 SERANGAN SIBER TERDETEKSI!", "cyber")
        self._add_log(f"🔴 Tipe: {ad['name']}", "cyber")
        self._add_log(f"🎯 Target: {target['name']}", "cyber")
        self._add_log(f"🖥️ OS: {target['os']}  Protocol: {target['protocol']}", "cyber_warn")
        self._add_log(f"⚠️ Kerentanan: {len(target['vulnerabilities'])} ditemukan", "cyber_warn")
        self._add_log("📋 TEKNIK SERANGAN:", "cyber_info")
        for line in ad["technique"].split("\n"):
            self._add_log(f"  {line}", "cyber_info")

        target["compromised"] = True
        target["scada_online"] = False
        self._add_log(f"💀 {target['name']} TELAH DIKOMPROMI!", "critical")
        self._add_log("📊 DAMPAK:", "cyber_warn")
        self._add_log(f"  💰 {ad['impact_economy']}", "cyber_warn")
        self._add_log(f"  👥 {ad['impact_social']}", "cyber_warn")
        self._add_log(f"  🏥 {ad['impact_health']}", "cyber_warn")
        self._add_log(f"⚡ Hacker mematikan {target['name']} secara remote!", "critical")

        self._add_timeline_event("cyber", f"{ad['name']} → {target['name']} DIKOMPROMI", "critical")
        self._notify(f"💀 SERANGAN SIBER! {target['name']} dikuasai hacker!", color=C["cyber_red"], duration=4000)

        self.total_blackouts += 1
        self.root.after(800, lambda: self._cascade(target))
        self.root.after(2000, lambda: self._show_attack_detail(atk_type))

    def _show_attack_detail(self, atk_type):
        ad = CYBER_ATTACKS.get(atk_type)
        if not ad:
            return
        self.running = False
        self.btn_auto.config(state=tk.NORMAL, text="⚡ BLACKOUT OTOMATIS  [F2]", bg=C["accent_red"])
        self.btn_cyber.config(state=tk.NORMAL, text="💀 SERANGAN SIBER  [F3]", bg=C["cyber_red"])
        self.active_attacks = [a for a in self.active_attacks if a["type"] != atk_type]
        dw = tk.Toplevel(self.root)
        dw.title(f"📖 Detail: {ad['name']}")
        dw.geometry("650x650")
        dw.configure(bg=C["bg_dark"])
        tk.Label(dw, text=f"📖 PENJELASAN DETAIL: {ad['name']}",
                 font=("Segoe UI", 13, "bold"), fg=C["cyber_red"], bg=C["bg_dark"]).pack(pady=10)
        tw = tk.Text(dw, bg=C["bg_card"], fg=C["text_primary"], font=("Segoe UI", 10),
                     wrap=tk.WORD, relief=tk.FLAT, padx=15, pady=15)
        tw.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        tw.insert(tk.END, ad["layman"])
        tw.config(state=tk.DISABLED)
        tk.Button(dw, text="✅ Mengerti", command=dw.destroy,
                  bg=C["accent_blue"], fg="white", font=("Segoe UI", 11, "bold"),
                  cursor="hand2", relief=tk.FLAT, padx=20, pady=8).pack(pady=10)
        self._add_log("📖 Baca detail serangan di jendela terbuka.", "cyber_info")
        self._add_log("🛡️ Tingkatkan Pertahanan Siber untuk mencegah!", "defense")
        self._add_log("─" * 40, "separator")

    # ============================================================
    # SCAN KERENTANAN
    # ============================================================
    def _scan_vulnerabilities(self):
        if self.running or self.restoring:
            return
        self._add_log("🔍 Memindai kerentanan...", "cyber_info")
        vw = tk.Toplevel(self.root)
        vw.title("🔍 Hasil Scan Kerentanan")
        vw.geometry("700x550")
        vw.configure(bg=C["bg_dark"])
        tk.Label(vw, text="🔍 HASIL SCAN KERENTANAN INFRASTRUKTUR",
                 font=("Segoe UI", 13, "bold"), fg=C["cyber_yellow"], bg=C["bg_dark"]).pack(pady=10)
        ct = tk.Frame(vw, bg=C["bg_dark"])
        ct.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        cs = tk.Canvas(ct, bg=C["bg_dark"], highlightthickness=0)
        sb_scroll = tk.Scrollbar(ct, orient=tk.VERTICAL, command=cs.yview)
        sf = tk.Frame(cs, bg=C["bg_dark"])
        sf.bind("<Configure>", lambda e: cs.configure(scrollregion=cs.bbox("all")))
        cs.create_window((0, 0), window=sf, anchor=tk.NW, width=660)
        cs.configure(yscrollcommand=sb_scroll.set)
        sb_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        cs.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        tv = 0
        for g in self.gardus:
            fr = tk.Frame(sf, bg=C["bg_card"],
                          highlightbackground=C["accent_red"] if len(g["vulnerabilities"]) >= 3
                          else C["accent_yellow"] if g["vulnerabilities"] else C["accent_green"],
                          highlightthickness=2)
            fr.pack(fill=tk.X, pady=4, padx=5)
            si = "🟢" if g["status"] else "🔴"
            tk.Label(fr, text=f"{si} {g['name']} ({g['os']})",
                     font=("Segoe UI", 10, "bold"), fg=C["text_primary"], bg=C["bg_card"]).pack(anchor=tk.W, padx=8, pady=(5, 0))
            tk.Label(fr, text=f"Protocol: {g['protocol']} | Firewall: {'✅' if g['firewall'] else '❌'} | IDS: {'✅' if g['ids'] else '❌'}",
                     font=("Segoe UI", 8), fg=C["text_secondary"], bg=C["bg_card"]).pack(anchor=tk.W, padx=8)
            if g["vulnerabilities"]:
                tk.Label(fr, text=f"⚠️ {len(g['vulnerabilities'])} Kerentanan:",
                         font=("Segoe UI", 9, "bold"), fg=C["accent_red"], bg=C["bg_card"]).pack(anchor=tk.W, padx=8, pady=(3, 0))
                for vk in g["vulnerabilities"]:
                    v = VULNS.get(vk, {})
                    vf = tk.Frame(fr, bg=C["bg_medium"])
                    vf.pack(fill=tk.X, padx=12, pady=1)
                    rc = C["accent_red"] if v.get("risk") in ("KRITIS", "SANGAT TINGGI") else C["accent_yellow"]
                    tk.Label(vf, text=f"  {v.get('name', vk)} [{v.get('risk', '?')}]",
                             font=("Segoe UI", 8, "bold"), fg=rc, bg=C["bg_medium"]).pack(anchor=tk.W)
                    tk.Label(vf, text=f"  💬 {v.get('desc', '')}",
                             font=("Segoe UI", 7), fg=C["text_secondary"], bg=C["bg_medium"]).pack(anchor=tk.W)
                    tk.Label(vf, text=f"  🛡️ Fix: {v.get('fix', '')}",
                             font=("Segoe UI", 7), fg=C["cyber_green"], bg=C["bg_medium"]).pack(anchor=tk.W)
                tv += len(g["vulnerabilities"])
            else:
                tk.Label(fr, text="✅ Tidak ada kerentanan kritis",
                         font=("Segoe UI", 8), fg=C["accent_green"], bg=C["bg_card"]).pack(anchor=tk.W, padx=8)
        rl = "🔴 KRITIS" if tv >= 8 else "🟡 SEDANG" if tv >= 4 else "🟢 RENDAH"
        tk.Label(vw, text=f"Total: {tv} kerentanan | Level: {rl}",
                 font=("Segoe UI", 10, "bold"),
                 fg=C["accent_red"] if tv >= 8 else C["accent_yellow"], bg=C["bg_dark"]).pack(pady=5)
        tk.Button(vw, text="✅ Tutup", command=vw.destroy,
                  bg=C["accent_blue"], fg="white", font=("Segoe UI", 10, "bold"),
                  cursor="hand2", relief=tk.FLAT, padx=20, pady=5).pack(pady=10)
        self._add_log(f"🔍 Scan selesai: {tv} kerentanan ditemukan.", "cyber_warn")
        self._add_log("─" * 40, "separator")
        self._notify(f"🔍 Scan: {tv} kerentanan ditemukan | Level: {rl}", color=C["accent_orange"])

    # ============================================================
    # RESTORATION
    # ============================================================
    def _start_restoration(self):
        if self.running or self.restoring or self.paused:
            return
        mati = [g for g in self.gardus if not g["status"]]
        if not mati:
            messagebox.showinfo("Info", "Semua gardu sudah aktif!")
            return
        self.restoring = True
        self.btn_restore.config(state=tk.DISABLED, text="⏳ MEMULIHKAN...", bg=C["bg_medium"])
        self._add_log("🔧 PEMULIHAN LISTRIK DIMULAI", "restore")
        self._add_log("📋 Prioritas: RS → Industri → Perumahan", "restore")
        self._add_log("─" * 40, "separator")
        self._add_timeline_event("restore", f"Pemulihan dimulai: {len(mati)} gardu", "restore")
        self._notify("🔧 Memulai pemulihan listrik...", color=C["accent_cyan"])
        self._restore_step(mati, 0)

    def _restore_step(self, mati, idx):
        if idx >= len(mati):
            self.restoring = False
            self.btn_restore.config(state=tk.NORMAL, text="🔧 PEMULIHAN LISTRIK  [F4]", bg=C["accent_green"])
            self._add_log("✅ PEMULIHAN SELESAI!", "success")
            self._add_log("─" * 40, "separator")
            self._draw_all()
            self._update_all()
            self._add_timeline_event("restore", "Pemulihan selesai ✅", "success")
            self._notify("✅ Semua gardu berhasil dipulihkan!", color=C["accent_green"], duration=3000)
            return

        g = mati[idx]
        self._add_log(f"🔧 Memulihkan {g['name']}...", "restore")
        g["status"] = True
        g["load"] = 0
        g["compromised"] = False
        g["scada_online"] = True
        self.total_restorations += 1
        self._add_log(f"🟢 {g['name']} aktif kembali!", "success")

        for area in sorted([a for a in self.areas if a["gardu_id"] == g["id"] and not a["status"]],
                           key=lambda a: a["priority"]):
            if g["load"] + area["load"] <= g["capacity"]:
                area["status"] = True
                g["load"] += area["load"]
                for h in self.houses:
                    if h["area_id"] == area["id"]:
                        h["status"] = True
                pl = {1: "KRITIS", 2: "PENTING", 3: "NORMAL"}[area["priority"]]
                self._add_log(f"💡 {area['icon']} {area['name']} dipulihkan [{pl}]", "success")
            else:
                self._add_log(f"⚠️ {area['name']} belum bisa - kapasitas penuh!", "warning")

        self._draw_all()
        self._update_all()
        self.root.update()
        time.sleep(0.12 / self.simulation_speed)
        self._add_log(f"✅ {g['name']}: {g['load']}/{g['capacity']} MW", "info")
        self._add_log("─" * 30, "separator")
        self.root.after(400, lambda: self._restore_step(mati, idx + 1))

    # ============================================================
    # LOAD BALANCE
    # ============================================================
    def _load_balance(self):
        if self.running or self.restoring:
            return
        aktif = [g for g in self.gardus if g["status"]]
        if len(aktif) < 2:
            messagebox.showinfo("Info", "Minimal 2 gardu aktif diperlukan.")
            return
        self._add_log("⚖️ LOAD BALANCING...", "info")
        moved = 0
        for g in aktif:
            pct = (g["load"] / g["capacity"]) * 100 if g["capacity"] > 0 else 0
            if pct > 85:
                for area in [a for a in self.areas if a["gardu_id"] == g["id"] and a["status"] and a["priority"] == 3]:
                    for tg in aktif:
                        if tg["id"] != g["id"] and tg["load"] + area["load"] <= tg["capacity"]:
                            tp = (tg["load"] / tg["capacity"]) * 100
                            if tp < 70:
                                g["load"] -= area["load"]
                                area["gardu_id"] = tg["id"]
                                tg["load"] += area["load"]
                                moved += 1
                                self._add_log(f"↪️ {area['name']}: {g['name']} → {tg['name']}", "info")
                                break
        self._add_log(f"✅ {moved} area dipindah." if moved else "ℹ️ Tidak ada perubahan.",
                      "success" if moved else "info")
        self._add_log("─" * 40, "separator")
        self._draw_all()
        self._update_all()
        msg = f"⚖️ Load Balance selesai: {moved} area dipindah" if moved else "ℹ️ Load sudah seimbang"
        self._notify(msg, color=C["accent_green"] if moved else C["accent_yellow"])

    # ============================================================
    # CANVAS INTERACTION
    # ============================================================
    def _on_canvas_click(self, event):
        if self.running or self.restoring:
            return
        for g in self.gardus:
            if abs(event.x - g["x"]) < 45 and abs(event.y - g["y"]) < 35:
                self._show_gardu_info(g)
                if g["status"]:
                    if messagebox.askyesno("Konfirmasi", f"Trigger blackout pada {g['name']}?"):
                        self._add_log(f"🖱️ Manual: {g['name']} dimatikan", "warning")
                        self.total_blackouts += 1
                        self.running = True
                        self.btn_auto.config(state=tk.DISABLED)
                        self.undo_stack.append({"type": "blackout", "gardu_id": g["id"], "reason": "Manual"})
                        self._add_timeline_event("blackout", f"Manual trigger: {g['name']}", "warning")
                        self._cascade(g)
                        self.running = False
                        self.btn_auto.config(state=tk.NORMAL, text="⚡ BLACKOUT OTOMATIS  [F2]", bg=C["accent_red"])
                return
        for area in self.areas:
            if abs(event.x - area["x"]) < 20 and abs(event.y - area["y"]) < 20:
                self._show_area_info(area)
                return

    def _on_canvas_hover(self, event):
        for g in self.gardus:
            if abs(event.x - g["x"]) < 45 and abs(event.y - g["y"]) < 35:
                lp = (g["load"] / g["capacity"]) * 100 if g["capacity"] > 0 else 0
                st = "🟢 Aktif" if g["status"] else "🔴 Mati"
                comp = " 💀 HACKED" if g.get("compromised") else ""
                self._show_tooltip(
                    event,
                    f"{g['name']}{comp}\n"
                    f"{st}\n"
                    f"{g['load']}/{g['capacity']}MW ({lp:.0f}%)\n"
                    f"OS: {g['os']}\n"
                    f"Protocol: {g['protocol']}\n"
                    f"Firewall: {'✅' if g['firewall'] else '❌'} | IDS: {'✅' if g['ids'] else '❌'}\n"
                    f"Kerentanan: {len(g['vulnerabilities'])}\n"
                    f"{g['desc']}"
                )
                return
        for area in self.areas:
            if abs(event.x - area["x"]) < 20 and abs(event.y - area["y"]) < 20:
                g = self.gardus[area["gardu_id"]]
                st = "💡 Nyala" if (area["status"] and g["status"]) else "🌑 Padam"
                pr = {1: "⭐ Kritis", 2: "🔶 Penting", 3: "⚪ Normal"}[area["priority"]]
                self._show_tooltip(
                    event,
                    f"{area['icon']} {area['name']}\n"
                    f"{st}\n"
                    f"Beban: {area['load']}MW\n"
                    f"Prioritas: {pr}\n"
                    f"Populasi: {area.get('population', 0)} jiwa\n"
                    f"Rumah: {area.get('house_count', 0)}\n"
                    f"Gardu: {g['name']}\n"
                    f"{area['desc']}"
                )
                return
        self._hide_tooltip()

    def _show_tooltip(self, event, text):
        self._hide_tooltip()
        tw = tk.Toplevel(self.root)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{event.x_root + 15}+{event.y_root + 10}")
        tw.configure(bg=C["bg_card"])
        fr = tk.Frame(tw, bg=C["bg_card"], highlightbackground=C["accent_blue"], highlightthickness=1)
        fr.pack()
        tk.Label(fr, text=text, font=("Segoe UI", 8), bg=C["bg_card"],
                 fg=C["text_primary"], justify=tk.LEFT, padx=8, pady=5).pack()
        self.tooltip_window = tw

    def _hide_tooltip(self, event=None):
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None

    def _show_gardu_info(self, g):
        lp = (g["load"] / g["capacity"]) * 100 if g["capacity"] > 0 else 0
        st = "🟢 AKTIF" if g["status"] else "🔴 BLACKOUT"
        comp = "\n💀 DIKOMPROMI HACKER!" if g.get("compromised") else ""
        ac = sum(1 for a in self.areas if a["gardu_id"] == g["id"] and a["status"])
        tc = sum(1 for a in self.areas if a["gardu_id"] == g["id"])
        vt = "".join(
            f"\n  ⚠️ {VULNS.get(v, {}).get('name', v)} [{VULNS.get(v, {}).get('risk', '?')}]"
            for v in g["vulnerabilities"]
        )
        self.lbl_info.config(text=(
            f"🏭 {g['name']}{comp}\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"Status: {st}\n"
            f"Kapasitas: {g['capacity']}MW\n"
            f"Beban: {g['load']}MW ({lp:.0f}%)\n"
            f"Area: {ac}/{tc}\n"
            f"OS: {g['os']}\n"
            f"Protocol: {g['protocol']}\n"
            f"Firewall: {'✅' if g['firewall'] else '❌'}\n"
            f"IDS: {'✅' if g['ids'] else '❌'}\n"
            f"Trip: {g['trip_count']}x\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"🔍 Kerentanan ({len(g['vulnerabilities'])}):{vt}\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"📝 {g['desc']}"
        ))

    def _show_area_info(self, area):
        g = self.gardus[area["gardu_id"]]
        st = "💡 NYALA" if (area["status"] and g["status"]) else "🌑 PADAM"
        pr = "⭐ KRITIS (RS)" if area["priority"] == 1 else "🔶 PENTING" if area["priority"] == 2 else "⚪ NORMAL"
        ah = [h for h in self.houses if h["area_id"] == area["id"]]
        gs = sum(1 for h in ah if h["has_generator"])
        sl = sum(1 for h in ah if h["has_solar"])
        md = sum(1 for h in ah if h["has_medical_equipment"])
        pop = sum(h["family_size"] for h in ah)
        self.lbl_info.config(text=(
            f"{area['icon']} {area['name']}\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"Status: {st}\n"
            f"Beban: {area['load']}MW\n"
            f"Prioritas: {pr}\n"
            f"Populasi: {area.get('population', 0)} jiwa\n"
            f"Rumah: {area.get('house_count', 0)}\n"
            f"Gardu: {g['name']} ({g['protocol']})\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"🏠 Detail Perumahan:\n"
            f"  Total unit: {len(ah)}\n"
            f"  👥 Total jiwa: {pop}\n"
            f"  ⚡ Generator: {gs}\n"
            f"  ☀️ Solar: {sl}\n"
            f"  🏥 Alat medis: {md}\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"📝 {area['desc']}"
        ))
        if area["priority"] == 1 and not area["status"]:
            messagebox.showwarning(
                "🏥 Fasilitas Kritis Terdampak",
                f"⚠️ {area['name']} adalah fasilitas PRIORITAS 1 (KRITIS)!\n\n"
                f"Jika listrik padam:\n"
                f"• ICU/OK kehilangan daya cadangan\n"
                f"• Alat medis vital (ventilator, monitor) berisiko\n"
                f"• Vaksin dan obat di cold chain rusak\n\n"
                f"Segera pulihkan gardu {g['name']}!"
            )

    # ============================================================
    # TOGGLE FUNCTIONS
    # ============================================================
    def _toggle_legend(self):
        self.show_legend = not self.show_legend
        self._draw_all()

    def _toggle_connections(self):
        self.show_connections = not self.show_connections
        self._draw_all()

    def _toggle_labels(self):
        self.show_labels = not self.show_labels
        self._draw_all()

    def _toggle_minimap(self):
        self.show_minimap = not self.show_minimap
        if self.show_minimap:
            self.minimap_frame.place(relx=1.0, rely=0.0, anchor=tk.NE, x=-4, y=4)
            self._notify("🗺️ Minimap ditampilkan", color=C["accent_cyan"])
        else:
            self.minimap_frame.place_forget()
            self._notify("🗺️ Minimap disembunyikan", color=C["text_muted"])

    # ============================================================
    # DEFENSE / WEATHER / SPEED
    # ============================================================
    def _on_defense_change(self, val):
        self.cyber_defense_level = self.defense_var.get()
        self.lbl_defense.config(text=f"{self.cyber_defense_level}%")
        dc = C["cyber_green"] if self.cyber_defense_level >= 70 else C["cyber_yellow"] if self.cyber_defense_level >= 40 else C["cyber_red"]
        self.lbl_defense.config(fg=dc)
        self._add_log(f"🛡️ Pertahanan Siber: {self.cyber_defense_level}%", "defense")
        for g in self.gardus:
            if self.cyber_defense_level >= 70:
                if g["firewall"] and g["ids"] and not g["compromised"]:
                    g["scada_online"] = True
            elif self.cyber_defense_level >= 40:
                if not g.get("compromised"):
                    g["scada_online"] = g["firewall"]

    def _on_weather_change(self):
        self.weather = self.weather_var.get()
        icons = {"cerah": "☀️ Cerah", "hujan": "🌧️ Hujan", "badai": "⛈️ Badai"}
        risks = {
            "cerah": ("Rendah", C["accent_green"]),
            "hujan": ("Sedang", C["accent_yellow"]),
            "badai": ("TINGGI", C["accent_red"])
        }
        text = icons.get(self.weather, "☀️ Cerah")
        risk_text, risk_color = risks.get(self.weather, ("Rendah", C["accent_green"]))
        self.lbl_weather.config(text=f"{text}", fg=risk_color)
        self.lbl_weather_risk.config(text=f"Risiko: {risk_text}", fg=risk_color)
        self._add_log(f"{icons[self.weather]} Cuaca berubah → {self.weather}", "weather")
        self._add_timeline_event("weather", f"Cuaca berubah ke {self.weather}", "weather")

        if self.weather == "badai":
            self._add_log("⛈️ Risiko badai! Risiko blackout naik 3x!", "warning")
            self._notify("⛈️ BADAI! Risiko blackout meningkat 3x!", color=C["accent_red"], duration=3000)
            if not self.running and random.random() < 0.3:
                self.root.after(2000, self._auto_blackout)

    def _on_speed_change(self, v):
        self.simulation_speed = float(v)
        self.lbl_sb_speed.config(text=f"Speed: {self.simulation_speed}x")

    # ============================================================
    # RESET
    # ============================================================
    def _reset_simulation(self):
        if messagebox.askyesno("Konfirmasi", "Reset semua data?\nSemua progress akan hilang."):
            self._init_default_data()
            self._add_log("🔄 Simulasi di-reset.", "info")
            self._add_log("─" * 40, "separator")
            self._notify("🔄 Simulasi berhasil di-reset!", color=C["accent_cyan"])

    # ============================================================
    # HELP
    # ============================================================
    def _show_help(self):
        hw = tk.Toplevel(self.root)
        hw.title(f"📖 Bantuan Simulasi v{VERSION}")
        hw.geometry("700x650")
        hw.configure(bg=C["bg_dark"])

        tk.Label(hw, text=f"⚡ PANDUAN SIMULASI BLACKOUT v{VERSION}",
                 font=("Segoe UI", 14, "bold"), fg=C["accent_cyan"], bg=C["bg_dark"]).pack(pady=10)

        notebook_frame = tk.Frame(hw, bg=C["bg_dark"])
        notebook_frame.pack(fill=tk.BOTH, expand=True, padx=10)

        tab_frame = tk.Frame(notebook_frame, bg=C["bg_medium"])
        tab_frame.pack(fill=tk.X)
        content_frame = tk.Frame(notebook_frame, bg=C["bg_card"])
        content_frame.pack(fill=tk.BOTH, expand=True)

        help_tabs = {
            "🎮 Kontrol": (
                "TOMBOL UTAMA\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                "⚡ Blackout Otomatis [F2]\n"
                "  Memicu blackout acak berdasarkan cuaca.\n\n"
                "💀 Serangan Siber [F3]\n"
                "  Pilih dari 6 teknik hacking berbeda.\n\n"
                "🔧 Pemulihan Listrik [F4]\n"
                "  Pulihkan gardu dengan prioritas kritis dulu.\n\n"
                "⚖️ Load Balance [F6]\n"
                "  Seimbangkan beban antar gardu aktif.\n\n"
                "🔍 Scan Kerentanan [F7]\n"
                "  Lihat celah keamanan di setiap gardu.\n\n"
                "📄 Export Report [F8]\n"
                "  Export laporan lengkap simulasi ke .txt\n\n"
                "📅 Timeline [F9]\n"
                "  Lihat riwayat semua kejadian."
            ),
            "⌨️ Shortcuts": (
                "KEYBOARD SHORTCUTS LENGKAP\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                "[F1]         Bantuan / Help\n"
                "[F2]         Blackout Otomatis\n"
                "[F3]         Serangan Siber\n"
                "[F4]         Pemulihan Listrik\n"
                "[F5]         Reset Simulasi\n"
                "[F6]         Load Balance\n"
                "[F7]         Scan Kerentanan\n"
                "[F8]         Export Report\n"
                "[F9]         Timeline History\n"
                "[F10]        Toggle Minimap\n"
                "[F11]        Credits / Info\n"
                "[Space]      Pause / Resume\n"
                "[+] / [-]    Speed Up / Down\n"
                "[Ctrl+Z]     Undo Aksi Terakhir\n"
                "[Ctrl+S]     Export Log\n"
                "[Ctrl+L]     Clear Log\n"
                "[Ctrl+M]     Toggle Minimap\n"
                "[Ctrl+1~4]   Ganti View Tab\n"
                "[Ctrl+R]     Reset"
            ),
            "🗺️ Peta": (
                "INTERAKSI PETA\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                "🖱️ Klik GARDU → Info + trigger blackout manual\n"
                "🖱️ Klik AREA  → Detail perumahan & status\n"
                "🖱️ Hover      → Quick info tooltip\n\n"
                "TOMBOL PETA (kiri atas):\n"
                "• 📋 Legenda   → Tampilkan/sembunyikan legenda\n"
                "• 🔗 Koneksi  → Tampilkan/sembunyikan kabel\n"
                "• 🏷️ Label    → Tampilkan/sembunyikan nama\n"
                "• 🗺️ Minimap  → Tampilkan/sembunyikan minimap [F10]\n\n"
                "VIEW TABS:\n"
                "• Jaringan Listrik  [Ctrl+1] → Peta gardu & area\n"
                "• Denah Perumahan   [Ctrl+2] → Rumah per blok\n"
                "• Serangan Siber    [Ctrl+3] → Topologi keamanan\n"
                "• Dampak & Analisis [Ctrl+4] → Ekonomi/sosial/health"
            ),
            "☁️ Cuaca": (
                "SISTEM CUACA\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                "☀️ Cerah   → Risiko RENDAH (gangguan mekanis)\n"
                "🌧️ Hujan  → Risiko SEDANG (konsleting, banjir)\n"
                "⛈️ Badai  → Risiko TINGGI (petir, 3x lebih sering)\n\n"
                "🔄 Auto Cuaca → Cuaca berubah otomatis tiap 300 tick\n\n"
                "Cuaca mempengaruhi:\n"
                "• Frekuensi blackout spontan\n"
                "• Jenis penyebab kegagalan\n"
                "• Kemungkinan cascade failure"
            ),
            "📊 Fitur Baru": (
                f"FITUR BARU v{VERSION}\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                "🕐 JAM REALTIME\n"
                "  Jam dinding aktual tampil di top bar & status bar.\n\n"
                "📈 GRAFIK LOAD HISTORY\n"
                "  Sparkline beban 60 tick terakhir di panel kiri.\n\n"
                "🏆 CREDITS [F11]\n"
                f"  Creator By {CREATOR} · {ORG}\n\n"
                "⚡ OPTIMASI PERFORMA\n"
                "  Dirty-flag: canvas hanya di-redraw saat ada perubahan.\n\n"
                "⌨️ KEYBOARD SHORTCUTS\n"
                "  Semua fungsi utama punya shortcut F-key.\n\n"
                "🗺️ MINIMAP\n"
                "  Peta kecil di pojok kanan atas canvas.\n\n"
                "📅 TIMELINE HISTORY\n"
                "  Catat semua kejadian + filter + export CSV.\n\n"
                "📄 EXPORT REPORT\n"
                "  Laporan lengkap .txt dengan statistik detail.\n\n"
                "🔔 NOTIFIKASI POPUP\n"
                "  Notifikasi non-blocking di pojok kanan bawah.\n\n"
                "↩️ UNDO\n"
                "  Batalkan blackout terakhir (Ctrl+Z).\n\n"
                "📈 UPTIME SCORE\n"
                "  Skor performa sistem berdasarkan uptime.\n\n"
                "⏸ PAUSE / RESUME\n"
                "  Jeda simulasi kapan saja dengan [Space].\n\n"
                "📊 STATUS BAR\n"
                "  Bar bawah menampilkan info real-time."
            ),
        }

        current_tab = tk.StringVar(value="🎮 Kontrol")
        tab_buttons = {}

        help_text = tk.Text(content_frame, bg=C["bg_card"], fg=C["text_primary"],
                            font=("Segoe UI", 10), wrap=tk.WORD, relief=tk.FLAT, padx=15, pady=15)
        help_text.pack(fill=tk.BOTH, expand=True)

        def switch_help_tab(tab_name):
            current_tab.set(tab_name)
            for tb, tbtn in tab_buttons.items():
                tbtn.config(bg=C["accent_blue"] if tb == tab_name else C["bg_card"],
                            fg="white" if tb == tab_name else C["text_secondary"])
            help_text.config(state=tk.NORMAL)
            help_text.delete("1.0", tk.END)
            help_text.insert(tk.END, help_tabs[tab_name])
            help_text.config(state=tk.DISABLED)

        for tab_name in help_tabs:
            btn = tk.Button(tab_frame, text=tab_name,
                            command=lambda tn=tab_name: switch_help_tab(tn),
                            bg=C["accent_blue"] if tab_name == "🎮 Kontrol" else C["bg_card"],
                            fg="white" if tab_name == "🎮 Kontrol" else C["text_secondary"],
                            font=("Segoe UI", 8, "bold"), relief=tk.FLAT, cursor="hand2", padx=8, pady=4)
            btn.pack(side=tk.LEFT, padx=1, pady=2)
            tab_buttons[tab_name] = btn

        switch_help_tab("🎮 Kontrol")

        tk.Button(hw, text="✅ Tutup", command=hw.destroy,
                  bg=C["accent_blue"], fg="white", font=("Segoe UI", 11, "bold"),
                  cursor="hand2", relief=tk.FLAT, padx=20, pady=8).pack(pady=10)

    def _start_animation_loop(self):
        self._animation_step()

    def _animation_step(self):
        if not self.paused:
            self.animation_frame = (self.animation_frame + 1) % 1000
            self.pulse_phase = (self.pulse_phase + 1) % 1000
            self.simulation_time += 1

            # Auto weather change
            if self.auto_weather_var.get() and self.simulation_time % 300 == 0:
                old_weather = self.weather
                new_weather = random.choices(["cerah", "hujan", "badai"], weights=[60, 30, 10])[0]
                if old_weather != new_weather:
                    self.weather_var.set(new_weather)
                    self._on_weather_change()

            # Animasi per-interval — hanya redraw jika dirty atau setiap 6 frame
            if self.animation_frame % 6 == 0 or self._dirty:
                self._draw_all()
                self._update_all()
                self._dirty = False
                if self.weather == "badai" and random.random() < 0.1:
                    self.lightning_flash = True
                    self.root.after(100, lambda: setattr(self, 'lightning_flash', False))

            # Progress bar animation (cheap, always run)
            if self.progress_active:
                self.progress_value = (self.progress_value + 8) % (self.progress_bar_canvas.winfo_width() or 800)

            # idle-time load balancing warning
            if self.simulation_time % 10 == 0 and not self.running and not self.restoring:
                for gardu in self.gardus:
                    if gardu["status"]:
                        pct = (gardu["load"] / gardu["capacity"]) * 100 if gardu["capacity"] > 0 else 0
                        if pct > 100 and random.random() < 0.01:
                            self._add_log(f"⚡ {gardu['name']} overload! Melepas beban...", "warning")
                            self._dirty = True

        # Always update realtime clock every cycle (very cheap)
        now_str = datetime.now().strftime("%H:%M:%S")
        try:
            self.lbl_realtime_clock.config(text=f"🕐 {now_str}")
            self.lbl_sb_realtime.config(text=f"🕐 {now_str}")
        except Exception:
            pass

        interval = max(50, int(200 / self.simulation_speed))
        self.root.after(interval, self._animation_step)


# ============================================================
# MAIN ENTRY POINT
# ============================================================
if __name__ == "__main__":
    root = tk.Tk()
    app = BlackoutSimulation(root)
    root.mainloop()