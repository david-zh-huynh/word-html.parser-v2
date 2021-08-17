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
        print('Done! Output written to: {}\n'.format(filename))


# edit html file and modify
def custom_edit_html(filename):
    # open html file
    spoon = BeautifulSoup(open(filename), 'lxml')

    # find html
    html = spoon.find('html')
    if len(html) > 0:
        # remove/unwrap html tag
        html.unwrap()

    # find body
    body = spoon.find('body')
    if len(body) > 0:
        # remove/unwrap body tag
        body.unwrap()

    # unwrap p tag in li objects
    for li_tag in spoon.find_all('li'):
        if li_tag:
            li_children = li_tag.findChildren('p', recursive=False)
            if li_children:
                for child in li_children:
                    child.unwrap()
        else:
            print('no link items found, all good. program continues...')

    # find links in paragraphs
    for p_tag in spoon.find_all('p'):
        if p_tag:
            p_a_tag = p_tag.findChildren('a')
            if p_a_tag:
                for p_a_u_child in p_a_tag:
                    underlined = p_a_u_child.findChildren('u')
                    if underlined:
                        for underlined_link in underlined:
                            underlined_link.unwrap()
                # find bolded links in paragraphs
                for p_a_b_child in p_a_tag:
                    bolded = p_a_b_child.findChildren('strong')
                    if bolded:
                        for strong_link in bolded:
                            strong_link.unwrap()
        else:
            print('no paragraphs found, program continues')

    # find images in paragraphs
    for img_p_tag in spoon.find_all('p'):
        if img_p_tag:
            img_tag = img_p_tag.findChildren('img')
            if img_tag:
                img_p_tag.unwrap()

    # remove colgroup element from tables
    for table_colgroup_tag in spoon.find_all('table'):
        if table_colgroup_tag:
            colgroup_tag = table_colgroup_tag.find('colgroup')
            if colgroup_tag:
                print('colgroup element found')
                colgroup_tag.decompose()
                print('colgroup element decomposed/removed')
            else:
                print('no colgroup found, program continues...')

    # remove strong tags in th elements
    for th_tag_rm in spoon.find_all('th'):
        if th_tag_rm:
            th_tag_rm_strong = th_tag_rm.findChildren('strong')
            if th_tag_rm_strong:
                for rm_th_bold in th_tag_rm_strong:
                    rm_th_bold.unwrap()
        else:
            print('no th tags found, program continues...')

        # remove strong tags in th elements
        for td_tag_rm in spoon.find_all('td'):
            if td_tag_rm:
                td_tag_rm_strong = td_tag_rm.findChildren('strong')
                if td_tag_rm_strong:
                    for rm_td_bold in td_tag_rm_strong:
                        rm_td_bold.unwrap()
            else:
                print('no td tags found, program continues...')

    # Create dictionary for tables
    for table in spoon.find_all('table'):
        if table:
            meta_dict = {}
            cell_counter = 0
            a = iter((spoon.find_all('th') + spoon.find_all('td')))
            key = ""
            value = ""
            for cells in a:
                raw_cells = cells.text
                if raw_cells:
                    cell_counter += 1
                    if cell_counter % 2 == 1:
                        key = raw_cells
                    if cell_counter % 2 == 0:
                        value = raw_cells
                else:
                    print('table appears to be empty...')
                meta_dict[key] = value
        else:
            print('no table found, program continues...')
        # print key, value
        """for i in meta_dict:
            print(i + ": " + meta_dict[i])"""

    # Create dictionary and nummerate tags with exceptions for li, links and images
    dict_backend = {}
    lib = {'h2', 'h3', 'h4', 'h5', 'p', 'ol', 'ul', 'img'}
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
