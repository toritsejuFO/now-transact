def check_fields_same(src, dest, fields):
    if not isinstance(fields, list) or not isinstance(src, dict) or not isinstance(dest, dict):
        raise Exception('Invalid params received')

    for field in fields:
        if src[field] != dest[field]:
            return False

    return True
