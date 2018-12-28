#!/usr/bin/python3
import argparse
import json
import logging
import os
import sys
import textwrap
import yaml


DESC = "Create Patchouli books from a single YAML file."
LOGFMT = '%(asctime)s | %(message)s'
PROG = sys.argv[0].split('/')[-1]


def create_book_dirs(name: str, lang: str, out: str) -> None:
    book_dir = os.path.join(out, "patchouli_books", name)
    for path in os.path.join(book_dir, lang, "categories"), \
            os.path.join(book_dir, lang, "entries"):
        try:
            os.makedirs(path)
        except FileExistsError:
            pass


def read_yaml(yaml_file: str) -> str:
    with open(yaml_file, 'r') as f:
        lines = f.readlines()
    return ' '.join(lines)


def write_book_json(name: str, data: str, out: str) -> None:
    book_json = os.path.join(out, "patchouli_books", name, "book.json")
    with open(book_json, 'w+') as f:
        for ln in data:
            f.write(ln)
        f.write("\n")


def write_thing(thing: dict, type: str, lang: str, name: str, out: str):
    if type == "category":
        file_name = ''.join(a for a in thing["name"] if a.isalnum()) + "_category.json"
        path = os.path.join(out, "patchouli_books", name, lang, "categories", file_name)
    elif type == "entry":
        file_name = ''.join(a for a in thing["name"] if a.isalnum()) + "_entry.json"
        path = os.path.join(out, "patchouli_books", name, lang, "entries", file_name)
    with open(path, 'w+') as f:
        for line in json.dumps(thing, indent=4, sort_keys=True):
            f.write(line)
        f.write("\n")


def get_terminal_dims() -> tuple:
    tty = os.popen('stty size', 'r')
    try:
        y, x = tty.read().split()
    except ValueError:
        y, x = ["0", "0"]
    tty.close()
    return x, y


def emit_log(msg: str, level=logging.INFO, *args, **kwargs) -> None:
    """Logging wrapper."""
    if not level == logging.DEBUG and int(get_terminal_dims()[0]) > 0:
        _num = 31  # magic number to get how many actual columns we have to work with
        msg = textwrap.shorten(msg, width=int(get_terminal_dims()[0]) - _num,
                               placeholder=" ...")

    if level == logging.DEBUG:
        logging.debug(msg, *args, **kwargs)
    elif level == logging.INFO:
        logging.info(msg, *args, **kwargs)
    elif level == logging.WARN:
        logging.warn(msg, *args, **kwargs)
    elif level == logging.ERROR:
        logging.error(msg, *args, **kwargs)


def error_and_die(msg: str) -> SystemExit:
    """Call sys.ext(1) with a formatted error message."""
    emit_log("ERROR: " + msg, level=logging.ERROR)
    sys.exit(1)


def init_logging(log_lvl: str) -> bool:
    """Wrapper for initializing logging."""
    logging.basicConfig(format=LOGFMT, level=log_lvl, stream=sys.stdout)


def parse_argv() -> None:
    """Set up args and parse them."""
    parser = argparse.ArgumentParser(description=DESC, prog=PROG)
    parser.add_argument("yaml_file", help="YAML file to be read.", metavar="<YAML file>")
    options = parser.add_argument_group("Options")
    options.add_argument("-o", "--out-dir",
                         help="Where the book files should be written to.  Defaults to $PWD if not provided")
    options.add_argument("-q", "--quiet", action="store_true",
                         help="Don't print messages, just create the books files and directories.")
    return parser.parse_args()


def main() -> None:
    parsed = parse_argv()

    out_dir = None
    quiet = False
    yaml_file = None

    if parsed.out_dir:
        out_dir = parsed.out_dir
    if parsed.quiet:
        quiet = True
    if parsed.yaml_file:
        yaml_file = parsed.yaml_file

    if not out_dir:
        # TODO: is this brittle?
        out_dir = os.getenv("PWD")

    if quiet:
        init_logging(logging.FATAL)
    else:
        init_logging(logging.INFO)

    emit_log("Getting data from '" + yaml_file + "'")
    book_data = yaml.load(read_yaml(yaml_file))[0]
    book_name = book_data.get("book_name")
    del book_data["book_name"]
    book_lang = book_data.get("lang")

    if not book_lang:
        book_lang = "en_US"

    book_lang = book_lang.lower()

    categories = book_data.get("categories")
    del book_data["categories"]

    entries = book_data.get("entries")
    del book_data["entries"]

    emit_log("Creating book directories in '" + out_dir + "'")
    create_book_dirs(book_name, book_lang, out_dir)

    emit_log("Writing 'book.json'")
    write_book_json(book_name, json.dumps(book_data, indent=4, sort_keys=True), out_dir)

    emit_log("Writing category files")
    for c in categories:
        write_thing(c, "category", book_lang, book_name, out_dir)

    emit_log("Writing entry files")
    for e in entries:
        write_thing(e, "entry", book_lang, book_name, out_dir)

    emit_log("Done!")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("  CTRL-C Received, exiting...")
        sys.exit(2)
