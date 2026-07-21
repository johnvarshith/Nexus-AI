import requests
import time
import uuid

API_URL = "http://localhost:8000/api/chat"

# Synthetic test cases with expected keyword lists (using your improved ANY logic)
TEST_CASES = [
    {
        "name": "Cascading OOM (Memory Leak)",
        "input": "api-gateway and auth-service both crashing with OOMKilled every 2 hours. Heap dump shows 'io.netty.buffer.PoolArena' objects consuming 90% of 1Gi limit. Traffic is up 30% due to Black Friday sale.",
        "expected_keywords": ["memory", "heap", "netty", "limit"]
    },
    {
        "name": "Database Deadlock in Monolith",
        "input": "Orders API failing with 'ERROR: deadlock detected (Process 1424 waits for ShareLock on transaction 8734; blocked by process 1424)' during high concurrent checkout. Tables involved: 'inventory' and 'order_items'. No indexes on foreign keys.",
        "expected_keywords": ["deadlock", "index", "foreign", "concurrent"]
    },
    {
        "name": "DNS Outage + Timeouts",
        "input": "Payment service is throwing 'java.net.UnknownHostException: stripe.api.com' and timing out after 5 retries. ECS service discovery is healthy, but internal VPC endpoints are showing 'Request timed out' for external APIs.",
        "expected_keywords": ["dns", "host", "timeout", "resolve"]
    },
    {
        "name": "Kafka Consumer Lag Spike",
        "input": "Alert: 'order-processing' consumer group lag has spiked to 50,000 messages in the last 15 minutes. Brokers are showing high disk I/O. Processing time per message went from 200ms to 4.2s due to a new JSON serialization library.",
        "expected_keywords": ["kafka", "lag", "consumer", "serialization"]
    },
    {
        "name": "TLS Certificate Expiry",
        "input": "Mobile app users are getting 'SSL handshake failed' and 'certificate expired' errors on the authentication endpoint. Cert is issued by Let's Encrypt and expires in 2 days. Auto-renewal cron job failed due to ACME v2 endpoint deprecation.",
        "expected_keywords": ["certificate", "ssl", "expired", "renewal"]
    },
    {
        "name": "Slow SQL + Connection Pool Exhaustion",
        "input": "Checkout API is hanging. 'SELECT * FROM orders WHERE status='PENDING' AND created_at > NOW() - INTERVAL '1 day'' query is taking 45s. HikariCP is reporting 'Connection is not available, request timed out after 30000ms'. Active connections: 100/100.",
        "expected_keywords": ["connection", "pool", "timeout", "sql", "index"]
    },
    {
        "name": "S3 Access Denied (IAM Role Rotation)",
        "input": "Data pipeline is failing with 'Error: AccessDenied (403) when uploading parquet files to s3://analytics-bucket/'. IAM role 'data-processor-role' was rotated last night. CloudTrail logs show 'assume-role' succeeded but 's3:PutObject' denied.",
        "expected_keywords": ["s3", "access", "denied", "iam", "role"]
    },
    {
        "name": "Kubernetes CrashLoopBackOff (Wrong Image)",
        "input": "Deployment 'canary-ai-model' stuck in CrashLoopBackOff. Logs show 'ModuleNotFoundError: No module named 'torch''. Dockerfile uses 'python:3.9-slim' but requirements.txt needs torch==2.1.0. GPU node pool is available.",
        "expected_keywords": ["deployment", "crash", "module", "dockerfile"]
    },
    {
        "name": "Vague / Missing Context (Must trigger Clarifier)",
        "input": "The production app is down. Users are calling. Please fix ASAP.",
        "expected_keywords": ["clarification", "details", "logs", "specific"]
    },
    {
        "name": "Prometheus Scrape Timeout",
        "input": "Prometheus is dropping targets. Scrape of 'kube-state-metrics' service is taking 35s and timing out (config: 10s). It's pulling 5000+ metrics. Need to reduce cardinality of labels like 'job', 'namespace', and 'pod'.",
        "expected_keywords": ["prometheus", "scrape", "timeout", "cardinality", "metrics"]
    }
]
def run_evaluation():
    print("🚀 Starting NexusAI Ops Automated Evaluation Suite...\n")
    print("-" * 60)
    
    passed = 0
    total = len(TEST_CASES)

    for i, test in enumerate(TEST_CASES, 1):
        print(f"Test {i}: {test['name']}")
        print(f"Input: '{test['input']}'")
        
        # 🟢 Fresh state for each test – no history, no thread_id
        payload = {
            "message": test['input'],
            "deep_think": False,
            "history": []   # empty history
        }
        # No thread_id sent – backend generates a new one
        
        start_time = time.time()
        try:
            response = requests.post(API_URL, json=payload, timeout=120)
            latency = time.time() - start_time
            
            if response.status_code != 200:
                print(f"❌ FAIL: HTTP {response.status_code} - {response.text[:100]}")
                print("-" * 60)
                continue
            
            data = response.json()
            output = data.get('response', '').lower()
            
            keywords = test.get('expected_keywords', [])
            matched = any(kw.lower() in output for kw in keywords)
            
            if matched:
                print(f"✅ PASS (Latency: {latency:.2f}s)")
                passed += 1
            else:
                print(f"❌ FAIL: Expected any of {keywords} not found.")
                print(f"   Output snippet: {output[:150]}...")
                
        except requests.exceptions.Timeout:
            print(f"❌ ERROR: Request timed out after 120s.")
        except requests.exceptions.ConnectionError:
            print(f"❌ ERROR: Cannot connect to {API_URL}. Is the server running?")
        except Exception as e:
            print(f"❌ ERROR: {e}")
        
        print("-" * 60)

    accuracy = (passed / total) * 100 if total > 0 else 0
    print(f"\n📊 FINAL RESULTS:")
    print(f"Passed: {passed}/{total}")
    print(f"Accuracy: {accuracy:.1f}%")
    print("✅ Evaluation Complete. Add these metrics to your portfolio README!")

if __name__ == "__main__":
    run_evaluation()