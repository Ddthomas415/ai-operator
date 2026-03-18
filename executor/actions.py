from pathlib import Path

WORKSPACE = Path("./workspace").resolve()
WORKSPACE.mkdir(exist_ok=True)

def safe_path(filename: str) -> Path:
    target = (WORKSPACE / filename).resolve()
    if target != WORKSPACE and WORKSPACE not in target.parents:
        raise ValueError("Invalid path.")
    return target

def write_file(filename: str, content: str) -> str:
    target = safe_path(filename)
    target.write_text(content + ("\n" if not content.endswith("\n") else ""), encoding="utf-8")
    return f"Created {target}"

def read_file(filename: str) -> str:
    target = safe_path(filename)
    if not target.exists():
        return f"{filename} does not exist."
    return target.read_text(encoding="utf-8")
