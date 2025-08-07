import gspread
import streamlit as st
import json
from oauth2client.service_account import ServiceAccountCredentials

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

def get_participant_count(tanggal, sesi):
    try:
        data = sheet.get_all_records()
        return sum(1 for row in data if str(row.get('Tanggal Hadir')) == tanggal and str(row.get('Sesi')) == sesi)
    except Exception as e:
        print(f"[ERROR] get_participant_count: {e}")
        return 0

def append_row(data):
    try:
        sheet.append_row(data)
    except Exception as e:
        print(f"[ERROR] append_row: {e}")

def get_all_data():
    try:
        return sheet.get_all_records()
    except Exception as e:
        print(f"[ERROR] get_all_data: {e}")
        return []
