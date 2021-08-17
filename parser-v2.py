import argparse
import os
import time
from pprint import pprint

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
        print('Done! Output written to: {}\n'.format(filename))


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

    # unwrap p tag in li objects
    """
    for li in spoon.find('li'):
        print('link item found')
        li_children = li.findChildren("p", recursive=False)
        for li_p in li_children:
            print('p tag in link item unwrapped')
            li_p.p.unwrap()"""

    # find links in paragraph
    for p_tag in spoon.find_all('p'):
        if p_tag:
            print('paragraphs found')
            p_a_tag = p_tag.findChildren('a')
            print('finding a tag children')
            if p_a_tag:
                print('link in paragraph found')
                for child in p_a_tag:
                    underlined = child.findChildren('u')
                    print('finding underlined text in link tag')
                    if underlined:
                        print('link with underlined text found')
                        for underlined_text in underlined:
                            print('unwrapped underlining for link')
                            underlined_text.unwrap()
                    else:
                        print('no underlined text in link found')
            else:
                print('no link found in paragraph, all good. program continues...')
        else:
            print('no paragraphs found, program continues')

    # remove strong tags in th elements
    for th_tag_rm in spoon.find_all('th'):
        if th_tag_rm:
            th_tag_rm_strong = th_tag_rm.findChildren('strong')
            if th_tag_rm_strong:
                for rm_th_bold in th_tag_rm_strong:
                    rm_th_bold.unwrap()
        else:
            return 'no th tags found, program continues...'

        # remove strong tags in th elements
        for td_tag_rm in spoon.find_all('td'):
            if td_tag_rm:
                td_tag_rm_strong = td_tag_rm.findChildren('strong')
                if td_tag_rm_strong:
                    for rm_td_bold in td_tag_rm_strong:
                        rm_td_bold.unwrap()
            else:
                return 'no td tags found, program continues...'

    # Create dictionary for
    for table in spoon.find_all('table'):
        if table:
            print('table found')
            meta_dict = {}
            cell_counter = 0
            for cells in spoon.find_all('th') + spoon.find_all('td'):
                raw_cells = cells.text.split('\n')
                cell_list = [raw_cells]
                cell_counter += 1
                pprint(cell_list)

        else:
            return 'no table found, program continues...'

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

    encoding = spoon.original_encoding or 'utf-8'
    print("encoding: " + encoding)

    # print(dict_backend)
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
    # convert
    convert_to_html(args.path)

    # parse and edit
    print('please insert name of newly converted html file:')
    htmlfile_name = input()
    custom_edit_html(htmlfile_name)
    t.stop()
