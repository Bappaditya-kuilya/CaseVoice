from __future__ import annotations

import json
from typing import Any

import database as db
from calendar_mock import book_consultation as mock_book
from logger import get_logger

logger = get_logger("tools")

TOOL_DEFINITIONS: list[dict[str, Any]] = [
    {
        "type": "function",
        "function": {
            "name": "extract_case_data",
            "description": "Store the collected client intake information in the database.",
            "parameters": {
                "type": "object",
                "properties": {
                    "caller_name": {"type": "string", "description": "Full name of the caller"},
                    "phone": {"type": "string", "description": "Phone number"},
                    "email": {"type": "string", "description": "Email address"},
                    "incident_type": {
                        "type": "string",
                        "enum": ["auto_accident", "slip_and_fall", "medical_malpractice", "workplace_injury", "other"],
                        "description": "Type of incident",
                    },
                    "incident_date": {"type": "string", "description": "Date of the incident (ISO format)"},
                    "incident_location": {"type": "string", "description": "Where the incident happened"},
                    "description": {"type": "string", "description": "Narrative of what happened"},
                    "injuries": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of injuries sustained",
                    },
                    "urgency": {
                        "type": "string",
                        "enum": ["low", "medium", "high", "urgent"],
                        "description": "Urgency level",
                    },
                },
                "required": ["caller_name", "incident_type"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "book_consultation",
            "description": "Book a legal consultation appointment for the client.",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Client name"},
                    "matter_type": {"type": "string", "description": "Type of legal matter"},
                },
                "required": ["name", "matter_type"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "read_legal_citation",
            "description": "Read back a legal citation, case number, or statute clearly.",
            "parameters": {
                "type": "object",
                "properties": {
                    "citation": {"type": "string", "description": "The legal citation text"},
                },
                "required": ["citation"],
            },
        },
    },
]


async def execute_tool(call_id: str, name: str, arguments: dict) -> str:
    """Execute a tool call and return a confirmation string."""
    logger.info("Tool call: %s(%s)", name, arguments)

    if name == "extract_case_data":
        case = await db.get_case_for_call(call_id)
        if case:
            await db.update_case(case["id"], arguments)
            case_id = case["id"]
        else:
            case_id = await db.create_case(call_id, arguments)
        return json.dumps({"status": "saved", "case_id": case_id})

    if name == "book_consultation":
        result = mock_book(arguments.get("name", ""), arguments.get("matter_type", ""))
        if result["booked"]:
            case = await db.get_case_for_call(call_id)
            if case:
                await db.update_case(case["id"], {
                    "consultation_booked": True,
                    "consultation_date": result["date"],
                })
        return json.dumps(result)

    if name == "read_legal_citation":
        citation = arguments.get("citation", "")
        return json.dumps({
            "citation": citation,
            "formatted": f"Let me confirm that citation: {citation}. Is that correct?",
        })

    return json.dumps({"error": f"Unknown tool: {name}"})
