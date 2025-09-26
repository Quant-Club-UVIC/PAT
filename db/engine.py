from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base

db_url="postgresql+psycopg://admin:admin@localhost:5432/pat"

engine = create_engine(db_url)

Base=declarative_base()
Base.metadata.create_all(engine)