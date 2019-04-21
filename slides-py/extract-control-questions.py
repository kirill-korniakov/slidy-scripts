#!/usr/bin/env python3
# -*- coding: utf8 -*-

import os

from functions import gglob, cat, grep

header = "# Контрольные вопросы"

def check_if_control_questions_exist(file):
    lines = cat(file)
    findings = grep(lines, header)
    return len(findings)

def split_into_groups(files):
    has_no_questions = []
    has_questions = []
    has_multiple_questions = []

    for file in files:
        number = check_if_control_questions_exist(file)
        if number == 0:
            has_no_questions.append(file)
        elif number == 1:
            has_questions.append(file)
        else:
            has_multiple_questions.append(file)

    return (has_no_questions, has_questions, has_multiple_questions)

def make_header(tup):
    # Format:
    # <a name="text"/>
    # ## 1. Текстовые форматы

    header = "<a name=\"" + tup[1] + "\"/>\n\n"
    digit = str(int(os.path.basename(tup[0])[:2]))
    header += "## " + digit + ". " + tup[2] + "\n"

    return header

def extract_questions(tup):
    lines = cat(tup[0])

    questions = make_header(tup)

    copying = False
    for line in lines:
        if copying:
            if line.startswith("#"):
                break;
            else:
                questions += line

        if line.startswith(header):
            copying = True

    return questions

def extract_files_with_control_questions():
    files = gglob("./", "*.md")
    # print("Full list of files found:")
    # print("\n - ".join(files))

    groups = split_into_groups(files)

    if len(groups[0]):
        print("These files do not contain control questions:")
        print(" - " + "\n - ".join(groups[0]))
    if len(groups[2]):
        print("These files have multiple questions:")
        print(" - " + "\n - ".join(groups[2]))

    return sorted(groups[1])

def extract_headers(files):
    paths_tags_names = []

    for file in files:
        path = file
        tag = os.path.splitext(os.path.basename(file))[0][3:]
        with open(file, 'r', encoding="utf8") as f: first_line = f.readline()
        title = first_line[2:-1]

        paths_tags_names.append((path, tag, title))

    return paths_tags_names

def generate_toc(paths_tags_names):
    toc = ""

    toc += "# Список контрольных вопросов\n\n"
    toc += "---------------------\n\n"
    for tup in paths_tags_names:
        #   1. [Текстовые форматы](#text)
        toc += "  1. [" + tup[2] + "](#" + tup[1] + ")\n"
    toc += "\n---------------------\n\n"

    return toc

if __name__ == '__main__':
    files = extract_files_with_control_questions()
    paths_tags_names = extract_headers(files)
    toc = generate_toc(paths_tags_names)

    content = toc

    print("Getting questions from:")
    for tup in paths_tags_names:
        print(" - " + tup[0])
        content += extract_questions(tup)

    output = open("slides/control-questions.md", 'w', encoding="utf8")
    output.write(content)
    output.close()
