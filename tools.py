import json
import os
import uuid
from datetime import datetime, timedelta
from typing import Optional

DB_FILE = "database.json"

def get_today_date() -> str:
    return datetime.now().strftime("%Y-%m-%d")

get_today_date_schema = {
    "type": "function",
    "name": "get_today_date",
    "description": "Returns the current date in YYYY-MM-DD format.",
    "parameters": {
        "type": "object",
        "properties": {},
        "required": [],
        "additionalProperties": False
    },
    "strict": True
}

def get_future_date(days: int) -> str:
    target_date = datetime.now() + timedelta(days=days)
    return target_date.strftime("%Y-%m-%d")

get_future_date_schema = {
    "type": "function",
    "name": "get_future_date",
    "description": "Calculates and returns the date after a given number of days from today in YYYY-MM-DD format.",
    "parameters": {
        "type": "object",
        "properties": {
            "days": {
                "type": "integer",
                "description": "The number of days to add to the current date."
            }
        },
        "required": ["days"],
        "additionalProperties": False
    },
    "strict": True
}

def get_items(date: Optional[str] = None, item_type: Optional[str] = None) -> str:
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []
    else:
        data = []

    if date:
        day_entry = next((item for item in data if item["date"] == date), None)
        if not day_entry:
            if item_type:
                return json.dumps([], ensure_ascii=False)
            return json.dumps({"date": date, "tasks": [], "events": [], "meetings": []}, ensure_ascii=False)

        if item_type in ["tasks", "events", "meetings"]:
            return json.dumps(day_entry.get(item_type, []), ensure_ascii=False)

        return json.dumps(day_entry, ensure_ascii=False)

    if item_type in ["tasks", "events", "meetings"]:
        filtered_data = [
            {"date": item["date"], item_type: item.get(item_type, [])}
            for item in data
            if item.get(item_type)
        ]
        return json.dumps(filtered_data, ensure_ascii=False)

    return json.dumps(data, ensure_ascii=False)

get_items_schema = {
    "type": "function",
    "name": "get_items",
    "description": "Retrieves tasks, events, or meetings. Filters by date and item_type if provided, or returns all records if null.",
    "parameters": {
        "type": "object",
        "properties": {
            "date": {
                "type": ["string", "null"],
                "description": "The target date in YYYY-MM-DD format. Use null to retrieve items across all dates."
            },
            "item_type": {
                "type": ["string", "null"],
                "enum": ["tasks", "events", "meetings", None],
                "description": "The category of items to retrieve. Use null to retrieve all categories."
            }
        },
        "required": ["date", "item_type"],
        "additionalProperties": False
    },
    "strict": True
}

def add_task(date: str, title: str, priority: Optional[str] = None) -> str:
    if not priority:
        priority = "medium"

    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []
    else:
        data = []

    day_entry = next((item for item in data if item["date"] == date), None)
    if not day_entry:
        day_entry = {
            "date": date,
            "tasks": [],
            "events": [],
            "meetings": []
        }
        data.append(day_entry)

    new_task = {
        "id": str(uuid.uuid4())[:8],
        "title": title,
        "priority": priority,
        "status": "pending"
    }

    day_entry["tasks"].append(new_task)

    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    return json.dumps(new_task, ensure_ascii=False)


add_task_schema = {
    "type": "function",
    "name": "add_task",
    "description": "Adds a new task for a specific date with status set to pending.",
    "parameters": {
        "type": "object",
        "properties": {
            "date": {
                "type": "string",
                "description": "The date for the task in YYYY-MM-DD format."
            },
            "title": {
                "type": "string",
                "description": "The title of the task."
            },
            "priority": {
                "type": ["string", "null"],
                "enum": ["low", "medium", "high", None],
                "description": "The priority of the task. Defaults to medium if null."
            }
        },
        "required": ["date", "title", "priority"],
        "additionalProperties": False
    },
    "strict": True
}

def add_event(date: str, title: str, time: str) -> str:
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []
    else:
        data = []

    day_entry = next((item for item in data if item["date"] == date), None)
    if not day_entry:
        day_entry = {
            "date": date,
            "tasks": [],
            "events": [],
            "meetings": []
        }
        data.append(day_entry)

    new_event = {
        "id": str(uuid.uuid4())[:8],
        "title": title,
        "time": time,
        "status": "pending"
    }

    day_entry["events"].append(new_event)

    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    return json.dumps(new_event, ensure_ascii=False)

add_event_schema = {
    "type": "function",
    "name": "add_event",
    "description": "Adds a new event for a specific date and time with status set to pending.",
    "parameters": {
        "type": "object",
        "properties": {
            "date": {
                "type": "string",
                "description": "The date for the event in YYYY-MM-DD format."
            },
            "title": {
                "type": "string",
                "description": "The title of the event."
            },
            "time": {
                "type": "string",
                "description": "The time of the event in HH:MM format."
            }
        },
        "required": ["date", "title", "time"],
        "additionalProperties": False
    },
    "strict": True
}

def add_meeting(date: str, title: str, time: str) -> str:
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []
    else:
        data = []

    day_entry = next((item for item in data if item["date"] == date), None)
    if not day_entry:
        day_entry = {
            "date": date,
            "tasks": [],
            "events": [],
            "meetings": []
        }
        data.append(day_entry)

    new_meeting = {
        "id": str(uuid.uuid4())[:8],
        "title": title,
        "time": time,
        "status": "pending"
    }

    day_entry["meetings"].append(new_meeting)

    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    return json.dumps(new_meeting, ensure_ascii=False)

add_meeting_schema = {
    "type": "function",
    "name": "add_meeting",
    "description": "Adds a new meeting for a specific date and time with status set to pending.",
    "parameters": {
        "type": "object",
        "properties": {
            "date": {
                "type": "string",
                "description": "The date for the meeting in YYYY-MM-DD format."
            },
            "title": {
                "type": "string",
                "description": "The title or description of the meeting."
            },
            "time": {
                "type": "string",
                "description": "The time of the meeting in HH:MM format."
            }
        },
        "required": ["date", "title", "time"],
        "additionalProperties": False
    },
    "strict": True
}