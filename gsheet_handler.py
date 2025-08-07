import os
import json
import gspread
from google.oauth2.service_account import Credentials

# === Load Credentials dari Environment Variable ===
def load_credentials():
    try:
        service_account_info = json.loads(os.environ["GOOGLE_CREDENTIALS"])
        scopes = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive"
        ]
        credentials = Credentials.from_service_account_info(service_account_info, scopes=scopes)
        return credentials
    except Exception as e:
        print(f"[ERROR] load_credentials: {e}")
        return None

# === Inisialisasi Google Sheets ===
SPREADSHEET_NAME = 'Data_Absensi'
SHEET_NAME = "Sheet1"

try:
    creds = load_credentials()
    client = gspread.authorize(creds)
    sheet = client.open(SPREADSHEET_NAME).worksheet(SHEET_NAME)
except Exception as e:
    print(f"[ERROR] GSheet Init: {e}")
    sheet = None

# === Fungsi-fungsi untuk digunakan di Streamlit App ===
def get_participant_count(tanggal, sesi):
    """Menghitung jumlah peserta pada tanggal dan sesi tertentu."""
    try:
        if not sheet:
            return 0
        data = sheet.get_all_records()
        return sum(1 for row in data if str(row.get('Tanggal Hadir')) == tanggal and str(row.get('Sesi')) == sesi)
    except Exception as e:
        print(f"[ERROR] get_participant_count: {e}")
        return 0

def append_row(data):
    """Menambahkan satu baris ke Google Sheets."""
    try:
        if sheet:
            sheet.append_row(data)
    except Exception as e:
        print(f"[ERROR] append_row: {e}")

def get_all_data():
    """Mengambil semua data dari Google Sheets."""
    try:
        if sheet:
            return sheet.get_all_records()
        return []
    except Exception as e:
        print(f"[ERROR] get_all_data: {e}")
        return []
