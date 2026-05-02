import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

# postgres_conn_string = os.getenv("POSTGRES_CONN_STR")

# DB_USER = os.getenv("DB_USER", "postgres")
# DB_PASS = os.getenv("DB_PASS", "Admin=2@26$")
# DB_NAME = os.getenv("DB_NAME", "fastapi_db")
# DB_HOST = os.getenv("DB_HOST", "/cloudsql/fastapi-gcp-app:us-central1:free-trial-first-project")

# postgres_conn_string = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@/{DB_NAME}?host={DB_HOST}"
#local to cloud running via cloud sql proxy
# postgres_conn_string = os.getenv(
#     "POSTGRES_CONN_STR",
#     "postgresql+psycopg2://postgres:T:TeVB1I:pPK|t0|@35.222.47.133:5432/fastapi_db"
# )

#cloud running via public ip
postgres_conn_string = os.getenv("DATABASE_URL")
# postgres_conn_string = os.getenv(
#     "POSTGRES_CONN_STR",
#     "postgresql+psycopg2://postgres:T:TeVB1I:pPK|t0|@/fastapi_db?host=/cloudsql/fastapi-gcp-app:us-central1:free-trial-first-project"
# )

if not postgres_conn_string:
    raise ValueError(" POSTGRES_CONN_STR is not set in .env")

print("🔍 Using DB:", postgres_conn_string)  # debug

postgres_engine = create_engine(postgres_conn_string)

PostgresSessionLocal = sessionmaker(
    bind=postgres_engine,
    autocommit=False,
    autoflush=False
)

Base = declarative_base()

def get_db():
    db = PostgresSessionLocal()
    try:
        yield db
    finally:
        db.close()



"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

DB_USER = os.getenv("DB_USER", "fastapi_user")
DB_PASS = os.getenv("DB_PASS", "StrongPassword123")
DB_NAME = os.getenv("DB_NAME", "fastapi_db")
DB_HOST = os.getenv("DB_HOST", "127.0.0.1")  # via Cloud SQL proxy

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()
"""