import time
try:
    raw_input
except:
    raw_input = input


def set_color(string, level=None):
    """
    set the string color
    """
    color_levels = {
        10: "\033[36m{}\033[0m",
        15: "\033[1m\033[32m{}\033[0m",
        20: "\033[32m{}\033[0m",
        30: "\033[1m\033[33m{}\033[0m",
        35: "\033[33m{}\033[0m",
        40: "\033[1m\033[31m{}\033[0m",
        45: "\033[1m\033[96m{}\033[0m",
        50: "\033[1m\033[30m{}\033[0m",
        60: "\033[7;31;31m{}\033[0m"
    }
    if level is None:
        return color_levels[20].format(string)
    else:
        return color_levels[int(level)].format(string)


def info(string):
    print(
        f'\033[38m[{time.strftime("%H:%M:%S")}]\033[0m{set_color(f"[INFO] {string}", level=20)}'
    )


def debug(string):
    print(
        f'\033[38m[{time.strftime("%H:%M:%S")}]\033[0m{set_color(f"[DEBUG] {string}", level=10)}'
    )


def warn(string, minor=False):
    if not minor:
        print(
            f'\033[38m[{time.strftime("%H:%M:%S")}]\033[0m{set_color(f"[WARN] {string}", level=30)}'
        )
    else:
        print(
            f'\033[38m[{time.strftime("%H:%M:%S")}]\033[0m{set_color(f"[WARN] {string}", level=35)}'
        )


def error(string):
    print(
        f'\033[38m[{time.strftime("%H:%M:%S")}]\033[0m{set_color(f"[ERROR] {string}", level=40)}'
    )


def fatal(string):
    print(
        f'\033[38m[{time.strftime("%H:%M:%S")}]\033[0m{set_color(f"[FATAL] {string}", level=60)}'
    )


def payload(string):
    print(set_color(f"[PAYLOAD] {string}", level=50))


def success(string):
    print(
        f'\033[38m[{time.strftime("%H:%M:%S")}]\033[0m{set_color(f"[SUCCESS] {string}", level=15)}'
    )


def prompt(string, opts, default="n", check_choice=True):
    opts = list(opts)
    choice = raw_input(
        f'\033[38m[{time.strftime("%H:%M:%S")}]\033[0m[PROMPT] {string}[{"/".join(opts) if opts else ""}]: '
    )
    if check_choice:
        if choice not in [o.lower() for o in opts]:
            choice = default
    return choice


def discover(string):
    print(
        f'\033[38m[{time.strftime("%H:%M:%S")}]\033[0m{set_color(f"[FIREWALL] {string}", level=45)}'
    )