import streamlit as st
import pandas as pd
import random

# Load data from CSV files
st.title("Sistem Multiagen Cerdas untuk Ekosistem Keuangan Terintegrasi")
st.sidebar.title("Navigasi")
menu = st.sidebar.radio("Pilih Menu", ["Dashboard", "Simulasi Agen"])

# Load databases
@st.cache_data
def load_data():
    customers = pd.read_csv("customers.csv")  # Data pelanggan
    transactions = pd.read_csv("transactions.csv")  # Data transaksi
    return customers, transactions

customers, transactions = load_data()

if menu == "Dashboard":
    st.header("Dashboard Ekosistem Keuangan")

    st.subheader("Data Pelanggan")
    st.dataframe(customers)

    st.subheader("Data Transaksi")
    st.dataframe(transactions)

elif menu == "Simulasi Agen":
    st.header("Simulasi Agen Cerdas")

    # Simulasi Penilaian Kredit
    st.subheader("1. Penilaian Kredit")
    
    def evaluate_credit_score(customer_data):
        """Fungsi sederhana untuk menghitung skor kredit berdasarkan data pelanggan."""
        return random.randint(300, 850)  # Simulasi nilai kredit

    customers["Credit_Score"] = customers.apply(evaluate_credit_score, axis=1)
    st.dataframe(customers[["Customer_ID", "Name", "Credit_Score"]])

    # Simulasi Negosiasi Pinjaman
    st.subheader("2. Negosiasi Pinjaman")
    def negotiate_loan(credit_score):
        """Menentukan jumlah pinjaman dan suku bunga berdasarkan skor kredit."""
        if credit_score >= 750:
            return "Low Interest", random.randint(5000, 20000)
        elif 600 <= credit_score < 750:
            return "Medium Interest", random.randint(3000, 10000)
        else:
            return "High Interest", random.randint(1000, 5000)

    customers[["Loan_Type", "Loan_Amount"]] = customers["Credit_Score"].apply(
        lambda x: pd.Series(negotiate_loan(x))
    )
    st.dataframe(customers[["Customer_ID", "Name", "Loan_Type", "Loan_Amount"]])

    # Simulasi Koordinasi Transaksi
    st.subheader("3. Koordinasi Transaksi")
    def process_transaction(transaction):
        """Memproses transaksi berdasarkan data pelanggan."""
        customer_id = transaction["Customer_ID"]
        customer = customers[customers["Customer_ID"] == customer_id]
        if not customer.empty:
            credit_score = customer.iloc[0]["Credit_Score"]
            return "Approved" if credit_score > 650 else "Denied"
        return "Invalid"

    transactions["Status"] = transactions.apply(process_transaction, axis=1)
    st.dataframe(transactions)

# Simpan data jika diubah
if st.button("Simpan Perubahan"):
    customers.to_csv("customers_updated.csv", index=False)
    transactions.to_csv("transactions_updated.csv", index=False)
    st.success("Data berhasil disimpan!")
