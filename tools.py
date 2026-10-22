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

def delete_item(item_id: str) -> str:
    if not os.path.exists(DB_FILE):
        return json.dumps({"success": False, "error": "Database not found."})

    with open(DB_FILE, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            return json.dumps({"success": False, "error": "Invalid database format."})

    for day_entry in data:
        for category in ["tasks", "events", "meetings"]:
            items = day_entry.get(category, [])
            for i, item in enumerate(items):
                if item.get("id") == item_id:
                    deleted_item = items.pop(i)
                    with open(DB_FILE, "w", encoding="utf-8") as f:
                        json.dump(data, f, indent=2, ensure_ascii=False)
                    return json.dumps({"success": True, "deleted_item": deleted_item}, ensure_ascii=False)

    return json.dumps({"success": False, "error": "Item not found."})

delete_item_schema = {
    "type": "function",
    "name": "delete_item",
    "description": "Deletes a task, event, or meeting by its unique ID.",
    "parameters": {
        "type": "object",
        "properties": {
            "item_id": {
                "type": "string",
                "description": "The unique ID of the item to delete."
            }
        },
        "required": ["item_id"],
        "additionalProperties": False
    },
    "strict": True
}

def update_item(item_id: str, title: Optional[str] = None, status: Optional[str] = None) -> str:
    if not os.path.exists(DB_FILE):
        return json.dumps({"success": False, "error": "Database not found."})

    with open(DB_FILE, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            return json.dumps({"success": False, "error": "Invalid database format."})

    for day_entry in data:
        for category in ["tasks", "events", "meetings"]:
            items = day_entry.get(category, [])
            for item in items:
                if item.get("id") == item_id:
                    if title is not None:
                        item["title"] = title
                    if status is not None:
                        item["status"] = status
                    with open(DB_FILE, "w", encoding="utf-8") as f:
                        json.dump(data, f, indent=2, ensure_ascii=False)
                    return json.dumps({"success": True, "updated_item": item}, ensure_ascii=False)

    return json.dumps({"success": False, "error": "Item not found."})

update_item_schema = {
    "type": "function",
    "name": "update_item",
    "description": "Updates the title and/or status of a task, event, or meeting by its unique ID.",
    "parameters": {
        "type": "object",
        "properties": {
            "item_id": {
                "type": "string",
                "description": "The unique ID of the item to update."
            },
            "title": {
                "type": ["string", "null"],
                "description": "The new title for the item. Pass null to keep the current title."
            },
            "status": {
                "type": ["string", "null"],
                "enum": ["pending", "completed", "not_completed", "cancelled", None],
                "description": "The new status for the item. Pass null to keep the current status."
            }
        },
        "required": ["item_id", "title", "status"],
        "additionalProperties": False
    },
    "strict": True
}

tools = [
    get_today_date_schema,
    get_future_date_schema,
    add_task_schema,
    add_event_schema,
    add_meeting_schema,
    get_items_schema,
    delete_item_schema,
    update_item_schema
]

available_functions = {
    "get_today_date": get_today_date,
    "get_future_date": get_future_date,
    "add_task": add_task,
    "add_event": add_event,
    "add_meeting": add_meeting,
    "get_items": get_items,
    "delete_item": delete_item,
    "update_item": update_item
}

def execute_tool(name: str, arguments: str) -> str:
    func = available_functions.get(name)
    if not func:
        return json.dumps({"error": f"Tool {name} not found."})
    
    args = json.loads(arguments) if arguments else {}
    return func(**args)