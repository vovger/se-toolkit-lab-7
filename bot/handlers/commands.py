import httpx
from config import settings

def start() -> str:
    return "Welcome to LMS Bot! Use /help to see available commands."

def help() -> str:
    return (
        "/start - Welcome message\n"
        "/help - Show this help\n"
        "/health - Check backend status\n"
        "/labs - List available labs\n"
        "/scores <lab> - Get scores for a lab"
    )

def health() -> str:
    try:
        resp = httpx.get(
            f"{settings.lms_api_base_url}/health",
            headers={"api-key": settings.lms_api_key},
            timeout=5.0,
        )
        if resp.status_code == 200:
            return f"Backend is OK: {resp.text}"
        return f"Backend returned status {resp.status_code}"
    except Exception as e:
        return f"Error connecting to backend: {e}"

def labs() -> str:
    try:
        resp = httpx.get(
            f"{settings.lms_api_base_url}/items/",
            headers={"api-key": settings.lms_api_key},
            timeout=5.0,
        )
        if resp.status_code == 200:
            items = resp.json()
            labs = list(set(item.get("lab_name", "unknown") for item in items))
            return "Available labs:\n" + "\n".join(labs[:10])
        return f"Failed to fetch labs: {resp.status_code}"
    except Exception as e:
        return f"Error: {e}"

def scores(lab_name: str = "") -> str:
    if not lab_name:
        return "Please specify a lab, e.g., /scores lab-04"
    try:
        resp = httpx.get(
            f"{settings.lms_api_base_url}/items/",
            headers={"api-key": settings.lms_api_key},
            timeout=5.0,
        )
        if resp.status_code == 200:
            items = resp.json()
            lab_items = [i for i in items if i.get("lab_name") == lab_name]
            if not lab_items:
                return f"No data found for lab {lab_name}"
            total_score = sum(i.get("score", 0) for i in lab_items)
            count = len(lab_items)
            avg = total_score / count if count else 0
            return f"Lab {lab_name}: {count} submissions, average score {avg:.2f}"
        return f"Failed to fetch scores: {resp.status_code}"
    except Exception as e:
        return f"Error: {e}"
