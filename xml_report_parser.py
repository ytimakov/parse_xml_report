#!/usr/bin/env python
from XMLReportConverter import xml_to_text
import sys
import time

if __name__ == "__main__":

    if len(sys.argv) < 3:
        print("file names are not defined")
        print("usage: " + sys.argv[0] + " input_xml_file output_text_file")
        print("sample: " + sys.argv[0] + " sample.xml sample.txt")
        print("exiting in 3 seconds...")
        time.sleep(3)
        sys.exit(1)

    input_xml_file = sys.argv[1]
    output_text_file = sys.argv[2]

    print(input_xml_file)
    print(output_text_file)

    xml_to_text(input_xml_file, output_text_file)