#!/usr/bin/env python3
# -*- coding: utf8 -*-

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

def extract_questions(file):
    questions = ""

    lines = cat(file)
    questions += lines[0]

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

if __name__ == '__main__':
    files = gglob("./", "*.md")
    print("Full list of files found:")
    print("\n - ".join(files))

    groups = split_into_groups(files)

    if len(groups[0]):
        print("These files do not have questions at all:")
        print("\n - ".join(groups[0]))
    if len(groups[2]):
        print("These files have multiple questions:")
        print("\n - ".join(groups[2]))

    questions = ""
    for file in groups[1]:
        questions += extract_questions(file)

    # print("Extracted questions:")
    # print(questions)

    output = open("extracted-questions.md", 'w')
    output.write(questions)
    output.close()
