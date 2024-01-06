import string


__example_payload__ = 'AND 1=1,<script>alert("1,2,3,4,5);</script>'
__type__ = "enclosing brackets and masking an apostrophe around the character in the brackets"


def tamper(payload, **kwargs):
    payload = str(payload)
    to_enclose = string.digits
    if all(i not in payload for i in to_enclose):
        return payload
    return "".join(
        f"[%EF%BC%87{char}%EF%BC%87]" if char in to_enclose else char
        for char in payload
    )
