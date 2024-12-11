import streamlit as st
import pandas as pd

# Load Data
@st.cache
def load_data(file_path):
    return pd.read_csv(file_path)

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

        # Filter data
        customer_data = credit_scores[credit_scores['CustomerID'] == customer_id]

        if not customer_data.empty:
            st.write("Credit Score:", customer_data['CreditScore'].values[0])

            # Simulate Loan Negotiation
            st.subheader("Loan Negotiation")
            amount = st.slider("Loan Amount", 1000, 100000, step=500)
            credit_score = customer_data['CreditScore'].values[0]

            # Calculate interest rate based on credit score
            interest_rate = max(5 - (credit_score // 100), 1)
            st.write("Proposed Interest Rate:", interest_rate, "%")

            if st.button("Submit Loan Request"):
                st.success("Loan request submitted with interest rate {}%".format(interest_rate))
        else:
            st.error("No data found for the specified customer ID.")

if __name__ == "__main__":
    main()
