#!/usr/bin/env python3

# TODO: Change the name of this project to TopSecret

import os
import sys
from tempfile import NamedTemporaryFile

from getch import getch

HEADER = """
Welcome to [REDACTED]!
Press Esc to exit
"""

FOOTER = """
Everything you wrote was stored somewhere! ...Or maybe not.
"""

PATHS_PATH = os.path.expanduser('~/.redacted')

def read_paths():
    try:
        with open(PATHS_PATH, 'r', encoding='utf-8') as paths_file:
            lines = paths_file.read().strip().splitlines()
            lines = [line.strip() for line in lines]
            keys, values = zip(*[line.split(': ') for line in lines])
            numbers = [int(key) for key in keys]
            paths = values

            return {number: path for number, path in zip(numbers, paths)}
    except FileNotFoundError:
        return None

def write_paths(number, path):
    with open(PATHS_PATH, 'a+', encoding='utf-8') as paths_file:
        line = f'{number}: {path}'
        paths_file.writelines(['', line])

def num_entries():
    paths = read_paths()
    if paths is None:
        return 0

    return len(paths)

def handle_cr(ch):
    if ch != '\r':
        return ch
    return os.linesep

def main():
    n = num_entries()

    print(HEADER)
    with NamedTemporaryFile(mode='w+', delete=False) as tempfile:
        write_paths(n + 1, tempfile.name)

        try:
            wordlen = 0
            while True:
                ch = getch()
                val = ord(ch)

                if val == 27: # ESC
                    raise KeyboardInterrupt()
                elif (ch == ' ' or ch == '\r' or ch == '\n' or ch == '\t'):
                    sys.stdout.write('\r' + (' ' * wordlen) + ('\b' * wordlen))
                    sys.stdout.flush()
                    wordlen = 0
                elif val not in range(32, 126 + 1): # NOTE: Delete should be ignored
                    continue
                else:
                    sys.stdout.write(ch)
                    sys.stdout.flush()
                    wordlen += 1

                tempfile.write(handle_cr(ch))
        except KeyboardInterrupt:
            print(FOOTER)

if __name__ == '__main__':
    main()
