__example_payload__ = "'))) AND '1'='1' ((('"
__type__ = "hiding an apostrophe by its UTF equivalent"


def tamper(payload, **kwargs):
    payload = str(payload)
    identifier = "'"
    return "".join("%EF%BC%87" if char == identifier else char for char in payload)