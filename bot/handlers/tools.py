"""LLM tool definitions for LMS API endpoints."""

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_items",
            "description": "Get list of all labs and tasks",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_learners",
            "description": "Get list of enrolled students and groups",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_scores",
            "description": "Get score distribution (4 buckets) for a specific lab",
            "parameters": {
                "type": "object",
                "properties": {
                    "lab": {
                        "type": "string",
                        "description": "Lab identifier, e.g. 'lab-01'"
                    }
                },
                "required": ["lab"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_pass_rates",
            "description": "Get per-task average scores and attempt counts for a lab",
            "parameters": {
                "type": "object",
                "properties": {
                    "lab": {
                        "type": "string",
                        "description": "Lab identifier, e.g. 'lab-01'"
                    }
                },
                "required": ["lab"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_timeline",
            "description": "Get submissions per day for a lab",
            "parameters": {
                "type": "object",
                "properties": {
                    "lab": {
                        "type": "string",
                        "description": "Lab identifier, e.g. 'lab-01'"
                    }
                },
                "required": ["lab"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_groups",
            "description": "Get per-group scores and student counts for a lab",
            "parameters": {
                "type": "object",
                "properties": {
                    "lab": {
                        "type": "string",
                        "description": "Lab identifier, e.g. 'lab-01'"
                    }
                },
                "required": ["lab"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_top_learners",
            "description": "Get top N learners by score for a lab",
            "parameters": {
                "type": "object",
                "properties": {
                    "lab": {
                        "type": "string",
                        "description": "Lab identifier, e.g. 'lab-01'"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Number of top learners to return",
                        "default": 5
                    }
                },
                "required": ["lab"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_completion_rate",
            "description": "Get completion rate percentage for a lab",
            "parameters": {
                "type": "object",
                "properties": {
                    "lab": {
                        "type": "string",
                        "description": "Lab identifier, e.g. 'lab-01'"
                    }
                },
                "required": ["lab"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "trigger_sync",
            "description": "Trigger ETL sync to refresh data from autochecker",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    }
]

# Map tool names to LMSClient methods
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
