from pathlib import Path
from pathlib import PurePosixPath

from config import SUPPORTED_EXTENSION

WORKSPACE = Path("./workspace").resolve()
WORKSPACE.mkdir(exist_ok=True)

def validate_filename(filename: str) -> str:
    cleaned = filename.strip()
    if not cleaned:
        raise ValueError("Filename cannot be empty.")
    if cleaned.endswith(("/", "\\")):
        raise ValueError("Filename must point to a Python file, not a directory.")

    path = PurePosixPath(cleaned)
    if path.is_absolute():
        raise ValueError("Absolute paths are not allowed.")
    if any(part in {"", ".", ".."} for part in path.parts):
        raise ValueError("Invalid path.")
    if path.suffix != SUPPORTED_EXTENSION:
        raise ValueError(f"Only {SUPPORTED_EXTENSION} files are supported.")

    return cleaned

def safe_path(filename: str) -> Path:
    target = (WORKSPACE / validate_filename(filename)).resolve()
    if target != WORKSPACE and WORKSPACE not in target.parents:
        raise ValueError("Invalid path.")
    return target

def file_exists(filename: str) -> bool:
    return safe_path(filename).exists()

def write_file(filename: str, content: str, *, allow_overwrite: bool = False) -> str:
    target = safe_path(filename)
    existed_before = target.exists()
    if existed_before and not allow_overwrite:
        raise FileExistsError(f"{filename} already exists.")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content + ("\n" if not content.endswith("\n") else ""), encoding="utf-8")
    action = "Updated" if existed_before else "Created"
    return f"{action} {target}"


def edit_file(filename: str, content: str) -> str:
    target = safe_path(filename)
    if not target.exists():
        raise FileNotFoundError(f"{filename} does not exist.")
    target.write_text(content + ("\n" if not content.endswith("\n") else ""), encoding="utf-8")
    return f"Updated {target}"

def read_file(filename: str) -> str:
    target = safe_path(filename)
    if not target.exists():
        return f"{filename} does not exist."
    return target.read_text(encoding="utf-8")


def list_workspace() -> str:
    files = sorted(
        str(path.relative_to(WORKSPACE))
        for path in WORKSPACE.rglob("*")
        if path.is_file() and "__pycache__" not in path.parts and path.suffix == SUPPORTED_EXTENSION
    )
    if not files:
        return "Workspace is empty."
    return "\n".join(files)
