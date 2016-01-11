from xml.dom.minidom import Element
from xml.dom.pulldom import CHARACTERS, START_ELEMENT, parseString, END_ELEMENT, parse

from xml_collation.EditGraphAligner import EditGraphAligner

"""
 XML hierarchy collation using a pull parser and minidom
 @author: Ronald Haentjens Dekker
"""


def convert_xml_file_into_string(xml):
    # init input
    doc = parse(xml)
    # init output
    # NOTE: we start with output as a string
    # we might want to make the tokens more complex to store the original location in xpath form
    output = ""
    for event, node in doc:
        if event == CHARACTERS:
            continue

        # debug
        # print(event, node)

        if event == START_ELEMENT:
            output += " " + node.localName

    return output

output1 = convert_xml_file_into_string("../xml_source_transcriptions/liefde-tsa.xml")
output2 = convert_xml_file_into_string("../xml_source_transcriptions/liefde-tsb.xml")

print(output1)
print(output2)

# hmmm above we plak everything aan elkaar en hier slopen we het weer
# we need to tokenize both strings
tokens1 = output1.split()
tokens2 = output2.split()
# TODO: tokens needs to be made more unique (localName can be repeated)

print(tokens1)
print(tokens2)

aligner = EditGraphAligner()
alignment = aligner.align_table(tokens1, tokens2, None)

print(alignment.keys())

