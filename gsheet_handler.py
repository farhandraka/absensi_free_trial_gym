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

def get_worksheet_df():
    data = worksheet.get_all_records()
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
        print(f"[ERROR] append_row: {e}")

def get_all_data():
    try:
        return sheet.get_all_records()
    except Exception as e:
        print(f"[ERROR] get_all_data: {e}")
        return []


