import streamlit as st
from datetime import datetime
from gsheet_handler import get_participant_count, append_row

st.set_page_config(page_title="Open Class / Free Trial House of Caesar", layout="centered")
st.title("📋 Form Open Class/Free Trial - House of Caesar")

# Tanggal hadir terbatas (khusus event)
tanggal_opsi = {
    "5 September 2025": "2025-09-05",
    "6 September 2025": "2025-09-06",
    "7 September 2025": "2025-09-07"
}
tanggal_label = st.selectbox("📅 Pilih Tanggal Hadir", list(tanggal_opsi.keys()))
tanggal_hadir = tanggal_opsi[tanggal_label]

# Jadwal sesi
sesi_jadwal = {
    "Sesi 1": "7:00 - 8:45",
    "Sesi 2": "09:30 - 11:15",
    "Sesi 3": "13:15 - 15:00",
    "Sesi 4": "15:45 - 17:30",
    "Sesi 5": "20:00 - 22:00"
}

# Dropdown sesi + info kuota
sesi_interaktif = []
sesi_mapping = {}
for sesi, jam in sesi_jadwal.items():
    label_asli = f"{sesi} : {jam}"
    jumlah_peserta = get_participant_count(tanggal_hadir, label_asli)

    # Atur kapasitas berdasarkan sesi
    kapasitas = 4 if sesi == "Sesi 5" else 6

    label_ditampilkan = f"{label_asli} ({jumlah_peserta}/{kapasitas})"
    sesi_interaktif.append(label_ditampilkan)
    sesi_mapping[label_ditampilkan] = (label_asli, kapasitas)

# Pilih sesi sebelum form
sesi_pilihan_label = st.selectbox("🕒 Pilih Sesi (dengan info kuota)", sesi_interaktif)
sesi, kapasitas_maks = sesi_mapping[sesi_pilihan_label]

# Tampilkan info kuota langsung
peserta_di_sesi = get_participant_count(tanggal_hadir, sesi)
if peserta_di_sesi >= kapasitas_maks:
    st.warning(f"❌ Sesi ini sudah penuh ({peserta_di_sesi}/{kapasitas_maks})")
else:
    st.success(f"✅ Slot tersedia: {kapasitas_maks - peserta_di_sesi} dari {kapasitas_maks}")

# --- FORM ---
with st.form("absen_form"):
    nama = st.text_input("Nama Lengkap")
    umur = st.number_input("Umur", min_value=7, max_value=99, step=1)
    jenis_kelamin = st.selectbox("Jenis Kelamin", ["Laki-laki", "Perempuan"])
    no_hp = st.text_input("Nomor HP")
    email = st.text_input("Email")
    alamat = st.text_area("Alamat")

    st.markdown("### 📎 [Upload Bukti Pembayaran di Google Form](https://forms.gle/txyE7MbHueSJWjC66)")
    st.caption("*Mohon untuk upload bukti pembayaran terlebih dahulu sebelum melanjutkan atau bisa kirim bukti pembayaran ke whatsapp admin House of Caesar : 087720036581*")

    upload_status = st.selectbox("Status Upload Bukti di Google Form atau Whatsapp Admin", ["Belum Upload", "Sudah Upload"])
    status_pembayaran = st.selectbox("Status Pembayaran", ["Sudah Bayar"])

    submitted = st.form_submit_button("✅ Submit")

    if submitted:
        jumlah_peserta = get_participant_count(tanggal_hadir, sesi, status="Hadir")
    
        if jumlah_peserta < 6:
            status = "Hadir"
        else:
            jumlah_waiting = get_participant_count(tanggal_hadir, sesi, status="Waiting List")
            if jumlah_waiting < 3:
                status = "Waiting List"
            else:
                st.error("Sesi ini sudah penuh termasuk waiting list. Silakan pilih sesi lain.")
                st.stop()
    
        data = [nama, umur, jenis_kelamin, alamat, tanggal_hadir, sesi, status]
        append_row(data)
        st.success(f"Berhasil mendaftar sebagai '{status}' untuk sesi {sesi} pada {tanggal_hadir}")
        st.balloons()


        st.markdown("📎 [Upload Ulang Bukti jika Diperlukan](https://forms.gle/txyE7MbHueSJWjC66)")





