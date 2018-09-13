#!/usr/bin/env python3

# TODO: Change the name of this project to TopSecret

from configparser import ConfigParser
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
CONFIG_PATH = os.path.expanduser('~/.redacted_conf')

def read_config():
    config = ConfigParser()
    config.read(CONFIG_PATH)
    return config

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
        paths_file.writelines(['\n', line])

def num_entries():
    paths = read_paths()
    if paths is None:
        return 0

    return len(paths)

def handle_cr(ch):
    if ch != '\r':
        return ch
    return os.linesep

def word_loop(output):
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

        output.write(handle_cr(ch))

def char_loop(output):
    while True:
        ch = getch()
        val = ord(ch)

        if val == 27: # ESC
            raise KeyboardInterrupt()
        elif (ch == ' ' or ch == '\r' or ch == '\n' or ch == '\t'):
            sys.stdout.write('\r \b')
            sys.stdout.flush()
        elif val not in range(32, 126 + 1): # NOTE: Delete should be ignored
            continue
        else:
            sys.stdout.write('\r \b' + ch)
            sys.stdout.flush()

        output.write(handle_cr(ch))

def main():
    opts = read_config()['options']
    n = num_entries()

    print(HEADER)
    with NamedTemporaryFile(mode='w+', delete=False) as tempfile:
        write_paths(n + 1, tempfile.name)

        try:
            if opts['char_by_char'] == 'yes':
                char_loop(tempfile)
            else:
                word_loop(tempfile)
        except KeyboardInterrupt:
            print(FOOTER)

if __name__ == '__main__':
    main()
