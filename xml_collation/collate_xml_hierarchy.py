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
            tokens.append(Token(node.localName))

        elif event == END_ELEMENT:
            tokens.append(Token("/"+node.localName))

    return tokens


def print_segments(segments):
    # We want to show the result
    # we traverse over the tokens in the segments:
    result = []
    for segment in segments:
        representation = ""
        if not segment.aligned:
            if segment.addition:
                representation += "+"
            else:
                representation += "-"
        result.append(", ".join([representation+token.content for token in segment.tokens]))

    print(result)


def convert_segments_into_result_dom(segments):
    # create new document
    impl = getDOMImplementation()
    newdoc = impl.createDocument(None, "root", None)
    root = newdoc.documentElement
    latest = root
    # process the segments and fill document
    for segment in segments:
        # for now we only handle aligned segments
        if segment.aligned:
            for token in segment.tokens:
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
        else:
            for token in segment.tokens:
                # skip text nodes in case of a change for now
                if not isinstance(token, TextToken):
                    if token.content.startswith("/"):
                        latest = latest.parentNode
                    else:
                        # print("adding "+token.content+" to "+str(latest))
                        node = newdoc.createElement(token.content)
                        # set attribute to mark change!
                        if segment.addition:
                            node.setAttribute("CX", "addition")
                        else:
                            node.setAttribute("CX", "omission")
                        latest.appendChild(node)
                        latest = node
    return root

# convert XML files into tokens
tokens1 = convert_xml_file_into_tokens("../xml_source_transcriptions/tsa-small-text-test.xml")
tokens2 = convert_xml_file_into_tokens("../xml_source_transcriptions/tsb-small-text-test.xml")

print(tokens1)
print(tokens2)

# align sequences of tokens. Results in segments.
aligner = EditGraphAligner()
alignment = aligner.align(tokens1, tokens2)
segments = aligner.segments

print_segments(segments)

# convert segments in dom tree
root = convert_segments_into_result_dom(segments)

print(root.toprettyxml())

