import os
import time
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

JSON_PATH = 'D:/Project_Absen_Gym/etl-gsheet-to-sql-df5caccb37f0.json'
DRIVE_FOLDER_ID = '1al68ecONi082KoO2AhPCNJG9zxvPk_BJ'

# Setup drive client
creds = service_account.Credentials.from_service_account_file(
    JSON_PATH, scopes=["https://www.googleapis.com/auth/drive"]
)
drive_service = build('drive', 'v3', credentials=creds)

def upload_file_to_drive(file, nama, tanggal, sesi, folder_id="1al68ecONi082KoO2AhPCNJG9zxvPk_BJ"):
    from google.oauth2 import service_account
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaIoBaseUpload
    import io

    creds = service_account.Credentials.from_service_account_file(
        "etl-gsheet-to-sql-df5caccb37f0.json",
        scopes=["https://www.googleapis.com/auth/drive"]
    )
    drive_service = build("drive", "v3", credentials=creds)

    filename = f"{tanggal}_{sesi}_{nama}.{file.name.split('.')[-1]}"
    media = MediaIoBaseUpload(io.BytesIO(file.read()), mimetype=file.type)

    file_metadata = {
        "name": filename,
        "parents": [folder_id]
    }

    uploaded_file = drive_service.files().create(
        body=file_metadata,
        media_body=media,
        fields="id",
        supportsAllDrives=True  # ✅ Tambahkan ini
    ).execute()

    file_id = uploaded_file.get("id")
    return f"https://drive.google.com/file/d/{file_id}/view"

