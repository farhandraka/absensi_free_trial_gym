import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Konfigurasi
JSON_PATH = 'D:/Project_Absen_Gym/etl-gsheet-to-sql-df5caccb37f0.json'
SPREADSHEET_NAME = 'Data_Absensi'
SHEET_NAME = "Sheet1"

# Scope dan autentikasi
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]
credentials = ServiceAccountCredentials.from_json_keyfile_name(JSON_PATH, scope)
client = gspread.authorize(credentials)
sheet = client.open(SPREADSHEET_NAME).worksheet(SHEET_NAME)

def get_participant_count(tanggal, sesi):
    """Menghitung jumlah peserta pada tanggal dan sesi tertentu."""
    try:
        data = sheet.get_all_records()
        return sum(1 for row in data if str(row.get('Tanggal Hadir')) == tanggal and str(row.get('Sesi')) == sesi)
    except Exception as e:
        print(f"[ERROR] get_participant_count: {e}")
        return 0

def append_row(data):
    """Menambahkan satu baris ke Google Sheets."""
    try:
        sheet.append_row(data)
    except Exception as e:
        print(f"[ERROR] append_row: {e}")

def get_all_data():
    """Mengambil semua data dari Google Sheets."""
    try:
        return sheet.get_all_records()
    except Exception as e:
        print(f"[ERROR] get_all_data: {e}")
        return []
