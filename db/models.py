from sqlalchemy.sql import func
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Table, Column, Integer, String, Numeric, BigInteger, DOUBLE_PRECISION, DateTime, ForeignKey, CheckConstraint

Base = declarative_base()

# association table
company_etf_association = Table('company_etf_association', Base.metadata,
                                Column('company_id', ForeignKey('companies.company_id'), primary_key=True),
                                Column('etf_id', ForeignKey('etfs.etf_id'), primary_key=True)
                                )

class Company(Base):
    __tablename__ = "companies"
    company_id = Column(Integer, primary_key=True)
    ticker     = Column(String)
    name       = Column(String)
    sector     = Column(String)
    industry   = Column(String)

    etfs = relationship("ETF", secondary=company_etf_association, back_populates="companies")
    stock = relationship("Stock", back_populates="company", uselist=False)
    financial_statement = relationship("FinancialStatement", back_populates="company", uselist=False)
    corp_actions = relationship("CorpAction", back_populates="company")
    financial_metrics = relationship("FinancialMetric", back_populates="company")

class ETF(Base):
    __tablename__ = "etfs"
    etf_id=Column(Integer,primary_key=True)
    ticker=Column(String)
    name=Column(String)

    companies = relationship("Company", secondary=company_etf_association, back_populates="etfs")
    stock = relationship("Stock", back_populates="etf", uselist=False)

class CorpAction(Base):
    __tablename__="corp_actions"
    action_id=Column(Integer,primary_key=True)
    company_id=Column(Integer,ForeignKey("companies.company_id"),nullable=False)
    action_date=Column(DateTime(timezone=True),server_default=func.now())
    action_type=Column(String)
    value = Column(Numeric)
    detail=Column(String)

    company = relationship("Company", back_populates="corp_actions")

class Stock(Base):
    __tablename__="stocks"
    price_id=Column(Integer,primary_key=True)
    company_id=Column(Integer,ForeignKey("companies.company_id"), nullable=True,unique=True)
    etf_id=Column(Integer,ForeignKey("etfs.etf_id"), nullable=True, unique=True)
    
    price_timestamp=Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    open_price=Column(DOUBLE_PRECISION)
    high_price=Column(DOUBLE_PRECISION)
    low_price=Column(DOUBLE_PRECISION)
    close_price=Column(DOUBLE_PRECISION)
    volume=Column(BigInteger)

    company = relationship("Company", back_populates="stock")
    etf = relationship("ETF", back_populates="stock")

    __table_args__ = (
        CheckConstraint(
            "(company_id IS NOT NULL AND etf_id IS NULL) OR "
            "(company_id IS NULL AND etf_id IS NOT NULL)",
            name="ck_stock_exactly_one_owner",
        ),
    )

class FinancialStatement(Base):
    __tablename__="financial_statements"
    statement_id=Column(Integer,primary_key=True)
    company_id=Column(Integer,ForeignKey("companies.company_id"),nullable=False,unique=True)
    statement_type=Column(String)
    period_type=Column(String)
    fiscal_year=Column(Integer)
    statement_date=Column(DateTime(timezone=True),server_default=func.now())

    company = relationship("Company", back_populates="financial_statement")
    metrics = relationship("FinancialMetric", back_populates="statement")
    

class FinancialMetric(Base):
    __tablename__="financial_metrics"
    metric_id=Column(Integer, primary_key=True)
    statement_id=Column(Integer, ForeignKey("financial_statements.statement_id"), nullable=False)
    company_id=Column(Integer, ForeignKey("companies.company_id"), nullable=False)
    metric_name=Column(String)
    metric_value=Column(Numeric)

    company = relationship("Company", back_populates="financial_metrics")
    statement = relationship("FinancialStatement", back_populates="metrics")

