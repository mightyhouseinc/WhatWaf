import string


__example_payload__ = "<script>alert('test');</script>"
__type__ = "encoding punctuation characters by their URL encoding equivalent"


def tamper(payload, **kwargs):
    to_encode = string.punctuation
    if all(s not in payload for s in to_encode):
        return payload
    return "".join(
        f"%{ord(char)}" if char in to_encode else char for char in payload
    )