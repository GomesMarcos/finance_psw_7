def validate_fields(instance, null_fields=None):
    null_fields = null_fields or []
    return not any((attr not in ['id', 'state'] + null_fields) and (val is None or val == '')
                   for attr, val in instance.__dict__.items())
