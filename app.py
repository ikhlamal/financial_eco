import streamlit as st
import pandas as pd
import random

# Load Data
@st.cache_data
def load_data(file_path):
    return pd.read_csv(file_path)

# Define Agents
class CreditScoringAgent:
    def __init__(self, credit_scores):
        self.credit_scores = credit_scores

    def get_credit_score(self, customer_id):
        customer_data = self.credit_scores[self.credit_scores['CustomerID'] == customer_id]
        if not customer_data.empty:
            return customer_data['CreditScore'].values[0]
        return None

class TransactionAgent:
    def __init__(self, transactions):
        self.transactions = transactions

    def record_transaction(self, sender, receiver, amount):
        transaction_id = len(self.transactions) + 1
        new_transaction = {
            "TransactionID": transaction_id,
            "Sender": sender,
            "Receiver": receiver,
            "Amount": amount
        }
        self.transactions = self.transactions.append(new_transaction, ignore_index=True)
        return new_transaction

class NegotiationAgent:
    def negotiate_interest_rate(self, credit_score):
        base_rate = 5
        discount = credit_score // 100
        return max(base_rate - discount, 1)

# Load CSV files
def main():
    st.title("Intelligent Multi-Agent System in Integrated Financial Ecosystem")

    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Home", "Agents Overview", "Transactions", "Simulation"])

    # Load CSVs
    companies_file = "companies.csv"
    transactions_file = "transactions.csv"
    credit_scores_file = "credit_scores.csv"

    companies = load_data(companies_file)
    transactions = load_data(transactions_file)
    credit_scores = load_data(credit_scores_file)

    # Initialize Agents
    credit_agent = CreditScoringAgent(credit_scores)
    transaction_agent = TransactionAgent(transactions)
    negotiation_agent = NegotiationAgent()

    if page == "Home":
        st.header("Overview")
        st.write("This application demonstrates an intelligent multi-agent system used in an integrated financial ecosystem.")
        st.write("""
            Key Features:
            - Collaborative decision-making between financial institutions.
            - Credit scoring using AI.
            - Transaction management via coordinated agents.
        """)

    elif page == "Agents Overview":
        st.header("Agents Overview")
        st.subheader("Companies")
        st.write("List of companies involved in the ecosystem:")
        st.dataframe(companies)

        st.subheader("Credit Scores")
        st.write("Credit scores of individuals and entities:")
        st.dataframe(credit_scores)

    elif page == "Transactions":
        st.header("Transactions")
        st.write("Transactions managed by agents:")
        st.dataframe(transactions)

    elif page == "Simulation":
        st.header("Simulation")

        customer_id = st.text_input("Enter Customer ID", "C001")
        st.write("Fetching data for customer:", customer_id)

        credit_score = credit_agent.get_credit_score(customer_id)

        if credit_score is not None:
            st.write("Credit Score:", credit_score)

            # Simulate Loan Negotiation
            st.subheader("Loan Negotiation")
            amount = st.slider("Loan Amount", 1000, 100000, step=500)
            interest_rate = negotiation_agent.negotiate_interest_rate(credit_score)
            st.write("Proposed Interest Rate:", interest_rate, "%")

            if st.button("Submit Loan Request"):
                transaction = transaction_agent.record_transaction("Customer", "Bank", amount)
                st.success(f"Loan request submitted with interest rate {interest_rate}%")
                st.write("Transaction Details:", transaction)
        else:
            st.error("No data found for the specified customer ID.")

if __name__ == "__main__":
    main()
