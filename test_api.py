import requests

url = "http://localhost:8000/api/chat"

print("🤖 Step 1: Introducing myself to the AI...\n")
payload1 = {
    "message": "My name is Varshith and I am an AI engineer.",
    "history": []
}

response1 = requests.post(url, json=payload1).json()
print("AI Response:", response1['response'])
print("-" * 50)

print("\n🧠 Step 2: Asking the AI to remember...\n")
payload2 = {
    "message": "What is my name and what do I do?",
    "history": response1['history']  # <-- We pass the history from Step 1!
}

response2 = requests.post(url, json=payload2).json()
print("AI Response:", response2['response'])
print("-" * 50)