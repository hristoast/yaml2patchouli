#!/usr/bin/env python3
from setuptools import find_packages, setup

setup(
    name="yaml2patchouli",
    version="0.1",
    author="Hristos N. Triantafillou",
    author_email="<me@hristos.lol>",
    maintainer="Hristos N. Triantafillou",
    maintainer_email="<me@hristos.lol>",
    url="https://hristos.lol/",
    description="Stupid tool for abstracting a Patchouli book as YAML.",
    long_description="Stupid tool for abstracting a Patchouli book as YAML.",
    download_url="https://hristos.lol/",
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
                  ['{0} = {0}.core:main'.format("y2p"),
                   '{0} = {1}.core:main'.format("yaml2patchouli", "y2p"), ]})
