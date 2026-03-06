
import yaml

def load_config(path):
    with open(path) as f:
        raw = f.read()
    cfg = yaml.safe_load(raw)
    cfg["_raw_yaml"] = raw
    return cfg
