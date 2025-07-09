def validate_target_in_rules(target: str, rules: list[str]) -> bool:
    return target.lower() in [rule.lower() for rule in rules]

def validate_char_length(data: str, min: int = None, max: int = None) -> bool:
    if not isinstance(data, str):
        return False

    length = len(data)

    if min is not None and length < min:
        return False
    if max is not None and length > max:
        return False

    return True


