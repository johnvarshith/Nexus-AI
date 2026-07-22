from backend.agents.state import AgentState
from backend.llm_factory import get_llm
import json
import logging
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CriticAgent:
    def __init__(self):
        self.llm = get_llm(temperature=0.1, max_tokens=250)
    
    def critique(self, state: AgentState) -> dict:
        if not state.get('messages'):
            return {
                "confidence_score": 0,
                "fix_status": "REJECTED",
                "needs_clarification": False,
                "messages": [{"role": "assistant", "content": "Error: No messages found."}]
            }

        original_error = state['messages'][0]['content'] if state['messages'] else "No error."
        
        # Only trigger clarifier if the input is completely empty
        if not original_error or original_error.strip() == "":
            return {
                "confidence_score": 10,
                "fix_status": "PAUSED",
                "needs_clarification": True,
                "clarification_question": "Please provide a detailed description of the issue.",
                "trace_log": [{"agent": "Critic", "action": "Triggered Clarifier (Empty Input)"}]
            }

        coder_output = state['messages'][-1]['content'] if len(state['messages']) > 1 else "No code provided."
        
        # Extract research context
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
            response = self.llm.invoke(prompt)
            content = response.content.strip()
            
            # Extract JSON with regex
            import re
            match = re.search(r'\{.*\}', content, re.DOTALL)
            if not match:
                raise ValueError("No JSON found")
            
            verdict = json.loads(match.group(0))
            status = verdict.get("status", "REJECTED").upper()
            confidence = int(verdict.get("confidence", 50))
            feedback = verdict.get("feedback", "No feedback.")
            
            logger.info(f"⚖️ [Critic] {status} | {confidence}% | {feedback}")
            
            # If confidence is low, trigger clarifier (but this is the LLM's decision)
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