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
    return open(name, 'r').readlines()

def grep(text, pattern):
    p = re.compile(pattern)
    lines = []
    i = 0
    for l in text:
        i += 1
        if p.match(l):
            lines += [i]
    return lines
