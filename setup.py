#!/usr/bin/env python3
import re

from setuptools import find_packages, setup


with open('y2p/y2p.py', 'r') as f:
    __version__ = re.search(
        r'__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
        f.read()).group(1)

with open('README.md', 'r') as r:
    readme = ' '.join(r.readlines())
    r.close()

setup(
    name="yaml2patchouli",
    version=__version__,
    author="Hristos N. Triantafillou",
    author_email="<y2p@hristos.lol>",
    maintainer="Hristos N. Triantafillou",
    maintainer_email="<y2p@hristos.lol>",
    url="https://git.sr.ht/~hristoast/yaml2patchouli",
    description="Create Patchouli books from a single YAML file.",
    long_description=readme,
    download_url="https://git.sr.ht/~hristoast/yaml2patchouli",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'License :: OSI Approved :: GNU General Public License v3 or later'
        '(GPLv3+)',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Games/Entertainment',
        'Topic :: Utilities'],
    platforms=['linux2'],
    license="GPLv3+",
    packages=find_packages(),
    entry_points={'console_scripts':
                  ['y2p = y2p.y2p:main',
                   'yaml2patchouli = y2p.y2p:main', ]})
