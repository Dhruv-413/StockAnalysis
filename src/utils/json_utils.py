import json
from datetime import datetime
from typing import Any

class DatetimeEncoder(json.JSONEncoder):
    """Custom JSON encoder that handles datetime objects by converting them to ISO format strings."""
    def default(self, obj: Any) -> Any:
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)

def serialize_object(obj: Any) -> Any:
    """
    Recursively traverse dictionaries and lists to convert datetime objects to strings.
    This is useful for ensuring all data is JSON serializable before it reaches the JSON encoder.
    
    Args:
        obj: Any Python object (usually a dict or list)
        
    Returns:
        The object with all datetime values converted to ISO format strings
    """
    if isinstance(obj, datetime):
        return obj.isoformat()
    
    if isinstance(obj, dict):
        return {k: serialize_object(v) for k, v in obj.items()}
    
    if isinstance(obj, list):
        return [serialize_object(item) for item in obj]
    
    return obj