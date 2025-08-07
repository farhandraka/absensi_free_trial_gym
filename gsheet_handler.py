import gspread
import streamlit as st
import json
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
import time

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

# Retry function agar lebih stabil
def safe_get_all_records(max_retries=3, wait_seconds=2):
    for i in range(max_retries):
        try:
            return sheet.get_all_records()
        except Exception as e:
            if i < max_retries - 1:
                time.sleep(wait_seconds)
            else:
                st.error("Gagal mengambil data dari Google Sheets. Coba beberapa saat lagi.")
                return []

def get_worksheet_df():
    data = safe_get_all_records()
    return pd.DataFrame(data)

def get_participant_count(tanggal, sesi, status=None):
    df = get_worksheet_df()
    if df.empty:
        return 0

    df = df[df['Tanggal Hadir'] == tanggal]
    df = df[df['Sesi'] == sesi]

    if status:
        df = df[df['Status'] == status]

    return len(df)

def append_row(data):
    try:
        sheet.append_row(data)
    except Exception as e:
        st.error(f"[ERROR] Gagal menyimpan data: {e}")

def get_all_data():
    try:
        return sheet.get_all_records()
    except Exception as e:
        st.error(f"[ERROR] Gagal mengambil data: {e}")
        return []
