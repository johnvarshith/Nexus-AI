import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# Load environment variables
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

print("🔌 Testing Database Connection...\n")

try:
    # 1. Test Connection
    engine = create_engine(DATABASE_URL)
    with engine.connect() as conn:
        # "SELECT 1" works on BOTH SQLite and PostgreSQL
        result = conn.execute(text("SELECT 1"))
        print("✅ SUCCESS! Connected to database.")
        
    # 2. Test Table Creation
    print("🏗️ Initializing database tables...")
    from backend.models.database import init_db
    init_db()
    
    print("🎉 All database tests passed! Ready for Phase 4.")

except Exception as e:
    print(f"\n❌ FAILED to connect.")
    print(f"Error details: {e}")
    print("\n👉 Please check your DATABASE_URL in the .env file.")