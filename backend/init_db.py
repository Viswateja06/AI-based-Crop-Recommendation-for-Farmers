import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# 1. Connect to the default postgres database first to create the new one
DEFAULT_DB_URL = "postgresql://postgres:postgres@localhost:5432/postgres"

print("Connecting to PostgreSQL...")
try:
    # We must use isolation_level="AUTOCOMMIT" to run CREATE DATABASE
    engine = create_engine(DEFAULT_DB_URL, isolation_level="AUTOCOMMIT")
    with engine.connect() as conn:
        print("Creating 'agridb' database if it doesn't exist...")
        # Check if DB exists
        result = conn.execute(text("SELECT 1 FROM pg_database WHERE datname='agridb'"))
        if not result.fetchone():
            conn.execute(text("CREATE DATABASE agridb"))
            print("Database 'agridb' created successfully!")
        else:
            print("Database 'agridb' already exists.")
except Exception as e:
    print(f"Error creating database: {e}")
    print("Please make sure PostgreSQL is installed, running, and accessible with user 'postgres' and password 'postgres'.")
    exit(1)

# 2. Now connect to the new agridb and create all the tables from our models
print("Connecting to 'agridb' to create tables...")
try:
    from app.database import Base
    from app.models import User, QueryLog # Import models so Base metadata registers them
    
    AGRIDB_URL = "postgresql://postgres:postgres@localhost:5432/agridb"
    agri_engine = create_engine(AGRIDB_URL)
    
    # This will create all tables defined in models that inherit from Base
    Base.metadata.create_all(bind=agri_engine)
    print("All database tables created successfully!")
    
except Exception as e:
    print(f"Error creating tables: {e}")
