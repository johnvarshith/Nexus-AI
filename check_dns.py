import socket

# Replace this with the exact host part of your DATABASE_URL
# Example: "aws-0-ap-south-1.pooler.supabase.com" or "db.jpbxwubymlaovnfiglij.supabase.co"
host_to_check = "db.jpbxwubymlaovnfiglij.supabase.co" 

try:
    ip = socket.gethostbyname(host_to_check)
    print(f"✅ SUCCESS: {host_to_check} resolves to {ip}")
except socket.gaierror:
    print(f"❌ FAILED: Cannot resolve {host_to_check}")
    print("👉 The Project ID in your URL is likely incorrect or the project is paused.")