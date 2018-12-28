#!/usr/bin/env -S python3 -Wd
import json
import os
import sys
import yaml

from y2p.core import create_book_dirs, read_yaml, write_book_json
from tempfile import mkdtemp
from unittest import TestCase, main as test_main


class Y2pTestCase(TestCase):
    def setUp(self):
        self.out = mkdtemp()
        self.yml = os.path.abspath(
            os.path.join(os.path.dirname(sys.argv[0]),
                         "sample-book.yml"))
        create_book_dirs("TestBook", "en_us", self.out)

    def test_create_book_dirs(self):
        self.assertTrue(os.path.isdir(
            os.path.join(self.out, "patchouli_books")))
        self.assertTrue(os.path.isdir(
            os.path.join(self.out, "patchouli_books", "TestBook")))
        self.assertTrue(os.path.isdir(
            os.path.join(self.out, "patchouli_books", "TestBook", "en_us")))
        self.assertTrue(os.path.isdir(
            os.path.join(self.out, "patchouli_books", "TestBook", "en_us",
                         "categories")))
        self.assertTrue(os.path.isdir(
            os.path.join(self.out, "patchouli_books", "TestBook", "en_us",
                         "entries")))

    def test_read_yaml(self):
        yml = read_yaml(self.yml)
        d = yaml.load(yml)[0]
        self.assertTrue(yml.startswith("-"))
        self.assertIsInstance(d, dict)

    def test_write_book_json(self):
        data = yaml.load(read_yaml(self.yml))[0]
        del data["book_name"]
        del data["entries"]
        del data["categories"]
        write_book_json("TestBook", json.dumps(data), self.out)
        _file = os.path.join(
            self.out,
            "patchouli_books",
            "TestBook",
            "book.json")
        self.assertTrue(os.path.isfile(_file))
        with open(_file, 'r') as f:
            s = ' '.join(f.readlines())
            j = json.loads(s)
        self.assertIsInstance(j, dict)

    def test_write_thing_cat(self):
        # TODO: test write_thing with a category
        pass

    def test_write_thing_entry(self):
        # TODO: test write_thing with an entry
        pass


if __name__ == '__main__':
    test_main()
