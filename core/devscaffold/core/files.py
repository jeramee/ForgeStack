
import os

def safe_mkdir(path, exist_ok=True):
    os.makedirs(path, exist_ok=exist_ok)

def safe_write_text(path, content, overwrite=False):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if os.path.exists(path) and not overwrite:
        raise Exception("File exists: "+path)
    with open(path,"w") as f:
        f.write(content)
