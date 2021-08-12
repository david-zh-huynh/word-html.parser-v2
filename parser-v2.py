import argparse
import os
import time

import pypandoc
from bs4 import BeautifulSoup


# convert docx/pdf to html
def convert_to_html(filename):
    # do conversion with pandoc
    output = pypandoc.convert_file(filename, "html")

    # replace "smart quotes".
    output = output.replace(u"\u2018", '&lsquo;').replace(u"\u2019", '&rsquo;')
    output = output.replace(u"\u201c", "&ldquo;").replace(u"\u201d", "&rdquo;")

    # write the output
    filename, ext = os.path.splitext(filename)
    filename = "{0}.html".format(filename)
    with open(filename, "w") as f:
        # Python 2 "fix". If this isn't a string, encode it.
        if type(output) is not str:
            output = output.encode("utf-8")

        f.write(output)
        print("Done! Output written to: {}\n".format(filename))


# edit html file and modify
def custom_edit_html(filename):
    spoon = BeautifulSoup(open(filename), 'lxml')

    ul = spoon.find('ul')
    ul_ls = ul.findChildren('li')
    for ul_l in ul_ls:
        ul_l.p.unwrap()

    with open(filename, "w") as edit_file:
        edit_file.write(str(spoon))


# time runtime of program

class TimerError(Exception):
    """A custom exception used to report errors in use of Timer class"""


class Timer:
    def __init__(self):
        self._start_time = None

    def start(self):
        """Start a new timer"""
        if self._start_time is not None:
            raise TimerError(f"Timer is running. Use .stop() to stop it")

        self._start_time = time.perf_counter()

    def stop(self):
        """Stop the timer, and report the elapsed time"""
        if self._start_time is None:
            raise TimerError(f"Timer is not running. Use .start() to start it")

        elapsed_time = time.perf_counter() - self._start_time
        self._start_time = None
        print(f"Elapsed time: {elapsed_time:0.4f} seconds")


def count_lines(input_file):
    lines = input_file.count('\n')
    return lines


# output results
if __name__ == "__main__":
    # initialize runtime_timer
    t = Timer()
    t.start()
    parser = argparse.ArgumentParser(
        description="Convert a Word document to an HTML document."
    )
    parser.add_argument("path", type=str, help="Path to your word document")
    args = parser.parse_args()
    convert_to_html(args.path)
    custom_edit_html("document.html")
    t.stop()
