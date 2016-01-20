from xml.dom.minidom import Element
from xml.dom.pulldom import CHARACTERS, START_ELEMENT, parseString, END_ELEMENT, parse

from xml_collation.EditGraphAligner import EditGraphAligner

"""
 XML hierarchy collation using a pull parser and minidom
 @author: Ronald Haentjens Dekker
"""


class Token(object):
    def __init__(self, content):
        self.content = content

    def __str__(self):
        return self.content

    def __repr__(self):
        return self.content


def convert_xml_file_into_string(xml):
    # init input
    doc = parse(xml)
    # init output
    # NOTE: tokens objects are made so to make them unique (localName can be repeated)
    # NOTE: we might want to make the tokens more complex to store the original location in xpath form
    output = []
    for event, node in doc:
        if event == CHARACTERS:
            continue

        # debug
        # print(event, node)

        if event == START_ELEMENT:
            output.append(Token(node.localName))

    return output

output1 = convert_xml_file_into_string("../xml_source_transcriptions/liefde-tsa.xml")
output2 = convert_xml_file_into_string("../xml_source_transcriptions/liefde-tsb.xml")

print(output1)
print(output2)

tokens1 = output1
tokens2 = output2

aligner = EditGraphAligner()
alignment = aligner.align_table(tokens1, tokens2, None)

print(alignment.keys())

