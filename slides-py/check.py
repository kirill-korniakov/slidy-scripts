#!/usr/bin/env python3

import os
import glob
import re
import subprocess
import traceback

from functions import gglob, cat, grep

root = os.path.join(subprocess.getoutput('git rev-parse --show-toplevel'), 'slides')


def get_grep(text, pattern):
    p = re.compile(pattern)
    out = []
    for line in text:
        out += p.findall(line)
    return out

def check_size(name, size):
    return True if os.path.getsize(name) < size else False

def who_am_i():
    stack = traceback.extract_stack()
    _, _, caller_name, _ = stack[-2]

    print(" - " + caller_name)


# ---------------------------------------------------------

def check_no_tabs():
    who_am_i()
    err = False
    global root
    files = gglob(root, "*.md")
    for f in files:
        lines = grep(cat(f), "\t")
        if len(lines) > 0:
            print('error: in {} has tabs in {} lines'.format(f, lines))
            err = True
    return err


def check_empty_line_before_eof():
    who_am_i()
    err = False
    global root
    files = gglob(root, "*.md")
    for f in files:
        if cat(f)[-1][-1] != '\n':
            print('error: in {} has no line break in the end of file'.format(f))
            err = True
    return err


def check_no_trailing_spaces():
    who_am_i()
    err = False
    global root
    files = gglob(root, "*.md")
    for f in files:
        lines = grep(cat(f), ".*[ ]+$")
        if len(lines) > 0:
            print('error: in {} has space in the end of lines {}'.format(f, lines))
            err = True
    return err


def check_use_highlighting():
    who_am_i()
    err = False
    global root
    files = gglob(root, "*.md")
    for f in files:
        p = re.compile(".*```\n[^`]*```\n.*")
        text = ''.join(cat(f))
        m = p.findall(text)
        if m:
            print('error: {} has block code without highlighting:'.format(f))
            for b in m:
                print('\n{}\n'.format(b))
            err = True
    return err


def check_all_file_size(max_size):
    who_am_i()
    err = False
    global root
    files = gglob(root, "*")
    for f in files:
        if not check_size(f, max_size):
            print('error: sizeof({}) >= {}'.format(f, max_size))
            err = True
    return err


def check_all_file_name():
    who_am_i()
    err = False
    global root
    files = os.listdir(root)
    for f in files:
        if os.path.isdir(f) and re.match('\d\d-.*', f):
            path = os.path.abspath(os.path.join(root, f))
            file = os.path.join(path, os.path.basename(path) + '.md')
            if not os.path.exists(file):
                print('error: folder {} has not {}'.format(f, file))
                err = True
    return err


def check_all_images_are_used():
    who_am_i()
    err = False
    global root
    files = gglob(root, "*.md")
    for f in files:
        path = os.path.dirname(os.path.abspath(f))
        if not os.path.exists(path + "/pix"):
            continue

        existing_images = gglob(path, "*.png")  + gglob(path, "*.jpg") +\
                     gglob(path, "*.jpeg") + gglob(path, "*.gif") +\
                     gglob(path, "*.svg")

        mentioned_images = get_grep(cat(f), "!\[\]\(([^)]*)\)")

        for img in mentioned_images:
            full_path = os.path.join(path, img).replace('/./', '/')
            if os.path.exists(full_path) and (full_path in existing_images):
                existing_images.remove(full_path)

        if len(existing_images) > 0:
            print("images are not used: ")
            for i in existing_images:
                print('      - {}'.format(i))
            err = False  # TODO: change to Truem so check fails

    return err


def check_all_images_exist():
    who_am_i()
    err = False
    global root
    files = gglob(root, "*.md")
    for f in files:
        path = os.path.dirname(os.path.abspath(f))
        m = get_grep(cat(f), "!\[\]\(([^)]*)\)")
        for img in m:
            full_path = os.path.join(path, img).replace('/./', '/')
            if not os.path.exists(full_path):
                print('error: {} does not exist'.format(full_path))
                err = True
    return err


def main():
    print("Starting validation process:")
    err = False

    err = err or check_use_highlighting()
    err = err or check_no_trailing_spaces()
    err = err or check_no_tabs()
    err = err or check_empty_line_before_eof()
    err = err or check_all_file_size(2500 * 1024)
    err = err or check_all_file_name()
    err = err or check_all_images_exist()
    err = err or check_all_images_are_used()

    if err:
        print("FAIL: validation finished with errors")
        return 1
    else:
        print("SUCCESS: validation finished without errors")
        return 0


if __name__ == '__main__':
    exit(main())
