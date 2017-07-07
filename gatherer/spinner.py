import itertools
import sys


class Spinner(object):
    def __init__(self):
        self.spinner = itertools.cycle(['-', '\\', '|', '/'])

    def spin(self):
        sys.stdout.write(self.spinner.__next__())
        sys.stdout.flush()
        sys.stdout.write('\b')