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

    kapasitas = 4 if sesi == "Sesi 5" else 6
    label_ditampilkan = f"{label_asli} ({jumlah_peserta}/{kapasitas})"
    sesi_interaktif.append(label_ditampilkan)
    sesi_mapping[label_ditampilkan] = (label_asli, kapasitas)

# Pilih sesi
sesi_pilihan_label = st.selectbox("🕒 Pilih Sesi (dengan info kuota)", sesi_interaktif)
sesi, kapasitas_maks = sesi_mapping[sesi_pilihan_label]

# Cek slot sesi
peserta_di_sesi = get_participant_count(tanggal_hadir, sesi)

if peserta_di_sesi >= kapasitas_maks:
    st.warning(f"❌ Sesi ini sudah penuh ({peserta_di_sesi}/{kapasitas_maks})")
    
    # Tambahan informasi jika waiting list juga penuh
    if peserta_di_sesi >= kapasitas_maks + 3:
        st.info(f"⚠️ Info: Sesi ini sudah mencapai batas maksimum termasuk waiting list yaitu {kapasitas_maks + 3} orang. "
                f"Silakan pilih sesi lain karena waiting list juga sudah penuh.")
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
    st.caption("**Bank Mandiri** : *1240013317939* Atas Nama **Caesesya Fitra Adrila**")
    st.caption("*Bank Syariah Indonesia (BSI) : 7153435531 Atas Nama Caesesya Fitra Adrila*")
    st.caption("*Bank Central Asia (BCA) : 6042810955 Atas Nama Siti Badriah*")
    st.caption("*Mohon untuk upload bukti pembayaran terlebih dahulu sebelum melanjutkan atau bisa kirim bukti pembayaran ke whatsapp admin House of Caesar : 087720036581*")

    upload_status = st.selectbox("Status Upload Bukti di Google Form atau Whatsapp Admin", ["Belum Upload", "Sudah Upload"])
    status_pembayaran = st.selectbox("Status Pembayaran", ["Sudah Bayar"])

    submitted = st.form_submit_button("✅ Submit")

    if submitted:
        if not nama or not no_hp or not email or not alamat:
            st.warning("⚠️ Harap lengkapi semua data sebelum submit.")
        elif upload_status != "Sudah Upload":
            st.warning("⚠️ Harap upload bukti pembayaran terlebih dahulu ke Google Form atau Whatsapp : 087720036581 (Admin HoC).")
        else:
            confirmed_count = get_participant_count(tanggal_hadir, sesi, status="Confirmed")
            waiting_list_count = get_participant_count(tanggal_hadir, sesi, status="Waiting List")

            if confirmed_count >= kapasitas_maks and waiting_list_count >= 3:
                st.error("❌ Sesi ini sudah penuh dan *Waiting List* juga sudah penuh. Silakan pilih sesi lain.")
            else:
                if confirmed_count < kapasitas_maks:
                    status = "Confirmed"
                    st.success("✅ Absensi berhasil disimpan. Terimakasih sudah mendaftar!")
                    st.balloons()
                else:
                    status = "Waiting List"
                    st.info("📋 Sesi sudah penuh. Kamu masuk ke *Waiting List*. Admin akan hubungi jika ada slot kosong.")

                append_row([
                    nama,
                    umur,
                    jenis_kelamin,
                    no_hp,
                    email,
                    alamat,
                    tanggal_hadir,
                    sesi,
                    status_pembayaran,
                    upload_status,
                    status
                ])

                st.markdown("📎 [Upload Ulang Bukti jika Diperlukan](https://forms.gle/txyE7MbHueSJWjC66)")



