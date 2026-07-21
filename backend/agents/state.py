from typing import TypedDict, Annotated, List, Dict
import operator

class Message(TypedDict):
    role: str
    content: str

class Task(TypedDict):
    task: str
    agent: str

class AgentState(TypedDict):
    messages: Annotated[List[Message], operator.add]
    task_plan: List[Task]
    current_agent: str
    confidence_score: int
    fix_status: str
    needs_clarification: bool
    clarification_question: str
    retry_count: int
    deep_think: bool
    trace_log: Annotated[List[Dict], operator.add]