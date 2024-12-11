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

# Show selected customer information with better formatting
st.subheader(f"Informasi Pelanggan {customer_id}")

# Using markdown for better structure
st.markdown(f"**Riwayat Transaksi:** {customer_data['transaction_history']}")
st.markdown(f"**Jumlah Pinjaman:** {customer_data['loan_amount']}")
st.markdown(f"**Skor Kredit:** {customer_data['credit_score']}")
st.markdown(f"**Syarat Pinjaman:** {customer_data['loan_terms']}")
st.markdown(f"**Status Transaksi:** {customer_data['transaction_status']}")

# Run the agent logic
credit_score, status = credit_score_assessment(customer_data['customer_id'], customer_data['transaction_history'])
loan_terms = loan_negotiation(credit_score, customer_data['loan_amount'])
transaction_status = process_transaction(customer_data['loan_amount'], loan_terms, status)

# Display agent results with enhanced formatting
st.subheader("Hasil Penilaian dan Transaksi")

# Create a table to show the results
result_data = {
    "Skor Kredit yang Dihasilkan oleh Agen": [credit_score],
    "Status Kredit": [status],
    "Syarat Pinjaman yang Dinegosiasikan": [loan_terms],
    "Status Transaksi": [transaction_status]
}
result_df = pd.DataFrame(result_data)

st.table(result_df)  # Show the results in a table for better visualization

# Optionally, use a different color or layout for the status (approved/denied)
if status == "Approved":
    st.markdown('<p style="color: green;">Transaksi Disetujui!</p>', unsafe_allow_html=True)
else:
    st.markdown('<p style="color: red;">Transaksi Ditolak!</p>', unsafe_allow_html=True)
