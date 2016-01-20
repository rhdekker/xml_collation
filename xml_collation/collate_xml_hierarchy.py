from xml.dom.pulldom import CHARACTERS, START_ELEMENT, parse

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


def convert_xml_file_into_tokens(xml):
    # init input
    doc = parse(xml)
    # init output
    # NOTE: tokens objects are made so to make them unique (localName can be repeated)
    # NOTE: we might want to make the tokens more complex to store the original location in xpath form
    tokens = []
    for event, node in doc:
        if event == CHARACTERS:
            continue

        # debug
        # print(event, node)

        if event == START_ELEMENT:
            tokens.append(Token(node.localName))

    return tokens

tokens1 = convert_xml_file_into_tokens("../xml_source_transcriptions/liefde-tsa.xml")
tokens2 = convert_xml_file_into_tokens("../xml_source_transcriptions/liefde-tsb.xml")

print(tokens1)
print(tokens2)


aligner = EditGraphAligner()
alignment = aligner.align_table(tokens1, tokens2, None)

# print(alignment.keys())

# We want to show the result
# NOTE: This code only shows aligned tokens and added tokens, omitted tokens are not yet shown!
# NOTE: Hmmm maybe the superbase is handy for this
# we traverse over the tokens in the second witness:
result = []
for token in tokens2:
    if token in alignment:
        result.append(token.content)
    else:
        result.append("+"+token.content)


print(result)
