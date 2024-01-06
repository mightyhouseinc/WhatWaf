import re
import sys
import json
import hashlib
import base64
try:
    from urllib2 import Request, urlopen
except ImportError:
    from urllib.request import Request, urlopen

import requests
from bs4 import BeautifulSoup

import lib.settings
import lib.formatter


def create_identifier(data):
    obj = hashlib.sha1()
    try:
        obj.update(data)
    except:
        obj.update(data.encode("utf-8"))
    return obj.hexdigest()[1:10]


def get_token(path):
    """
    we know what this is for
    """
    with open(path) as _token:
        data = _token.read()
        token, n = data.split(":")
        for _ in range(int(n)):
            token = base64.b64decode(token)
    return token


def ensure_no_issue(param):
    """
    ensure that there is not already an issue that has been created for yours
    """
    urls = (
        "https://github.com/Ekultek/WhatWaf/issues",
        "https://github.com/Ekultek/WhatWaf/issues?q=is%3Aissue+is%3Aclosed"
    )
    for url in urls:
        req = requests.get(url)
        param = re.compile(param)
        try:
            if param.search(req.content) is not None:
                return True
        except:
            content = str(req.content)
            if param.search(content) is not None:
                return True
    return False


def find_url(params):
    """
    get the URL that your issue is created at
    """
    searches = (
        "https://github.com/Ekultek/WhatWaf/issues",
        "https://github.com/Ekultek/WhatWaf/issues?q=is%3Aissue+is%3Aclosed"
    )
    retval = "https://github.com{}"
    for search in searches:
        href = None
        searcher = re.compile(params, re.I)
        req = requests.get(search)
        status, html = req.status_code, req.content
        if status == 200:
            split_information = str(html).split("\n")
            for i, line in enumerate(split_information):
                if searcher.search(line) is not None:
                    href = split_information[i]
        if href is not None:
            soup = BeautifulSoup(href, "html.parser")
            for item in soup.findAll("a"):
                link = item.get("href")
                return retval.format(link)
    return None


def hide_sensitive(args, command):
    """
    hide sensitive information out of the arguments
    """
    try:
        url_index = args.index(command) + 1
        hidden_url = ''.join([x.replace(x, "*") for x in str(args[url_index])])
        args.pop(url_index)
        args.insert(url_index, hidden_url)
        return ' '.join(args)
    except:
        return ' '.join(list(sys.argv))


def request_issue_creation(exception_details):
    """
    create an issue instead of a firewall
    """
    import platform

    question = lib.formatter.prompt(
        "would you like to create an anonymized issue for the unhandled exception", "yN"
    )
    if question.lower().startswith("y"):
        is_newest = lib.settings.check_version(speak=False)
        if not is_newest:
            lib.formatter.error(
                "whatwaf is not the newest version, in order to create an issue, please update whatwaf"
            )
            return

        identifier = create_identifier(exception_details)

        for item in sys.argv:
            if item in lib.settings.SENSITIVE_ARGUMENTS:
                argv_data = hide_sensitive(sys.argv, item)
        title = f"Whatwaf Unhandled Exception ({identifier})"

        python_version = f"{sys.version_info.major}.{sys.version_info.minor}{sys.version_info.micro}"
        issue_creation_template = {
            "title": title,
            "body": f"Whatwaf version: `{lib.settings.VERSION}`\nRunning context: `{argv_data}`\nPython version: `{python_version}`\nTraceback: \n```\n{exception_details}\n```\nRunning platform: `{platform.platform()}`",
        }

        issue_creation_json = json.dumps(issue_creation_template)
        if sys.version_info > (3,):  # python 3
            issue_creation_json = issue_creation_json.encode("utf-8")
        if not ensure_no_issue(identifier):
            req = Request(
                url="https://api.github.com/repos/ekultek/whatwaf/issues",
                data=issue_creation_json,
                headers={
                    "Authorization": f"token {get_token(lib.settings.TOKEN_PATH)}"
                },
            )
            try:
                urlopen(req, timeout=10).read()
                lib.formatter.info(
                    f"this exception has been submitted successfully with the title '{title}', URL: '{find_url(identifier)}'"
                )
            except Exception as e:
                unprocessed_file_path = lib.settings.save_temp_issue(issue_creation_template)
                lib.formatter.fatal(
                    f"caught an exception while trying to process request: {str(e)}, you can either create this issue manually, or try again. if you have decided to create the issue manually you can find the issue information in the following file: {unprocessed_file_path}"
                )
        else:
            lib.formatter.error(
                f"this exception has already been reported: '{find_url(identifier)}'"
            )


def request_firewall_issue_creation(path):
    """
    request the creation and create the issue
    """
    question = lib.formatter.prompt(
        "would you like to create an issue with the discovered unknown firewall to potentially "
        "get a detection script created for it", "yN"
    )
    if question.lower().startswith("y"):
        is_newest = lib.settings.check_version(speak=False)
        if not is_newest:
            lib.formatter.error(
                "whatwaf is currently not the newest version, please update to request a firewall script creation"
            )
            return

        # gonna read a chunk of it instead of one line
        chunk = 4096
        with open(path) as data:
            identifier = create_identifier(data.read(chunk))
            # gotta seek to the beginning of the file since it's already been read `4096` into it
            data.seek(0)
            full_fingerprint = data.read()
            issue_title = f"Unknown Firewall ({identifier})"

        for item in sys.argv:
            if item in lib.settings.SENSITIVE_ARGUMENTS:
                data = hide_sensitive(sys.argv, item)

        issue_data = {
            "title": issue_title,
            "body": f"WhatWaf version: `{lib.settings.VERSION}`\nRunning context: `{data}`\nFingerprint:\n```\n{full_fingerprint}\n```",
        }

        _json_data = json.dumps(issue_data)
        if sys.version_info > (3,):  # python 3
            _json_data = _json_data.encode("utf-8")

        if not ensure_no_issue(identifier):
            req = Request(
                url="https://api.github.com/repos/ekultek/whatwaf/issues",
                data=_json_data,
                headers={
                    "Authorization": f"token {get_token(lib.settings.TOKEN_PATH)}"
                },
            )
            try:
                urlopen(req, timeout=10).read()
                lib.formatter.info(
                    f"this firewalls fingerprint has successfully been submitted with the title '{issue_title}', URL '{find_url(identifier)}'"
                )
            except Exception as e:
                unprocessed_file_path = lib.settings.save_temp_issue(issue_data)
                lib.formatter.fatal(
                    f"caught an exception while trying to process request: {str(e)}, you can either create this issue manually, or try again. if you have decided to create the issue manually you can find the issue information in the following file: {unprocessed_file_path}"
                )
        else:
            lib.formatter.error(
                f"someone has already sent in this firewalls fingerprint here: {find_url(identifier)}"
            )
    lib.formatter.info(
        f"for further analysis the WAF fingerprint can be found in: '{path}'"
    )