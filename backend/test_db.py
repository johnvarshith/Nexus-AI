# test_db.py
import psycopg2
import sys

def test_connection():
    try:
        # Connect using the same credentials as your docker-compose.yml
        conn = psycopg2.connect(
            host="localhost",       # Postgres is on your host machine
            port="5432",
            database="nexusai_db",  # The database name we hardcoded
            user="nexusai",
            password="varshtih2004"
        )
        cur = conn.cursor()
        
        # Execute a simple query
        cur.execute("SELECT version();")
        version = cur.fetchone()
        print("✅ Database connection successful!")
        print(f"📦 PostgreSQL Version: {version[0][:30]}...")  # Print first 30 chars
        
        cur.close()
        conn.close()
        return True
        
    except psycopg2.OperationalError as e:
        print(f"❌ Connection failed: {e}")
        print("\n💡 Troubleshooting tips:")
        print("  1. Is the container running? Run: docker ps")
        print("  2. Did you start the container? Run: docker-compose up -d")
        print("  3. Try restarting the container: docker-compose restart postgres")
        return False
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    test_connection()