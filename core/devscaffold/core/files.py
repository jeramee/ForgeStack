from pathlib import Path

def safe_mkdir(path, exist_ok=True):
    Path(path).mkdir(parents=True, exist_ok=exist_ok)

def safe_write_text(path, content, overwrite=False):
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists() and not overwrite:
        raise FileExistsError(f"File exists: {path}")
    target.write_text(content, encoding="utf-8")
