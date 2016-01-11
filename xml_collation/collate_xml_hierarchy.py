from xml.dom.minidom import Element
from xml.dom.pulldom import CHARACTERS, START_ELEMENT, parseString, END_ELEMENT, parse

"""
 XML hierarchy collation using a pull parser and minidom
 @author: Ronald Haentjens Dekker
"""


def convert_xml_file_into_string(xml):
    # init input
    doc = parse(xml)
    # init output
    # NOTE: we start with output as a string
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

#
# output = Element("output")
# open_elements = Stack()
# open_elements.push(output)
#
#     if event == START_ELEMENT:
#         # skip rdg element
#         if node.localName == "rdg":
#             continue
#         # in case of add deal with overlapping hierarchies
#         if node.localName == "add":
#             # set type attribute to start and add node as a child to output
#             node.setAttribute("type","start")
#             open_elements.peek().appendChild(node)
#         else:
#             open_elements.peek().appendChild(node)
#             open_elements.push(node)
#     if event == END_ELEMENT:
#         # skip rdg element
#         if node.localName == "rdg":
#             continue
#         # in case of add deal with overlapping hierarchies
#         if node.localName == "add":
#             # create a clone of the node and set type attribute to end and add node as a child to output
#             clone = node.cloneNode(False)
#             clone.setAttribute("type","end")
#             open_elements.peek().appendChild(clone)
#         else:
#             open_elements.pop()
#
