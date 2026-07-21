from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional
import uuid
import logging
from backend.tools.mcp_adapter import list_tools, call_tool
from backend.agents.graph import app as agent_graph

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="NexusAI Ops")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    history: List[Dict[str, str]] = []
    deep_think: bool = False
    thread_id: Optional[str] = None
@app.get("/api/tools")
async def get_tools():
    return {"tools": list_tools()}

@app.post("/api/tools/call")
async def execute_tool(name: str, arguments: dict):
    result = await call_tool(name, arguments)
    return {"result": result}
@app.post("/api/chat")
async def chat(request: ChatRequest):
    if not request.message or not request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty.")

    try:
        messages = request.history + [{"role": "user", "content": request.message}]
        thread_id = request.thread_id or str(uuid.uuid4())

        initial_state = {
            "messages": messages,
            "task_plan": [],
            "current_agent": "",
            "retry_count": 0,
            "needs_clarification": False,
            "clarification_question": "",
            "confidence_score": 0,
            "fix_status": "PENDING",
            "deep_think": request.deep_think,
            "trace_log": []
        }

        config = {"configurable": {"thread_id": thread_id}}
        logger.info(f"🚀 [Session: {thread_id}] Processing: {request.message[:60]}...")

        try:
            result = agent_graph.invoke(initial_state, config=config)
        except Exception as e:
            logger.error(f"Graph failed: {e}", exc_info=True)
            return {
                "response": "⚠️ The agent encountered a hiccup. Please try rephrasing your query or toggling 'Fast' mode.",
                "thread_id": thread_id,
                "trace_log": [{"agent": "System", "action": "Fallback triggered", "details": str(e)}],
                "confidence_score": 0,
            }

        ai_response = result.get('messages', [{}])[-1].get('content', "No response generated.")
        trace_log = result.get('trace_log', [])
        confidence_score = result.get('confidence_score', 0)

        return {
            "response": ai_response,
            "thread_id": thread_id,
            "trace_log": trace_log,
            "confidence_score": confidence_score
        }

    except Exception as e:
        logger.error(f"❌ Graph invocation failed: {e}", exc_info=True)
        return {
            "response": "⚠️ The agent encountered an internal error. Please try rephrasing your query.",
            "thread_id": request.thread_id or str(uuid.uuid4()),
            "trace_log": [{"agent": "System", "action": "Error", "details": str(e)}]
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)