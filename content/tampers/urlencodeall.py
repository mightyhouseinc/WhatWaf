__example_payload__ = "SELECT * FROM information_schema.tables"
__type__ = "encoding all characters in the payload into their URL encoding equivalent"


def tamper(payload, **kwargs):
    return "".join(f"%{ord(char)}" for char in payload)
