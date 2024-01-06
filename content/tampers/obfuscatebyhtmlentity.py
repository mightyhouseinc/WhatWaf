__example_payload__ = r"""&\lt' AND 1=1 ',<script>alert("test");</script>"""
__type__ = "changing the payload characters into their HTML entities"


def tamper(payload, **kwargs):
    payload = str(payload)
    skip = ";"
    encoding_schema = {
        " ": "&nbsp;", "<": "&lt;", ">": "&gt;",
        "&": "&amp;", '"': "&quot;", "'": "&apos;",
    }
    if all(c not in payload for c in encoding_schema):
        return payload
    return "".join(encoding_schema.get(char, char) for char in payload)
