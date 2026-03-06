
from dataclasses import dataclass, field

@dataclass
class FileWrite:
    path: str
    content: str

@dataclass
class Command:
    cmd: list
    cwd: str="."

@dataclass
class Plan:
    folders: list = field(default_factory=list)
    files: list = field(default_factory=list)
    commands: list = field(default_factory=list)
    compose: dict = field(default_factory=dict)

def deep_merge(a,b):
    out=dict(a)
    for k,v in b.items():
        if k in out and isinstance(out[k],dict) and isinstance(v,dict):
            out[k]=deep_merge(out[k],v)
        else:
            out[k]=v
    return out

def merge_plans(plans):
    merged=Plan()
    for p in plans:
        merged.folders+=p.folders
        merged.files+=p.files
        merged.commands+=p.commands
        merged.compose=deep_merge(merged.compose,p.compose)
    merged.folders=list(set(merged.folders))
    return merged
