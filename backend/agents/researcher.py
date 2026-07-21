import json
from backend.agents.state import AgentState

# Mock Database of Historical Incidents (fallback only)
MOCK_RUNBOOKS = {
    "redis": "Historical Incident #402: Redis timeouts on checkout-service are usually caused by connection pool exhaustion. Fix: Increase max_connections in redis.conf to 500.",
    "database": "Historical Incident #112: Deadlock in user-service. Fix: Add index on user_id column in orders table.",
    "memory": "Historical Incident #88: OOMKilled in api-gateway. Fix: Increase memory limit in k8s deployment to 2Gi."
}

def researcher_node(state: AgentState) -> dict:
    current_task = state['task_plan'][0]['task']
    print(f"🔍 [Researcher] Investigating: '{current_task}'")
    
    # Defaults
    service = "api-gateway"
    logs = "INFO: No critical errors found in the last 15 mins."
    runbook_advice = "No historical incidents found for this specific pattern."

    # ----- DETECTION LOGIC (specific overrides) -----
    if "redis" in current_task.lower() or "checkout" in current_task.lower():
        service = "checkout-service"
        logs = "ERROR [2024-07-17 14:30:01] ConnectionPoolError: Max connections (100) reached."
        runbook_advice = "Historical Incident #402: Increase max_connections to 500 in redis.conf."
    elif "database" in current_task.lower() or "postgres" in current_task.lower() or "deadlock" in current_task.lower():
        service = "user-service"
        logs = "ERROR [2024-07-17 14:30:05] psycopg2.OperationalError: deadlock detected."
        runbook_advice = "Historical Incident #112: Add index on user_id column in orders table."
    elif "oom" in current_task.lower() or "memory" in current_task.lower():
        service = "api-gateway"
        logs = "ERROR [2024-07-17 14:30:10] OOMKilled: Container exceeded memory limit of 512Mi."
        runbook_advice = "Historical Incident #88: Increase memory limit to 2Gi in k8s deployment."
    elif "latency" in current_task.lower() or "slow" in current_task.lower() or "timeout" in current_task.lower():
        service = "checkout-service"
        logs = "WARN [2024-07-17 14:25:00] P99 latency spiked to 12s. Missing index on 'orders.user_id'."
        runbook_advice = "Historical Incident #221: Create index CONCURRENTLY idx_orders_user_id ON orders(user_id);"
    elif "dns" in current_task.lower() or "unknownhost" in current_task.lower():
        service = "payment-service"
        logs = "ERROR [2024-07-17 14:35:12] java.net.UnknownHostException: stripe.api.com. DNS resolution failed."
        runbook_advice = "Historical Incident #503: Check VPC endpoints and route53 private hosted zones."
    elif "ssl" in current_task.lower() or "tls" in current_task.lower() or "certificate" in current_task.lower():
        service = "auth-service"
        logs = "ERROR [2024-07-17 14:40:00] SSL handshake failed: certificate expired. Let's Encrypt renewal failed."
        runbook_advice = "Historical Incident #612: Update certbot to >=2.0 for ACME v2 support."
    elif "s3" in current_task.lower() or "accessdenied" in current_task.lower() or "iam" in current_task.lower():
        service = "data-pipeline"
        logs = "ERROR [2024-07-17 14:45:00] AccessDenied: s3:PutObject on analytics-bucket."
        runbook_advice = "Historical Incident #721: Verify IAM role policy includes s3:PutObject for the bucket."
    elif "kubernetes" in current_task.lower() or "k8s" in current_task.lower() or "deployment" in current_task.lower():
        service = "canary-ai-model"
        logs = "ERROR [2024-07-17 14:50:00] CrashLoopBackOff: ModuleNotFoundError: No module named 'torch'."
        runbook_advice = "Historical Incident #834: Ensure Dockerfile includes 'RUN pip install torch==2.1.0' and uses GPU node selector."
    elif "prometheus" in current_task.lower() or "scrape" in current_task.lower():
        service = "monitoring"
        logs = "ERROR [2024-07-17 14:55:00] Scrape timeout 35s (limit 10s) on kube-state-metrics."
        runbook_advice = "Historical Incident #945: Reduce label cardinality by dropping unnecessary labels like 'pod'."

    # If no detection matched, we keep the defaults, but we also have a fallback to generic MOCK_RUNBOOKS based on keyword
    # (only if runbook_advice is still default and we find a keyword in MOCK_RUNBOOKS)
    if runbook_advice == "No historical incidents found for this specific pattern.":
        for keyword, advice in MOCK_RUNBOOKS.items():
            if keyword in current_task.lower():
                runbook_advice = advice
                break

    observation = f"SYSTEM LOGS:\n{logs}\n\nHISTORICAL RUNBOOK ADVICE:\n{runbook_advice}"
    print("✅ [Researcher] Data gathered successfully.")
    
    return {
        "messages": [{"role": "assistant", "content": observation}],
        "current_agent": "researcher",
        "trace_log": [{"agent": "Researcher", "action": "Fetched logs and runbooks", "details": f"Service: {service}"}]
    }