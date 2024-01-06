__example_payload__ = "<script>alert(\"XSS\");</script>"
__type__ = "changing certain characters in the payload into their ordinal equivalent"


def tamper(payload, **kwargs):
    payload = str(payload)
    danger_characters = "%&<>/\\;'\""
    return "".join(
        f"%{ord(char)}" if char in danger_characters else char
        for char in payload
    )
