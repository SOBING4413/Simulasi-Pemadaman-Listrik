@echo off
title Simulasi Blackout Area v2.1.0 - Exter Interactive
color 0B
cls

echo.
echo  ============================================================
echo   ⚡  SIMULASI BLACKOUT AREA v2.1.0
echo       Creator By Sobing4413  ^|  Exter Interactive
echo  ============================================================
echo.

:: ── Cek apakah Python sudah terinstall ──────────────────────
python --version >nul 2>&1
if %errorlevel% neq 0 (
    color 0C
    echo  [ERROR] Python TIDAK ditemukan di PC kamu!
    echo.
    echo  Cara Install Python:
    echo  1. Buka browser, pergi ke: https://www.python.org/downloads/
    echo  2. Download versi terbaru ^(Python 3.8 atau lebih baru^)
    echo  3. Jalankan installer
    echo  4. PENTING: Centang kotak "Add Python to PATH"
    echo  5. Klik Install Now
    echo  6. Setelah selesai, jalankan file ini lagi
    echo.
    echo  Mau buka halaman download Python sekarang? ^(Y/N^)
    set /p choice="  Pilihan kamu: "
    if /i "%choice%"=="Y" (
        start https://www.python.org/downloads/
    )
    echo.
    pause
    exit /b 1
)

:: ── Tampilkan versi Python yang ditemukan ───────────────────
for /f "tokens=*" %%i in ('python --version 2^>^&1') do set PYVER=%%i
echo  [OK] %PYVER% ditemukan!
echo.

:: ── Cek apakah tkinter tersedia ─────────────────────────────
python -c "import tkinter" >nul 2>&1
if %errorlevel% neq 0 (
    color 0E
    echo  [PERINGATAN] tkinter tidak ditemukan.
    echo.
    echo  Solusi:
    echo  - Uninstall Python lama, lalu install ulang dari:
    echo    https://www.python.org/downloads/
    echo  - Pastikan saat install, opsi "tcl/tk and IDLE" dicentang.
    echo.
    pause
    exit /b 1
)
echo  [OK] tkinter tersedia!
echo.

:: ── Cek apakah main.py ada di folder yang sama ──────────────
if not exist "%~dp0main.py" (
    color 0C
    echo  [ERROR] File main.py tidak ditemukan!
    echo.
    echo  Pastikan file "jalankan.bat" dan "main.py"
    echo  berada di FOLDER YANG SAMA.
    echo.
    pause
    exit /b 1
)
echo  [OK] main.py ditemukan!
echo.

:: ── Semua OK, jalankan simulasi ─────────────────────────────
echo  ============================================================
echo   Memulai Simulasi Blackout Area...
echo  ============================================================
echo.

python "%~dp0main.py"

:: ── Tangkap error jika program crash ────────────────────────
if %errorlevel% neq 0 (
    color 0C
    echo.
    echo  [ERROR] Program berhenti dengan error kode: %errorlevel%
    echo.
    echo  Coba langkah berikut:
    echo  1. Pastikan Python versi 3.8 atau lebih baru
    echo  2. Coba jalankan ulang file ini
    echo  3. Hubungi: Sobing4413 ^| Exter Interactive
    echo.
    pause
)
