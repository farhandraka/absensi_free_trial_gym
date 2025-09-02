# gsheet_handler.py (versi aman untuk sheet kosong)
import gspread
import streamlit as st
import json
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
import time
from itertools import zip_longest

# Ambil kredensial dari Streamlit secrets
creds_dict = json.loads(st.secrets["GOOGLE_CREDENTIALS"])

# Scope Google API
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

# Autentikasi
credentials = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(credentials)

# Nama file & sheet
SPREADSHEET_NAME = 'Data_Absensi'
SHEET_NAME = 'Sheet1'
sheet = client.open(SPREADSHEET_NAME).worksheet(SHEET_NAME)

# Kolom minimum yang dipakai app kamu
REQUIRED_COLS = ["Tanggal Hadir", "Sesi", "Status"]

def _empty_df():
    """DataFrame kosong tapi kolomnya lengkap supaya filter tidak error."""
    return pd.DataFrame(columns=REQUIRED_COLS)

# Retry function agar lebih stabil + bedakan sheet kosong vs error API
def safe_get_all_records(max_retries=3, wait_seconds=2):
    for i in range(max_retries):
        try:
            # Pakai get_all_values supaya bisa deteksi sheet kosong tanpa exception
            values = sheet.get_all_values()  # list of lists
            # Benar-benar kosong (tidak ada data sama sekali)
            if not values:
                return []  # kosong, bukan error

            header = values[0] if values else []
            # Baris header kosong semua -> anggap sheet kosong
            if not any(str(c).strip() for c in header):
                return []

            rows = values[1:]  # data tanpa header
            # Build records manual, aman untuk panjang baris yang tidak seragam
            records = []
            for row in rows:
                # zip_longest agar kolom yang tidak ada diisi '' bukan meledak
                item = {h: v for h, v in zip_longest(header, row, fillvalue="")}
                # Lewati baris yang benar-benar kosong
                if any(str(v).strip() for v in item.values()):
                    records.append(item)
            return records

        except Exception as e:
            if i < max_retries - 1:
                time.sleep(wait_seconds)
                continue
            # Hanya tampilkan error kalau benar-benar gagal akses API
            st.error("Gagal mengambil data dari Google Sheets. Coba beberapa saat lagi.")
            return []

def get_worksheet_df():
    records = safe_get_all_records()
    if not records:
        # Sheet kosong -> kembalikan DF kosong yang kolomnya sudah ada
        return _empty_df()

    df = pd.DataFrame(records)

    # Pastikan kolom minimum ada semua
    for col in REQUIRED_COLS:
        if col not in df.columns:
            df[col] = pd.NA

    return df

def get_participant_count(tanggal, sesi, status=None):
    df = get_worksheet_df()
    if df.empty:
        return 0

    # Normalisasi tipe agar perbandingan aman (string ke string)
    df["Tanggal Hadir"] = df["Tanggal Hadir"].astype(str).str.strip()
    tanggal = str(tanggal).strip()
    df["Sesi"] = df["Sesi"].astype(str).str.strip()

    q = (df["Tanggal Hadir"] == tanggal) & (df["Sesi"] == sesi)
    if status:
        # Jika kolom Status ada (selalu ada dari REQUIRED_COLS), tetap aman
        df["Status"] = df["Status"].astype(str).str.strip()
        q = q & (df["Status"] == status)

    return int(q.sum())

def append_row(data):
    try:
        sheet.append_row(data)
        # Jika kamu pakai cache, di Streamlit 1.11 bisa clear begini:
        # st.cache.clear_cache()
    except Exception as e:
        st.error(f"[ERROR] Gagal menyimpan data: {e}")

def get_all_data():
    # Konsisten pakai jalur aman
    return safe_get_all_records() or []
