import httpx
from config import settings
from services import LMSClient

lms = LMSClient()

def start() -> str:
    return (
        "🤖 Welcome to LMS Analytics Bot!\n\n"
        "I can help you track your progress in the course. "
        "Use /help to see what I can do."
    )

def help() -> str:
    return (
        "📋 Available commands:\n\n"
        "/start - Welcome message\n"
        "/help - Show this help\n"
        "/health - Check backend status\n"
        "/labs - List available labs\n"
        "/scores <lab> - Show tasks for a lab\n\n"
        "Examples:\n"
        "/scores lab-01\n"
        "/scores Lab 01\n"
        "/scores Lab 04"
    )

def health() -> str:
    try:
        items = lms.get_items()
        count = len(items)
        if count > 0:
            return f"✅ Backend is healthy. {count} items available."
        else:
            return "⚠️ Backend is reachable but no data found. Try running ETL sync."
    except Exception as e:
        return f"❌ Backend error: {str(e)}"

def labs() -> str:
    try:
        items = lms.get_items()
        
        labs_list = []
        for item in items:
            if item.get("type") == "lab":
                title = item.get("title", "").strip()
                if title:
                    labs_list.append(title)
        
        if not labs_list:
            return "No labs found. Make sure backend has data (run ETL sync)."
        
        labs_list.sort()
        return "📚 Available labs:\n" + "\n".join(f"- {lab}" for lab in labs_list)
    except Exception as e:
        return f"❌ Failed to fetch labs: {str(e)}"

def scores(lab_name: str = "") -> str:
    if not lab_name:
        return "Please specify a lab, e.g., /scores lab-01"
    
    try:
        lab_query = lab_name.strip().lower()
        items = lms.get_items()
        
        # Ищем лабораторную по названию (без regex)
        target_lab = None
        lab_id = None
        
        for item in items:
            if item.get("type") == "lab":
                title = item.get("title", "")
                title_lower = title.lower()
                
                # Проверяем совпадение по разным форматам
                matched = False
                
                # lab-01, lab-02 и т.д.
                if lab_query == "lab-01" or lab_query == "lab 01" or lab_query == "lab1":
                    if "lab-01" in title_lower or "lab 01" in title_lower or "lab1" in title_lower:
                        matched = True
                elif lab_query == "lab-02" or lab_query == "lab 02" or lab_query == "lab2":
                    if "lab-02" in title_lower or "lab 02" in title_lower or "lab2" in title_lower:
                        matched = True
                elif lab_query == "lab-03" or lab_query == "lab 03" or lab_query == "lab3":
                    if "lab-03" in title_lower or "lab 03" in title_lower or "lab3" in title_lower:
                        matched = True
                elif lab_query == "lab-04" or lab_query == "lab 04" or lab_query == "lab4":
                    if "lab-04" in title_lower or "lab 04" in title_lower or "lab4" in title_lower:
                        matched = True
                elif lab_query == "lab-05" or lab_query == "lab 05" or lab_query == "lab5":
                    if "lab-05" in title_lower or "lab 05" in title_lower or "lab5" in title_lower:
                        matched = True
                elif lab_query == "lab-06" or lab_query == "lab 06" or lab_query == "lab6":
                    if "lab-06" in title_lower or "lab 06" in title_lower or "lab6" in title_lower:
                        matched = True
                elif lab_query == "lab-07" or lab_query == "lab 07" or lab_query == "lab7":
                    if "lab-07" in title_lower or "lab 07" in title_lower or "lab7" in title_lower:
                        matched = True
                else:
                    # Общее совпадение по вхождению
                    if lab_query in title_lower or title_lower.startswith(lab_query):
                        matched = True
                
                if matched:
                    target_lab = item
                    lab_id = item.get("id")
                    break
        
        if not target_lab:
            available = [item.get("title") for item in items if item.get("type") == "lab"]
            return f"Lab '{lab_name}' not found. Available labs:\n" + "\n".join(f"- {lab}" for lab in available[:10])
        
        # Ищем задачи, относящиеся к этой лабораторной
        tasks = [item for item in items if item.get("parent_id") == lab_id]
        
        if not tasks:
            return f"No tasks found for {target_lab.get('title')}."
        
        result = f"📊 Tasks for {target_lab.get('title')}:\n\n"
        for task in tasks:
            task_title = task.get("title", "Unnamed task")
            result += f"• {task_title}\n"
        
        return result
    except Exception as e:
        return f"❌ Failed to fetch scores: {str(e)}"
