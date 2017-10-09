import re
import os
import glob

def gglob(path, f):
    l = glob.glob(os.path.join(path, f))
    for folder in os.listdir(path):
        full_path = os.path.join(path, folder)
        if os.path.isdir(full_path):
            l += gglob(full_path, f)
    return l

def cat(name):
    with open(name, encoding="utf8") as f:
        content = f.readlines()
    return content

def grep(text, pattern):
    p = re.compile(pattern)
    lines = []
    i = 0
    for line in text:
        i += 1
        if p.match(line):
            lines += [i]
    return lines

def get_grep(text, pattern):
    p = re.compile(pattern)
    out = []
    for line in text:
        out += p.findall(line)
    return out
