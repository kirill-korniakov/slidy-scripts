#!/usr/bin/env python3

import os
import re
import subprocess
import unittest

from functions import gglob, cat, grep, get_grep

class TestSlides(unittest.TestCase):

    def setUp(self):
        toplevel = subprocess.getoutput('git rev-parse --show-toplevel')
        self.root = os.path.join(toplevel, 'slides')
        self.MAX_FILE_SIZE = 2500 * 1024
        self.md_files = gglob(self.root, "*.md")

    def test_no_tabs(self):
        error = False

        for f in self.md_files:
            lines = grep(cat(f), "\t")
            if len(lines) > 0:
                print('error: in {} has tabs in {} lines'.format(f, lines))
                error = True

        self.assertEqual(False, error)

    def test_empty_line_before_eof(self):
        error = False

        for f in self.md_files:
            if cat(f)[-1][-1] != '\n':
                print('error: in {} has no line break in the end of file'.format(f))
                error = True

        self.assertEqual(False, error)

    # def test_no_trailing_spaces(self):
    #     error = False

    #     for f in self.md_files:
    #         lines = grep(cat(f), ".*[ ]+$")
    #         if len(lines) > 0:
    #             print('error: in {} has space in the end of lines {}'.format(f, lines))
    #             error = True

    #     self.assertEqual(False, error)

    def test_no_trailing_spaces(self):
        for file in self.md_files:
            lines = grep(cat(file), ".*[ ]+$")
            self.assertEqual(0, len(lines))

    def test_use_highlighting(self):
        error = False

        for f in self.md_files:
            p = re.compile(".*```\n[^`]*```\n.*")
            text = ''.join(cat(f))
            m = p.findall(text)
            if m:
                print('error: {} has block code without highlighting:'.format(f))
                for b in m:
                    print('\n{}\n'.format(b))
                error = True

        self.assertEqual(False, error)

    def test_all_file_size(self):
        error = False

        files = gglob(self.root, "*")
        files = [f for f in files if os.path.splitext(f)[1] != ".pdf"]

        for f in files:
            if not os.path.getsize(f) < self.MAX_FILE_SIZE:
                print('Error: size of {} >= {}'.format(f, self.MAX_FILE_SIZE))
                error = True

        self.assertEqual(False, error)

    def test_all_file_name(self):
        error = False

        files = os.listdir(self.root)
        for f in files:
            if os.path.isdir(f) and re.match('\d\d-.*', f):
                path = os.path.abspath(os.path.join(self.root, f))
                file = os.path.join(path, os.path.basename(path) + '.md')
                if not os.path.exists(file):
                    print('error: folder {} has not {}'.format(f, file))
                    error = True

        self.assertEqual(False, error)

    def test_all_images_are_used(self):
        error = False

        for f in self.md_files:
            path = os.path.dirname(os.path.abspath(f))
            if not os.path.exists(path + "/pix"):
                continue

            existing_images = gglob(path, "*.png")  + gglob(path, "*.jpg") +\
                         gglob(path, "*.jpeg") + gglob(path, "*.gif") +\
                         gglob(path, "*.svg")

            mentioned_images = get_grep(cat(f), "!\[\]\(([^)]*)\)")

            for img in mentioned_images:
                full_path = os.path.join(path, img).replace('/./', '/').replace('\./pix/', '\\pix\\')
                if os.path.exists(full_path) and (full_path in existing_images):
                    existing_images.remove(full_path)

            if len(existing_images) > 0:
                print("images are not used: ")
                for i in existing_images:
                    print('      - {}'.format(i))
                error = True

        self.assertEqual(False, error)

    def test_all_images_exist(self):
        error = False

        for f in self.md_files:
            path = os.path.dirname(os.path.abspath(f))
            m = get_grep(cat(f), "!\[\]\(([^)]*)\)")
            for img in m:
                full_path = os.path.join(path, img).replace('/./', '/')
                if not os.path.exists(full_path):
                    print('error: {} does not exist'.format(full_path))
                    error = True

        self.assertEqual(False, error)

if __name__ == '__main__':
    print("Starting validation process:")
    unittest.main()
