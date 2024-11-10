def prepare_values_with_null(value):
    return f"'{value}'" if value is not None else "null"