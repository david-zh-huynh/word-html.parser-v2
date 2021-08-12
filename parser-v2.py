import argparse
import os
import sys
import time

import pypandoc
from bs4 import BeautifulSoup


# convert docx/pdf to html


def convert_to_html(filename):
    # start runtime counter
    t0 = time.perf_counter()
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
        # Implement HTMLParser

        # save console output to file
        sys.stdout = open("results.txt", "w")

        # provide content to html parser
        content = output

        soup = BeautifulSoup(content, 'lxml')

        list_items = soup.find_all("li")
        for list_item in list_items:
            print(list_item.text)

        # close file
        sys.stdout.close()

        print("Done! Output written to: {}\n".format(filename))
        t1 = time.perf_counter()
        print(f"Generated in {t1 - t0:0.4f} seconds")


# parse generated html into useable format


# output results
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Convert a Word document to an HTML document."
    )
    parser.add_argument("path", type=str, help="Path to your word document")
    args = parser.parse_args()
    convert_to_html(args.path)
