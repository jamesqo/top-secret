#!/usr/bin/env python3

# TODO: Change the name of this project to TopSecret

import sys
from tempfile import NamedTemporaryFile

from getch import getch

HEADER = """
Welcome to [REDACTED]!
"""

CONFIG_PATH = '~/.redacted'

def read_config():
    with open(CONFIG_PATH, 'r', encoding='utf-8') as config_file:
        lines = config_file.strip().splitlines()
        keys, values = zip(*[line.split(': ') for line in lines])
        numbers = [int(key) for key in keys]
        paths = values

        return {number: path for number, path in zip(numbers, paths)}

def num_entries():
    config = read_config()
    if config is None:
        return 0

    return len(config)

def main():
    print(HEADER)
    with NamedTemporaryFile(mode='w+') as tempfile:
        wordlen = 0

        while True:
            ch = getch()
            if ord(ch) == 27: # ESC
                raise KeyboardInterrupt()

            if ord(ch) not in range(32, 126 + 1): # NOTE: Delete should be ignored
                continue

            if ch.isspace():
                sys.stdout.write('\r' + (' ' * wordlen) + ('\b' * wordlen))
                sys.stdout.flush()
                wordlen = 0
            else:
                sys.stdout.write(ch)
                sys.stdout.flush()
                wordlen += 1

            tempfile.write(ch)

if __name__ == '__main__':
    main()
