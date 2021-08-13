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
    # open html file
    spoon = BeautifulSoup(open(filename), 'lxml')

    # find html
    html = spoon.find('html')
    if len(html) > 0:
        # remove/unwrap html tag
        print('html found and unwrapped')
        html.unwrap()
    else:
        print('no html tag found, all good. program continues...')

    # find body
    body = spoon.find('body')
    if len(body) > 0:
        # remove/unwrap body tag
        print('body found and unwrapped')
        body.unwrap()

    else:
        print('no body tag found, all good. program continues...')

    # find links in paragraph
    find_links = spoon.findAll('p')
    # link_records = []
    for find_link in find_links:
        print('paragraphs found')
        underlined_links = find_link.findChildren('a', recursive=False)
        if underlined_links:
            for underlined_link in underlined_links:
                underlined_link_text = underlined_link.findChildren('u')
                print('unwrapped underlining for link')
                underlined_link_text.u.unwrap()
        else:
            print('no link found in paragraph, all good. program continues...')

    # Create dictionary and nummerate tags with exceptions for li, links and images
    dict_backend = {}
    lib = {'h1', 'h2', 'h3', 'h4', 'h5', 'p', 'ol', 'ul', 'img', 'table', 'a'}
    dic_html = spoon.find_all(lib)
    id_counter = 0
    # for loop to iterate through all tags mentioned above
    for i in dic_html:
        id_counter += 1

        # h1
        if str(i).startswith("<h1"):
            dict_backend['h1'] = i.get_text()
            pass
        else:
            # create id counter
            i['id'] = id_counter

            # ul
            if i.name == 'ul':
                # print("ul found :" + str(i.prettify()))
                dict_backend[id_counter] = str(i.prettify())
            else:
                dict_backend[id_counter] = i.get_text()

            # ol
            if i.name == 'ol':
                # print("ol found :" + str(i.prettify()))
                dict_backend[id_counter] = str(i.prettify())
            else:
                dict_backend[id_counter] = i.get_text()

            # Table
            if i.name == 'table':
                # print("table found :" + str(i.prettify()))
                dict_backend[id_counter] = str(i.prettify())
            else:
                dict_backend[id_counter] = i.get_text()

    print(dict_backend)
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
