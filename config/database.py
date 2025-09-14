# config/database.py - SQL Server Configuration
import os
import urllib.parse
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

# SQL Server Configuration
SQL_SERVER = os.getenv("SQL_SERVER", "localhost")
SQL_INSTANCE = os.getenv("SQL_INSTANCE", "SQLEXPRESS") 
SQL_DATABASE = os.getenv("SQL_DATABASE", "agentic_pipeline_monitor")
SQL_USERNAME = os.getenv("SQL_USERNAME", "")
SQL_PASSWORD = os.getenv("SQL_PASSWORD", "")
SQL_PORT = os.getenv("SQL_PORT", "1433")

def get_connection_string():
    """Generate SQL Server connection string"""
    
    if SQL_USERNAME and SQL_PASSWORD:
        # SQL Server Authentication
        server_name = f"{SQL_SERVER}\\{SQL_INSTANCE},{SQL_PORT}" if SQL_INSTANCE else f"{SQL_SERVER},{SQL_PORT}"
        connection_string = f"mssql+pyodbc://{SQL_USERNAME}:{urllib.parse.quote_plus(SQL_PASSWORD)}@{server_name}/{SQL_DATABASE}?driver=ODBC+Driver+17+for+SQL+Server"
    else:
        # Windows Authentication (most common for local development)
        server_name = f"{SQL_SERVER}\\{SQL_INSTANCE}" if SQL_INSTANCE else SQL_SERVER
        connection_string = f"mssql+pyodbc://@{server_name}/{SQL_DATABASE}?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
    
    return connection_string

# Create connection string
SQL_URL = get_connection_string()

# SQLAlchemy setup
engine = create_engine(SQL_URL, echo=False, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def test_connection():
    """Test SQL Server connection"""
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1 as test")).fetchone()
            if result and result[0] == 1:
                print("✅ SQL Server connection successful")
                
                # Test database access
                tables_result = connection.execute(text("""
                    SELECT TABLE_NAME 
                    FROM INFORMATION_SCHEMA.TABLES 
                    WHERE TABLE_TYPE = 'BASE TABLE'
                """)).fetchall()
                
                print(f"📊 Found {len(tables_result)} tables in database")
                for table in tables_result:
                    print(f"  • {table[0]}")
                
                return True
    except Exception as e:
        print(f"❌ SQL Server connection failed: {e}")
        print(f"Connection string: {SQL_URL.replace(SQL_PASSWORD, '***') if SQL_PASSWORD else SQL_URL}")
        return False

def get_table_count(table_name):
    """Get count of records in a table"""
    try:
        with engine.connect() as connection:
            result = connection.execute(text(f"SELECT COUNT(*) FROM {table_name}")).fetchone()
            return result[0] if result else 0
    except Exception as e:
        print(f"Error getting count for {table_name}: {e}")
        return 0

if __name__ == "__main__":
    print("🔍 Testing SQL Server connection...")
    test_connection()