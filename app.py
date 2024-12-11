import streamlit as st
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

# Inisialisasi database
Base = declarative_base()
engine = create_engine('sqlite:///financial_ecosystem.db', echo=True)

# Definisikan tabel-tabel
class Company(Base):
    __tablename__ = 'companies'
    company_id = Column(Integer, primary_key=True)
    company_name = Column(String)
    available_funds = Column(Float)

class Agent(Base):
    __tablename__ = 'agents'
    agent_id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey('companies.company_id'))
    agent_name = Column(String)
    initial_offer = Column(Float)

    company = relationship("Company", back_populates="agents")

Company.agents = relationship("Agent", order_by=Agent.agent_id, back_populates="company")

class Transaction(Base):
    __tablename__ = 'transactions'
    transaction_id = Column(Integer, primary_key=True)
    agent_id = Column(Integer, ForeignKey('agents.agent_id'))
    buyer_fund = Column(Float)
    agreed_price = Column(Float)
    transaction_status = Column(String)

    agent = relationship("Agent", back_populates="transactions")

Agent.transactions = relationship("Transaction", order_by=Transaction.transaction_id, back_populates="agent")

class FundUpdate(Base):
    __tablename__ = 'fund_updates'
    update_id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey('companies.company_id'))
    amount_used = Column(Float)
    new_available_funds = Column(Float)

# Buat tabel jika belum ada
Base.metadata.create_all(engine)

# Inisialisasi sesi untuk query database
Session = sessionmaker(bind=engine)
session = Session()

# Kelas untuk agen negosiasi
class NegotiationAgent:
    def __init__(self, company_name, initial_offer, buyer_fund):
        self.company_name = company_name
        self.initial_offer = initial_offer
        self.buyer_fund = buyer_fund
        self.agreed_price = None

    def negotiate(self):
        if self.initial_offer > self.buyer_fund:
            self.agreed_price = self.buyer_fund
            return f"Negosiasi berhasil dengan {self.company_name}, harga disepakati: {self.agreed_price}"
        else:
            self.agreed_price = self.initial_offer
            return f"Negosiasi berhasil dengan {self.company_name}, harga disepakati: {self.agreed_price}"

# Streamlit UI
def app():
    st.title("Negosiasi Sistem Multiagen Cerdas - Ekosistem Keuangan Terintegrasi")

    st.header("Masukkan Informasi Penawaran dan Dana Pembeli")
    
    # Ambil data perusahaan dari database
    companies = session.query(Company).all()
    company_names = [company.company_name for company in companies]
    company_name = st.selectbox("Pilih Perusahaan Penyedia Layanan", company_names)
    
    # Ambil data agen berdasarkan perusahaan yang dipilih
    company = session.query(Company).filter_by(company_name=company_name).first()
    agents = session.query(Agent).filter_by(company_id=company.company_id).all()
    agent_names = [agent.agent_name for agent in agents]
    agent_name = st.selectbox("Pilih Agen", agent_names)
    
    agent = next(agent for agent in agents if agent.agent_name == agent_name)
    
    # Input harga penawaran dan dana pembeli
    initial_offer = st.number_input(f"Harga Penawaran dari {company_name}:", min_value=1000, max_value=100000, step=100, value=agent.initial_offer)
    buyer_fund = st.number_input("Dana Pembeli:", min_value=1000, max_value=100000, step=100)

    # Inisialisasi agen untuk negosiasi
    negotiation_agent = NegotiationAgent(company_name=company_name, initial_offer=initial_offer, buyer_fund=buyer_fund)
    
    # Menampilkan hasil negosiasi dan pembaruan dana perusahaan
    if st.button('Mulai Negosiasi'):
        negotiation_result = negotiation_agent.negotiate()
        st.write(negotiation_result)

        # Mengupdate dana perusahaan setelah transaksi
        company.available_funds -= negotiation_agent.agreed_price
        session.commit()

        # Tambah transaksi baru
        transaction = Transaction(agent_id=agent.agent_id, buyer_fund=buyer_fund, agreed_price=negotiation_agent.agreed_price, transaction_status="completed")
        session.add(transaction)
        session.commit()

        st.write(f"Sisa dana di {company_name}: {company.available_funds}")

# Menjalankan aplikasi
if __name__ == "__main__":
    app()
