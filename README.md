# yaml2patchouli

Create a [Patchouli](https://github.com/Vazkii/Patchouli/) book from a single [YAML](https://yaml.org/) file.

## Why?

[Patchouli](https://github.com/Vazkii/Patchouli/) is an awesome mod for Minecraft that lets you create beautiful in-game books using just json files.  While that is decidedly easier than hacking away at Java code, looking at and managing the specific names and locations of a couple dozen or so json files is hardly fun.

I created `yaml2patchouli` to ease the pain of dealing with a bunch of json files while creating/editing a Patchouli book.  Now, an entire book can be represented with a single [YAML](https://yaml.org/) file that is arguably easier to reason about.

As far as I know, `yaml2patchouli` has only been tested on Linux.  It doesn't depend on any Linux-specific things so it should work fine on macOS or Windows.  I would love to know if you run this on another OS!

## Installation

Installing from source is relatively easy, `python3-yaml` is a required package:

    # Install with pip from a clone of this source code:
    make

    # Install with pip from a zip of this source code:
    pip3 install --user https://github.com/hristoast/yaml2patchouli/archive/master.zip

    # You can also run y2p straight from the source directory, without installing:
    python3 ./y2p/y2p.py --help

When installing with `pip`, two binaries are installed: `y2p` and `yaml2patchouli`.

## Making A YAML File

The file's schema will closely resemble that seen in `book.json`, see [this example file with lots of comments](./sample-book.yml) for more information.

You can get started by copying [the example in this repository](./sample-book.yml) and editing as needed.

## Usage

`y2p` takes at minimum one argument, which is the YAML file it should read to create a book.

    # Create the given book in a MultiMC instance, don't wrap output if the
    # terminal is too small
    y2p --verbose --out ~/.multimc/instances/MY_COOL_INSTANCE/.minecraft my-cool-patchouli-book.yml

    # Create the given book in a MultiMC instance, erase existing book files first
    y2p --clean --out ~/.multimc/instances/MY_COOL_INSTANCE/.minecraft my-cool-patchouli-book.yml

    # Create the given book in a plain Minecraft install
    y2p --out ~/.minecraft my-cool-patchouli-book.yml

    # Create the given book in a plain Minecraft install, erase existing files
    # and don't output anything
    y2p -C -q -o ~/.minecraft my-cool-patchouli-book.yml

    # Create the given book in your current working directory, don't word wrap
    # the ouput if the terminal is too small
    y2p -V my-cool-patchouli-book.yml

Please run `y2p --help` to see all options, it doesn't do a whole lot more than you see above.

## Caveats

* Error handling could possibly be better; my limited use case for `y2p` will surely not expose all bugs.
* Currently, `y2p` doesn't do any schema validation at all.  So you can create a YAML file with garbage, and as long as it's valid YAML `y2p` will happily try to create a book from it.  More testing and validations is needed here, it would be nice to at least ensure required fields are present.
* If you create a category or an entry with `y2p` and then remove it, `y2p` will not manage the removal of the old json file.  Until this functionality is added (if it ever is), it should be just fine to delete the entire book directory and just generate it again.
