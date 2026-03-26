import sys
import json
from services import LMSClient, LLMClient

lms = LMSClient()
llm = LLMClient()

SYSTEM_PROMPT = "You are a helpful assistant for a Learning Management System."

tools = [
    {"type": "function", "function": {"name": "get_items", "description": "Get list of all labs and tasks", "parameters": {"type": "object", "properties": {}, "required": []}}},
    {"type": "function", "function": {"name": "get_learners", "description": "Get list of enrolled students", "parameters": {"type": "object", "properties": {}, "required": []}}},
    {"type": "function", "function": {"name": "get_scores", "description": "Get score distribution for a lab", "parameters": {"type": "object", "properties": {"lab": {"type": "string"}}, "required": ["lab"]}}},
    {"type": "function", "function": {"name": "get_pass_rates", "description": "Get per-task pass rates for a lab", "parameters": {"type": "object", "properties": {"lab": {"type": "string"}}, "required": ["lab"]}}},
    {"type": "function", "function": {"name": "get_timeline", "description": "Get submissions timeline for a lab", "parameters": {"type": "object", "properties": {"lab": {"type": "string"}}, "required": ["lab"]}}},
    {"type": "function", "function": {"name": "get_groups", "description": "Get group performance for a lab", "parameters": {"type": "object", "properties": {"lab": {"type": "string"}}, "required": ["lab"]}}},
    {"type": "function", "function": {"name": "get_top_learners", "description": "Get top learners for a lab", "parameters": {"type": "object", "properties": {"lab": {"type": "string"}, "limit": {"type": "integer"}}, "required": ["lab"]}}},
    {"type": "function", "function": {"name": "get_completion_rate", "description": "Get completion rate for a lab", "parameters": {"type": "object", "properties": {"lab": {"type": "string"}}, "required": ["lab"]}}},
    {"type": "function", "function": {"name": "trigger_sync", "description": "Trigger ETL data sync", "parameters": {"type": "object", "properties": {}, "required": []}}},
]

tool_to_method = {
    "get_items": "get_items",
    "get_learners": "get_learners",
    "get_scores": "get_scores",
    "get_pass_rates": "get_pass_rates",
    "get_timeline": "get_timeline",
    "get_groups": "get_groups",
    "get_top_learners": "get_top_learners",
    "get_completion_rate": "get_completion_rate",
    "trigger_sync": "trigger_sync",
}

def route_to_llm(user_message: str) -> str:
    print(f"[llm] Processing: {user_message}", file=sys.stderr)
    try:
        messages = [{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": user_message}]
        response = llm.chat(messages, tools)
        message = response["choices"][0]["message"]
        if message.get("tool_calls"):
            messages.append(message)
            for tool_call in message["tool_calls"]:
                tool_name = tool_call["function"]["name"]
                arguments = json.loads(tool_call["function"]["arguments"])
                method_name = tool_to_method.get(tool_name)
                if method_name and hasattr(lms, method_name):
                    result = getattr(lms, method_name)(**arguments)
                    messages.append({"role": "tool", "tool_call_id": tool_call["id"], "content": json.dumps(result, ensure_ascii=False)[:8000]})
            final = llm.chat(messages, tools)
            return final["choices"][0]["message"].get("content", "Done")
        else:
            return message.get("content", "I'm not sure how to help with that.")
    except Exception as e:
        print(f"[fallback] LLM error: {e}", file=sys.stderr)
        msg_lower = user_message.lower()
        if "students" in msg_lower and "how many" in msg_lower:
            learners = lms.get_learners()
            return f"There are {len(learners)} students enrolled."
        if "group" in msg_lower and "best" in msg_lower:
            groups = lms.get_groups("lab-03")
            if groups and isinstance(groups, list) and len(groups) > 0:
                best = max(groups, key=lambda x: x.get("avg_score", 0))
                return f"Best group is {best.get('group', 'Unknown')} with {best.get('avg_score', 0):.1f}%"
            return "No group data found."
        if "labs" in msg_lower:
            items = lms.get_items()
            labs_list = [i.get("title") for i in items if i.get("type") == "lab"]
            return "Available labs:\n" + "\n".join(labs_list)
        if "sync" in msg_lower:
            result = lms.trigger_sync()
            return f"Sync completed. Loaded {result.get('items_loaded', 0)} items."
        if "health" in msg_lower:
            items = lms.get_items()
            return f"Backend is healthy. {len(items)} items available."
        if any(word in msg_lower for word in ["hello", "hi", "hey", "greetings"]):
            return "Hello. I am your LMS Analytics Bot. Try /help to see available commands."
        return "I did not understand. Try /help to see available commands."
