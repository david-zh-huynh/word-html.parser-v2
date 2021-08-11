import argparse
import os
import sys

import pypandoc
import time


# convert docx/pdf to html


def convert_to_html(filename):
    output = pypandoc.convert_file(filename, "html")

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
        # close file
        sys.stdout.close()

        print("Done! Output written to: {}\n".format(filename))


# parse generated html into useable format


# output results
if __name__ == "__main__":
    t0 = time.perf_counter()
    parser = argparse.ArgumentParser(
        description="Convert a Word document to an HTML document."
    )
    parser.add_argument("path", type=str, help="Path to your word document")
    args = parser.parse_args()
    convert_to_html(args.path)
    t1 = time.perf_counter()
    print(f"Generated in {t1 - t0:0.4f} seconds")
