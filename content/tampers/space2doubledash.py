__example_payload__ = "' AND 1=1 ORDERBY(1,2,3,4,5) '; asdf"
__type__ = "changing the spaces in the payload into double dashes"


def tamper(payload, **kwargs):
    modifier = "--"
    return "".join(modifier if char == " " else char for char in payload)