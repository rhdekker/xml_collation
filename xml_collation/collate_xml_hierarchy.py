from xml.dom.minidom import Element
from xml.dom.pulldom import CHARACTERS, START_ELEMENT, parseString, END_ELEMENT, parse

"""
 XML hierarchy collation using a pull parser and minidom
 @author: Ronald Haentjens Dekker
"""


# init input
doc = parse("../xml_source_transcriptions/liefde-tsa.xml")

for event, node in doc:
    if event != CHARACTERS:
        # debug
        print(event, node)




# # init output
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
# print(output.toxml())