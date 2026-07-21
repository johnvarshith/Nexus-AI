import requests

url = "http://localhost:8000/api/chat"

print("🚀 Testing REAL Agentic Tools (Web Search + Code)...\n")

# A query that requires LIVE data (the AI's training data is cut off, so it MUST search)
payload = {
    "message": "What is the current stock price of NVIDIA (NVDA), and write a python script to calculate a 10% increase on that price?",
    "history": []
}

print("Sending query to NexusAI...")
response = requests.post(url, json=payload).json()

print("\n✅ Final AI Response:")
print("-" * 60)
print(response['response'])
print("-" * 60)