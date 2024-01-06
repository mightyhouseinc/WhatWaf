import random


__example_payload__ = "AS start WHERE 1601=1601 UNION ALL SELECT NULL,NULL"
__type__ = "changing the character case of the payload randomly with either upper or lower case"


def tamper(payload, **kwargs):
    payload = str(payload)
    identifier = (1, 2)
    return "".join(
        char.upper() if random.choice(identifier) == 1 else char.lower()
        for char in payload
    )
