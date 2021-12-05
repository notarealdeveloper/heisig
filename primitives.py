#!/usr/bin/env python3

"""
    A parser for the "primitives" file
    in the github repository at:

    https://github.com/Yomin/rtk-dicts

    This file only contains RTK Kanji,
    so it will need to be combined with
    data mapping RTK characters to their
    corresponding RTH and RSH Hanzi in
    order to port the primitives here
    to their Chinese counterparts.
"""

__all__ = [
    'get_primitives',
]

import os

RTK_DICTS_URL = 'https://github.com/Yomin/rtk-dicts'

def ensure_have_primitives_file():
    if not os.path.exists('rtk-dicts/primitives'):
        os.system(f"git clone {RTK_DICTS_URL}")
    return f"rtk-dicts/primitives"

def get_primitive_lines():
    path = ensure_have_primitives_file()
    with open(path) as fp:
        content = fp.read()

    index = content.find('0001:')
    content = content[index:]
    return content.splitlines()

class KanjiWithPrimitives:

    def __new__(cls, line):
        n, i, c, mean, compmean, comps = line.split(':')
        self = object.__new__(cls)
        self.num = n
        self.unknown = i
        self.char = c
        self.meaning = mean
        self.component_meaning = compmean
        self.components = comps.split('/')
        return self

    def __repr__(self):
        return ' | '.join([
            self.num,
            self.char,
            self.meaning,
            self.component_meaning,
            '... '.join(self.components),
        ])

def can_parse(line):
    try:
        n, i, c, mean, compmean, comps = line.split(':')
        return True
    except:
        return False

def get_primitives():
    lines = get_primitive_lines()
    characters = [KanjiWithPrimitives(line) for line in lines if can_parse(line)]
    primitives = {c.char: c for c in characters}
    return primitives
