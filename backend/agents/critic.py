from backend.agents.state import AgentState
from backend.llm_factory import get_llm
import json
import logging
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CriticAgent:
    def __init__(self):
        pass
    
    def critique(self, state: AgentState) -> dict:
        if not state.get('messages'):
            return {
                "confidence_score": 0,
                "fix_status": "REJECTED",
                "needs_clarification": False,
                "messages": [{"role": "assistant", "content": "Error: No messages found."}]
            }

        original_error = str(state['messages'][0].get('content', 'No error.')) if state['messages'] else "No error."
        word_count = len(original_error.split())
        # Heuristic to detect vague inputs before running the LLM
        vague_signals = ["broken", "not working", "server down", "something", "wrong", "issue", "problem", "isn't", "wasn't"]
        technical_keywords = ["error", "exception", "timeout", "deadlock", "oom", "crash", "fail", "denied", "expired",
                              "null", "index", "connection", "pool", "ssl", "tls", "dns", "kafka", "lag", "s3", "iam",
                              "role", "deployment", "pod", "container", "prometheus", "scrape", "metric", "latency", "slow"]

        is_vague = any(kw in original_error.lower() for kw in vague_signals)
        has_tech = any(kw in original_error.lower() for kw in technical_keywords)
        if word_count <= 6 or (is_vague and not has_tech):
            print(f"🛑 [Critic] Vague input ({word_count} words). Triggering Clarifier.")
            return {
                "confidence_score": 10,
                "fix_status": "PAUSED",
                "needs_clarification": True,
                "clarification_question": "The input is too vague. Could you provide specific error logs, service names, or stack traces?",
                "trace_log": [{"agent": "Critic", "action": "Triggered Clarifier (Vague Input)", "details": "Insufficient context to provide a fix"}]
            }

        coder_output = str(state['messages'][-1].get('content', 'No code provided.')) if len(state['messages']) > 1 else "No code provided."
        
        # Extract research context if available
        research_context = "No research findings."
        for msg in state['messages']:
            if "SYSTEM LOGS:" in msg['content']:
                research_context = msg['content']
                break

        prompt = f"""You are a Senior Staff SRE reviewing a code fix.

ORIGINAL INCIDENT:
{original_error}

RESEARCHER FINDINGS:
{research_context}

PROPOSED CODE FIX:
{coder_output}

Evaluate the fix. Does it definitively solve the exact error?
Output ONLY a valid JSON object (no markdown):
{{
    "status": "APPROVED" or "REJECTED",
    "confidence": <integer 0-100>,
    "feedback": "<1 sentence why>"
}}"""

        try:
            llm = get_llm(temperature=0.1, max_tokens=250)
            response = llm.invoke(prompt)
            content = response.content.strip()
            
            # Extract JSON with regex
            match = re.search(r'\{.*\}', content, re.DOTALL)
            if not match:
                raise ValueError("No JSON found")
            
            verdict = json.loads(match.group(0))
            status = verdict.get("status", "REJECTED").upper()
            confidence = int(verdict.get("confidence", 50))
            feedback = verdict.get("feedback", "No feedback.")
            
            logger.info(f"⚖️ [Critic] {status} | {confidence}% | {feedback}")
            
            if confidence < 60:
                return {
                    "confidence_score": confidence,
                    "fix_status": "PAUSED",
                    "needs_clarification": True,
                    "clarification_question": f"I'm not confident ({confidence}%). {feedback} Can you provide more logs?",
                    "trace_log": [{"agent": "Critic", "action": "Triggered Clarifier (Low Confidence)", "details": feedback}]
                }
            
            if status == "REJECTED":
                return {
                    "confidence_score": confidence,
                    "fix_status": "REJECTED",
                    "needs_clarification": False,
                    "messages": [{"role": "assistant", "content": f"CRITIC FEEDBACK: {feedback}"}],
                    "trace_log": [{"agent": "Critic", "action": "Rejected", "details": feedback}]
                }
            
            # APPROVED
            return {
                "confidence_score": confidence,
                "fix_status": "APPROVED",
                "needs_clarification": False,
                "trace_log": [{"agent": "Critic", "action": f"Approved with {confidence}%", "details": feedback}]
            }
            
        except Exception as e:
            logger.error(f"[Critic] Parsing failed: {e}")
            # Fallback: reject and let the graph retry or go to clarifier
            return {
                "confidence_score": 0,
                "fix_status": "REJECTED",
                "needs_clarification": True,
                "clarification_question": "The review system encountered an error. Please try rephrasing your query.",
                "trace_log": [{"agent": "Critic", "action": "Error", "details": str(e)}]
            }