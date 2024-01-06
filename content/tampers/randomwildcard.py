import random
import string


__example_payload__ = "/bin/cat /etc/passwd"
__type__ = "changing characters into a wildcard"


def tamper(payload, **kwargs):
    wildcard = ["*", "?"]
    safe_chars = f"{string.punctuation} "
    retval = ""
    for char in list(payload):
        if all(p != char for p in safe_chars):
            do_it = random.randint(1, 10) <= 3
            retval += random.choice(wildcard) if do_it else char
        else:
            retval += char
    return retval
