from __future__ import annotations

import getpass
import ipaddress
import os
import re
import socket
from copy import deepcopy
from typing import Any


IPV4_PATTERN = re.compile(r"(?<![\d.])(?:\d{1,3}\.){3}\d{1,3}(?![\d.])")
IPV6_CANDIDATE_PATTERN = re.compile(
    r"(?i)(?<![0-9a-f:.%])(?:[0-9a-f]{0,4}:){2,}[0-9a-f:.]*(?:%[0-9a-z_.-]+)?(?![0-9a-f:.%])"
)
MAC_PATTERN = re.compile(r"(?i)(?<![0-9a-f])(?:[0-9a-f]{2}[:-]){5}[0-9a-f]{2}(?![0-9a-f])")
USER_PATH_PATTERN = re.compile(r"(?i)\b([A-Z]:\\Users\\)([^\\\s|]+)")


class Redactor:
    """Recursively remove common identifiers before a report is shared."""

    def __init__(self, username: str | None = None, computer_name: str | None = None) -> None:
        self.username = username if username is not None else (getpass.getuser() or "")
        self.computer_name = computer_name if computer_name is not None else (socket.gethostname() or "")
        self.home = os.path.expanduser("~")

    def text(self, value: str) -> str:
        redacted = value
        replacements = [
            (self.home, r"C:\Users\[REDACTED]"),
            (self.computer_name, "[REDACTED-HOST]"),
            (self.username, "[REDACTED-USER]"),
        ]
        for original, replacement in replacements:
            if original:
                redacted = re.sub(re.escape(original), lambda _: replacement, redacted, flags=re.IGNORECASE)
        redacted = USER_PATH_PATTERN.sub(lambda match: match.group(1) + "[REDACTED]", redacted)
        redacted = MAC_PATTERN.sub("[REDACTED-MAC]", redacted)
        redacted = IPV6_CANDIDATE_PATTERN.sub(_redact_ipv6_candidate, redacted)
        redacted = IPV4_PATTERN.sub("[REDACTED-IP]", redacted)
        return redacted

    def value(self, value: Any) -> Any:
        if isinstance(value, str):
            return self.text(value)
        if isinstance(value, list):
            return [self.value(item) for item in value]
        if isinstance(value, tuple):
            return tuple(self.value(item) for item in value)
        if isinstance(value, dict):
            return {key: self.value(item) for key, item in value.items()}
        return value


def redact_data(data: dict[str, Any], redactor: Redactor | None = None) -> dict[str, Any]:
    safe = (redactor or Redactor()).value(deepcopy(data))
    safe["privacy"] = {
        "redacted": True,
        "mode": "standard",
        "notice": "Common usernames, hostnames, user-profile paths, IPv4/IPv6 addresses, and MAC addresses were redacted.",
    }
    return safe


def _redact_ipv6_candidate(match: re.Match[str]) -> str:
    candidate = match.group(0)
    suffix = ""
    while candidate.endswith("."):
        candidate = candidate[:-1]
        suffix = "." + suffix

    address = candidate.split("%", 1)[0]
    try:
        parsed = ipaddress.ip_address(address)
    except ValueError:
        return match.group(0)
    if isinstance(parsed, ipaddress.IPv6Address):
        return "[REDACTED-IP]" + suffix
    return match.group(0)
