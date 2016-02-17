import re
from xml.dom.minidom import getDOMImplementation
from xml.dom.pulldom import CHARACTERS, START_ELEMENT, parse, END_ELEMENT

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


class TextToken(Token):
    pass

class ElementToken(Token):
    pass


def tokenize_text(data):
    return (TextToken(content) for content in re.findall(r'\w+|[^\w\s]+', data))


def convert_xml_file_into_tokens(xml):
    # init input
    doc = parse(xml)
    # init output
    # NOTE: tokens objects are made so to make them unique (localName can be repeated)
    # NOTE: we might want to make the tokens more complex to store the original location in xpath form
    tokens = []
    for event, node in doc:
        # debug
        # print(event, node)
        if event == CHARACTERS:
            tokens.extend(tokenize_text(node.data))

        elif event == START_ELEMENT:
            tokens.append(ElementToken(node.localName))

        elif event == END_ELEMENT:
            tokens.append(ElementToken("/"+node.localName))

    return tokens


def print_superwitness(superwitness):
    # We want to show the result
    # we traverse over the tokens in the segments:
    result = []
    for extended_token in superwitness:
        representation = ""
        if not extended_token.aligned:
            if extended_token.addition:
                representation += "+"
            else:
                representation += "-"
        result.append(", ".join([representation+extended_token.token.content]))

    print(result)

#
# def process_aligned_text_nodes:



def convert_superwitness_into_result_dom(superwitness):
    # create new document
    impl = getDOMImplementation()
    newdoc = impl.createDocument(None, "root", None)
    root = newdoc.documentElement
    latest = root
    # process the segments and fill document
    for extended_token in superwitness:
        # here we handle aligned segments
        if extended_token.aligned:
            # get the token inside the extended_token
            token = extended_token.token
            if isinstance(token, TextToken):
                t = newdoc.createTextNode(token.content)
                latest.appendChild(t)
            elif token.content.startswith("/"):
                latest = latest.parentNode
            else:
                # print("adding "+token.content+" to "+str(latest))
                node = newdoc.createElement(token.content)
                latest.appendChild(node)
                latest = node
        # here we handle added segments
        elif extended_token.addition:
            # open wrapper
            token = extended_token.token
            if isinstance(token, TextToken):
                t = newdoc.createElement("cx:addition")
                latest.appendChild(t)
                # content of text node as child to node cx:addition (leaf node)
                t.appendChild(newdoc.createTextNode(token.content))
        else:
            token = extended_token.token
            if isinstance(token, ElementToken):
                if token.content.startswith("/"):
                    latest = latest.parentNode
                else:
                    # print("adding "+token.content+" to "+str(latest))
                    node = newdoc.createElement(token.content)
                    # set attribute to mark change!
                    if extended_token.addition:
                        node.setAttribute("CX", "addition")
                    else:
                        node.setAttribute("CX", "omission")
                    latest.appendChild(node)
                    latest = node
    return root

# convert XML files into tokens
tokens1 = convert_xml_file_into_tokens("../xml_source_transcriptions/ts-fol-test-small.xml")
tokens2 = convert_xml_file_into_tokens("../xml_source_transcriptions/tsq-test-small.xml")

print(tokens1)
print(tokens2)

# align sequences of tokens. Results in segments.
aligner = EditGraphAligner()
alignment = aligner.align(tokens1, tokens2)
superwitness = aligner.superwitness

print_superwitness(superwitness)

# group aligned text tokens in one segment

# convert segments in dom tree
root = convert_superwitness_into_result_dom(superwitness)

print(root.toprettyxml())

