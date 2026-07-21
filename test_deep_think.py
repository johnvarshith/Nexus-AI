import requests
import time

API_URL = "http://localhost:8000/api/chat"
QUERY = "checkout-service is throwing ConnectionPoolError max connections reached"

def test_mode(deep_think: bool):
    print(f"\n{'='*60}")
    print(f"🚀 Testing with deep_think = {deep_think}")
    start = time.time()
    
    try:
        resp = requests.post(API_URL, json={
            "message": QUERY,
            "deep_think": deep_think
        }, timeout=120)
        elapsed = time.time() - start
        data = resp.json()
        
        print(f"✅ Status: {resp.status_code}")
        print(f"⏱️  Latency: {elapsed:.2f}s")
        print(f"📝 Response snippet: {data.get('response', '')[:150]}...")
        print(f"📊 Confidence: {data.get('confidence_score', 'N/A')}%")
        print(f"🔗 Thread ID: {data.get('thread_id', 'N/A')}")
        print(f"📋 Trace log entries: {len(data.get('trace_log', []))}")
        return elapsed
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

if __name__ == "__main__":
    print("🧠 Deep Think Mode Test")
    print("="*60)
    print("Make sure your backend is running (python -m backend.main)")
    print("Watch the backend terminal to see which model loads.\n")
    
    # Fast mode first
    t_fast = test_mode(deep_think=False)
    # Deep mode second
    t_deep = test_mode(deep_think=True)
    
    if t_fast and t_deep:
        print("\n" + "="*60)
        print("📊 Comparison:")
        print(f"Fast mode latency : {t_fast:.2f}s")
        print(f"Deep mode latency : {t_deep:.2f}s")
        print(f"Speedup: {t_deep/t_fast:.2f}x slower in Deep mode (expected)")
        print("\n💡 Check your backend terminal now – you should see:")
        print("   - Fast mode: qwen2.5:3b")
        print("   - Deep mode: phi3:3.8b")