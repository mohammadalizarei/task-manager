from datetime import datetime

def get_today_date() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

get_today_date_schema = {
    "type": "function",
    "name": "get_today_date",
    "description": "Returns the current date and time in YYYY-MM-DD HH:MM:SS format.",
    "parameters": {
        "type": "object",
        "properties": {},
        "required": [],
        "additionalProperties": False
    },
    "strict": True
}