#!/usr/bin/python3
import argparse
import json
import logging
import os
import shutil
import sys
import textwrap
PROG = sys.argv[0].split('/')[-1]
try:
    import yaml
except ImportError:
    sys.stderr.write("The python3-yaml package is required to use {}!\n".format(PROG))
    sys.exit(1)
DESC = "Create Patchouli books from a single YAML file."
LOGFMT = '%(asctime)s | %(message)s'
__version__ = "0.2"


def create_book_dirs(book_name: str, entries: list, lang: str, out: str) -> None:
    book_dir = os.path.join(out, "patchouli_books", book_name)

    for path in os.path.join(book_dir, lang, "categories"), \
            os.path.join(book_dir, lang, "entries"), \
            os.path.join(book_dir, lang, "templates"):
        try:
            os.makedirs(path)
        except FileExistsError:
            # It already exists, cool.
            pass
        except PermissionError:
            error_and_die("The given out dir is not writeable!")

    for e in entries:
        entry_name = format_name(e["name"])
        entry_dir = os.path.join(book_dir, lang, "entries", entry_name)
        try:
            os.makedirs(entry_dir)
        except FileExistsError:
            pass


def read_yaml(yaml_file: str) -> str:
    try:
        with open(yaml_file, 'r') as f:
            lines = f.readlines()
        return ' '.join(lines)
    except FileNotFoundError:
        error_and_die("The given YAML file ({}) was not a real file!".format(yaml_file))


def format_name(name: str) -> str:
    name = name.replace(" ", "_")
    return ''.join(a for a in name if a.isalnum() or a == "_").lower()


def write_book_json(name: str, data: str, out: str) -> None:
    book_json = os.path.join(out, "patchouli_books", name, "book.json")
    with open(book_json, 'w+') as f:
        for ln in data:
            f.write(ln)
        f.write("\n")


def write_thing(thing: dict, type: str, lang: str, name: str, out: str) -> None:
    if type == "category":
        file_name = format_name(thing["name"]) + "_category.json"
        path = os.path.join(out, "patchouli_books", name, lang, "categories", file_name)
    elif type == "entry":
        entry_name = format_name(thing["name"])
        file_name = entry_name + "_entry.json"
        path = os.path.join(out, "patchouli_books", name, lang, "entries", entry_name, file_name)
    elif type == "template":
        # TODO: support macros/templates
        print("TODO")
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


def emit_log(msg: str, level=None, *args, **kwargs) -> None:
    """Logging wrapper."""
    if not level:
        logger = logging.getLogger()
        level = logger.level
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
    parser.add_argument("--version", action="version", version=PROG + " " + __version__, help=argparse.SUPPRESS)
    options = parser.add_argument_group("Options")
    options.add_argument("-C", "--clean", action="store_true", help="Erase the book directory before generating.")
    options.add_argument("-o", "--out-dir",
                         help="Where the book files should be written to.  Defaults to $PWD if not provided")
    options.add_argument("-q", "--quiet", action="store_true",
                         help="Don't print messages, just create the books files and directories.")
    options.add_argument("-V", "--verbose", action="store_true", help="Don't ellipsize output, do word wrap.")
    return parser.parse_args()


def main() -> None:
    parsed = parse_argv()

    clean = False
    log_level = logging.INFO
    out_dir = None
    quiet = False
    verbose = False
    yaml_file = None

    if parsed.clean:
        clean = True
    if parsed.out_dir:
        out_dir = parsed.out_dir
    if parsed.quiet:
        quiet = True
    if parsed.verbose:
        verbose = True
    if parsed.yaml_file:
        yaml_file = os.path.abspath(parsed.yaml_file)

    if not out_dir:
        # TODO: is this brittle?
        out_dir = os.getenv("PWD")

    # Absolute paths are preferred and more explicit
    out_dir = os.path.abspath(out_dir)

    if quiet:
        log_level = logging.FATAL
    elif verbose:
        log_level = logging.DEBUG

    init_logging(log_level)

    emit_log("Getting data from '" + yaml_file + "'")
    book_data = yaml.load(read_yaml(yaml_file))
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

    book_dir = os.path.join(out_dir, "patchouli_books", book_name)
    if clean:
        emit_log("Removing book directories in '" + book_dir + "'")
        shutil.rmtree(book_dir)

    emit_log("Creating book directories in '" + book_dir + "'")
    create_book_dirs(book_name, entries, book_lang, out_dir)

    emit_log("Writing 'book.json'")
    write_book_json(book_name, json.dumps(book_data, indent=4, sort_keys=True), out_dir)

    emit_log("Writing category files: " + ', '.join(cat["name"] for cat in categories).rstrip(", "))
    for c in categories:
        write_thing(c, "category", book_lang, book_name, out_dir)

    emit_log("Writing entry files: " + ', '.join(ent["name"] for ent in entries).rstrip(", "))
    for e in entries:
        write_thing(e, "entry", book_lang, book_name, out_dir)

    emit_log("Completed generation of the book '{0}' into the directory '{1}'!".format(book_name, out_dir))


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("  CTRL-C Received, exiting...")
        sys.exit(2)
