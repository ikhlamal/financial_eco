import streamlit as st
import pandas as pd
import json

# Load the data from CSV
def load_data():
    data = pd.read_csv('financial_data.csv')
    return data

# Agen Penilaian Kredit: Fungsi untuk menghitung skor kredit dan memberikan status kredit
def credit_score_assessment(customer_id, transaction_history):
    # Misalnya kita menggunakan aturan sederhana untuk penilaian kredit
    transaction_data = json.loads(transaction_history)
    total_transactions = sum(transaction_data.values())  # Menjumlahkan transaksi
    if total_transactions > 1000:
        credit_score = 750
        status = "Approved"
    else:
        credit_score = 650
        status = "Denied"
    return credit_score, status

# Agen Negosiasi Pinjaman: Fungsi untuk menentukan syarat pinjaman
def loan_negotiation(credit_score, loan_amount):
    if credit_score > 700:
        loan_terms = f"3%, {loan_amount // 1000} months"
    else:
        loan_terms = f"5%, {loan_amount // 500} months"
    return loan_terms

# Agen Koordinasi Transaksi: Fungsi untuk memproses transaksi
def process_transaction(loan_amount, loan_terms, status):
    if status == "Approved":
        transaction_status = "Transaction Successful"
    else:
        transaction_status = "Transaction Denied"
    return transaction_status

# Streamlit interface
st.title("Multi-Agent System: Integrated Financial Ecosystem")

# Load the data
data = load_data()
st.subheader("Data Keuangan Pelanggan")
st.write(data)

# Select customer to simulate agent system
customer_id = st.selectbox("Pilih ID Pelanggan untuk Simulasi", data['customer_id'])

# Find the selected customer data
customer_data = data[data['customer_id'] == customer_id].iloc[0]

# Tampilkan subjudul dengan gaya yang lebih menarik
st.subheader(f"🔍 Informasi Pelanggan {customer_id}")
st.markdown(
    f"""
    <div style="background-color: #f1f1f1; padding: 10px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
        <h5><strong>Riwayat Transaksi</strong></h5>
        <p>{customer_data['transaction_history']}</p>
        
        <h5><strong>Jumlah Pinjaman</strong></h5>
        <p><strong>IDR {customer_data['loan_amount']}</strong></p>

        <h5><strong>Skor Kredit</strong></h5>
        <p>{customer_data['credit_score']}</p>

        <h5><strong>Syarat Pinjaman</strong></h5>
        <p>{customer_data['loan_terms']}</p>

        <h5><strong>Status Transaksi</strong></h5>
        <p>{customer_data['transaction_status']}</p>
    </div>
    """, unsafe_allow_html=True
)

# Jalankan logika agen
credit_score, status = credit_score_assessment(customer_data['customer_id'], customer_data['transaction_history'])
loan_terms = loan_negotiation(credit_score, customer_data['loan_amount'])
transaction_status = process_transaction(customer_data['loan_amount'], loan_terms, status)

# Tampilkan hasil dengan format lebih menarik
st.subheader("💡 Hasil Penilaian dan Transaksi")
st.markdown(
    f"""
    <div style="background-color: #e9f7f6; padding: 10px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
        <h5><strong>Skor Kredit yang Dihasilkan oleh Agen</strong></h5>
        <p>{credit_score}</p>

        <h5><strong>Status Kredit</strong></h5>
        <p>{status}</p>

        <h5><strong>Syarat Pinjaman yang Dinegosiasikan</strong></h5>
        <p>{loan_terms}</p>

        <h5><strong>Status Transaksi</strong></h5>
        <p>{transaction_status}</p>
    </div>
    """, unsafe_allow_html=True
)
