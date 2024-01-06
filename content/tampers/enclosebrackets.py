import string


__example_payload__ = 'AND 1=1,<script>alert("1,2,3,4,5);</script>'
__type__ = "enclosing numbers into brackets"


def tamper(payload, **kwargs):
    payload = str(payload)
    to_enclose = string.digits
    if all(i not in list(payload) for i in to_enclose):
        return payload
    return "".join(f"[{char}]" if char in to_enclose else char for char in payload)
