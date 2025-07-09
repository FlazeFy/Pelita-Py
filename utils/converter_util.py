from sqlalchemy.orm import class_mapper
from datetime import datetime

def model_to_dict(obj):
    if isinstance(obj, list):
        return [
            {
                column.key: getattr(item, column.key)
                for column in class_mapper(item.__class__).columns
            }
            for item in obj
        ]
    return {
        column.key: getattr(obj, column.key)
        for column in class_mapper(obj.__class__).columns
    }

def format_list_of_dict_with_datetime(data: list[dict] | dict, datetime_fields: list[str]) -> list[dict] | dict:
    if not data:
        return [] if isinstance(data, list) else {}

    is_dict = isinstance(data, dict)
    rows = [data] if is_dict else data

    formatted = []
    for row in rows:
        if not isinstance(row, dict):
            row = model_to_dict(row)
        for field in datetime_fields:
            if field in row and isinstance(row[field], datetime):
                row[field] = row[field].isoformat()
        formatted.append(row)

    return formatted[0] if is_dict else formatted

