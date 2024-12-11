import streamlit as st
import pandas as pd
import numpy as np

# Fungsi untuk memuat data
@st.cache
def load_data(file_name):
    return pd.read_csv(file_name)

# Header aplikasi
st.title("Sistem Multiagen Cerdas dalam Ekosistem Keuangan Terintegrasi")

# Sidebar
st.sidebar.header("Navigasi")
menu = st.sidebar.selectbox("Pilih Menu", ["Home", "Data Agen", "Data Transaksi", "Simulasi Agen Cerdas"])

# Home Page
if menu == "Home":
    st.header("Selamat Datang!")
    st.write(
        """
        Aplikasi ini mengilustrasikan bagaimana agen-agen cerdas bekerja dalam ekosistem keuangan yang terintegrasi. 
        Setiap agen memiliki tugas spesifik, seperti menilai kredit, bernegosiasi pinjaman, dan mengelola transaksi keuangan.
        """
    )
    st.image("https://via.placeholder.com/800x400", caption="Arsitektur Sistem Multiagen")

# Data Agen Page
elif menu == "Data Agen":
    st.header("Data Agen Cerdas")
    st.write("Berikut adalah daftar agen cerdas dalam sistem:")
    data_agen = {
        "Agen": ["Agen Penilaian Kredit", "Agen Negosiasi", "Agen Koordinasi Transaksi"],
        "Fitur": [
            "Menilai skor kredit pelanggan berdasarkan data historis.",
            "Bernegosiasi suku bunga dan jumlah pinjaman.",
            "Mengelola transaksi antar pihak."
        ],
        "Teknologi": ["Machine Learning", "Reinforcement Learning", "Blockchain"],
    }
    df_agen = pd.DataFrame(data_agen)
    st.table(df_agen)

# Data Transaksi Page
elif menu == "Data Transaksi":
    st.header("Data Transaksi Keuangan")
    st.write("Berikut adalah data transaksi yang dikelola agen:")
    uploaded_file = st.file_uploader("Upload File CSV Transaksi", type=["csv"])
    if uploaded_file is not None:
        data_transaksi = load_data(uploaded_file)
        st.dataframe(data_transaksi)
    else:
        st.write("Silakan unggah file CSV untuk melihat data transaksi.")

# Simulasi Agen Cerdas Page
elif menu == "Simulasi Agen Cerdas":
    st.header("Simulasi Agen Cerdas")
    st.write("Simulasi bagaimana agen-agen bekerja untuk menyelesaikan tugas mereka.")

    # Input Data Simulasi
    skor_kredit = st.number_input("Masukkan Skor Kredit Pelanggan:", min_value=0, max_value=1000, value=750)
    kebutuhan_pinjaman = st.number_input("Masukkan Kebutuhan Pinjaman (dalam juta):", min_value=1, max_value=1000, value=100)
    suku_bunga = np.clip(0.1 + 0.005 * (1000 - skor_kredit) / 100, 0.05, 0.2)  # Rumus simulasi suku bunga

    # Output Simulasi
    st.write(f"**Skor Kredit Pelanggan:** {skor_kredit}")
    st.write(f"**Kebutuhan Pinjaman:** {kebutuhan_pinjaman} juta")
    st.write(f"**Suku Bunga yang Ditawarkan:** {suku_bunga:.2%}")

    # Proses Transaksi
    if st.button("Proses Transaksi"):
        transaksi_sukses = np.random.choice([True, False], p=[0.85, 0.15])
        if transaksi_sukses:
            st.success("Transaksi berhasil diproses oleh agen koordinasi!")
        else:
            st.error("Transaksi gagal. Silakan periksa kembali data atau hubungi pihak terkait.")
