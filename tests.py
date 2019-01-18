#!/usr/bin/python3 -Wd
import json
import os
import shutil
import sys
import yaml

from y2p.y2p import create_book_dirs, read_yaml, write_book_json, write_thing
from tempfile import mkdtemp
from unittest import TestCase, main


class Y2pTestCase(TestCase):
    def setUp(self):
        self.out = mkdtemp()
        self.yml = os.path.abspath(
            os.path.join(os.path.dirname(sys.argv[0]),
                         "sample-book.yml"))
        self.data = yaml.load(read_yaml(self.yml))
        self.book_name = self.data["book_name"]
        self.cats = self.data["categories"]
        self.entries = self.data["entries"]
        self.lang = self.data["lang"]
        self.cat_file = os.path.join(
            self.out,
            "patchouli_books",
            self.book_name,
            self.lang,
            "categories",
            "one_category.json")
        self.entry_file = os.path.join(
            self.out,
            "patchouli_books",
            self.book_name,
            self.lang,
            "entries",
            "sample_entry_one",
            "sample_entry_one_entry.json")
        create_book_dirs(self.book_name, self.entries, self.lang, self.out)
        write_thing(
            self.data["categories"][0],
            "category",
            self.lang,
            self.book_name,
            self.out)
        write_thing(
            self.data["entries"][0],
            "entry",
            self.lang,
            self.book_name,
            self.out)

    def tearDown(self):
        shutil.rmtree(self.out)

    def test_create_book_dirs(self):
        self.assertTrue(os.path.isdir(
            os.path.join(self.out, "patchouli_books")))
        self.assertTrue(os.path.isdir(
            os.path.join(self.out, "patchouli_books", self.book_name)))
        self.assertTrue(os.path.isdir(
            os.path.join(self.out, "patchouli_books", self.book_name, self.lang)))
        self.assertTrue(os.path.isdir(
            os.path.join(self.out, "patchouli_books", self.book_name, self.lang,
                         "categories")))
        self.assertTrue(os.path.isdir(
            os.path.join(self.out, "patchouli_books", self.book_name, self.lang,
                         "entries")))
        # TODO: test for entry sub dir

    def test_read_yaml(self):
        yml = read_yaml(self.yml)
        d = yaml.load(yml)
        self.assertTrue(yml.startswith("---"))
        self.assertIsInstance(d, dict)

    def test_write_book_json(self):
        data = yaml.load(read_yaml(self.yml))
        del data["book_name"]
        del data["entries"]
        del data["categories"]
        write_book_json(self.book_name, json.dumps(data), self.out)
        _file = os.path.join(
            self.out,
            "patchouli_books",
            self.book_name,
            "book.json")
        self.assertTrue(os.path.isfile(_file))
        with open(_file, 'r') as f:
            s = ' '.join(f.readlines())
            j = json.loads(s)
        self.assertIsInstance(j, dict)

    def test_write_thing_cat(self):
        self.assertTrue(os.path.isfile(self.cat_file))

    def test_cat_file_content(self):
        with open(self.cat_file, 'r') as f:
            s = ' '.join(f.readlines())
        d = json.loads(s)
        self.assertTrue(d["name"] == "One")

    def test_write_thing_entry(self):
        self.assertTrue(os.path.isfile(self.entry_file))

    def test_entry_file_content(self):
        with open(self.entry_file, 'r') as f:
            s = ' '.join(f.readlines())
        d = json.loads(s)
        self.assertTrue(d["name"] == "Sample Entry One")

    # def test_write_thing_template(self):
    #     pass


if __name__ == '__main__':
    main()
