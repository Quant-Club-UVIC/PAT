from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

engine = create_engine(os.environ["DATABASE_URL"],pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=True)