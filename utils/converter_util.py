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

def format_list_of_dict_with_datetime(data: list[dict], datetime_fields: list[str]) -> list[dict]:
    if not data:
        return []

    formatted = []
    for row in data:
        row = model_to_dict(row)
        for field in datetime_fields:
            if field in row and isinstance(row[field], datetime):
                row[field] = row[field].isoformat()
        formatted.append(row)
    return formatted
