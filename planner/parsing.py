import re

from config import SUPPORTED_EXTENSION

FILENAME_PATTERN = re.compile(r'["\']?([A-Za-z0-9_./-]+\.py)["\']?')
TRAILING_PUNCTUATION = '.,:;!?)]}"\''


def normalize_text(user_input: str) -> str:
    return user_input.strip()


def extract_filename(user_input: str) -> str:
    text = normalize_text(user_input)
    for match in FILENAME_PATTERN.finditer(text):
        candidate = match.group(1).strip().rstrip(TRAILING_PUNCTUATION)
        if candidate.endswith(SUPPORTED_EXTENSION):
            return candidate
    return ""


def extract_write_content(user_input: str, filename: str = "") -> str:
    text = normalize_text(user_input)

    for marker in (" with ", " containing "):
        if marker in text:
            return text.split(marker, 1)[1].strip()

    if filename:
        filename_index = text.find(filename)
        if filename_index != -1:
            remainder = text[filename_index + len(filename):].strip()
            for prefix in ("that ", "to ", "which "):
                if remainder.startswith(prefix):
                    return remainder[len(prefix):].strip()

    return ""


def extract_edit_content(user_input: str, filename: str = "") -> str:
    text = normalize_text(user_input)

    for marker in (" with ", " to ", " so it contains ", " and replace it with "):
        if marker in text:
            tail = text.split(marker, 1)[1].strip()
            if tail:
                return tail

    if filename:
        filename_index = text.find(filename)
        if filename_index != -1:
            remainder = text[filename_index + len(filename):].strip()
            for prefix in (
                "with ",
                "to ",
                "so it contains ",
                "and replace it with ",
            ):
                if remainder.startswith(prefix):
                    return remainder[len(prefix):].strip()

    return ""
