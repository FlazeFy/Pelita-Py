from sqlalchemy.orm import class_mapper

def model_to_dict(model_instance):
    return {
        column.key: getattr(model_instance, column.key)
        for column in class_mapper(model_instance.__class__).columns
    }