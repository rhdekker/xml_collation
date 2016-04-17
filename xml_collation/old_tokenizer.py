# Python module to tokenize XML strings and files into tokens
import re
from xml.dom.pulldom import CHARACTERS, START_ELEMENT, parse, END_ELEMENT, parseString


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


def convert_xml_file_into_tokens(xml_filename):
    doc = parse(xml_filename)
    return convert_xml_doc_into_tokens(doc)


def convert_xml_string_into_tokens(xml_string):
    doc = parseString(xml_string)
    return convert_xml_doc_into_tokens(doc)


def convert_xml_doc_into_tokens(xml_doc):
    # init output
    # NOTE: tokens objects are made so to make them unique (localName can be repeated)
    # NOTE: we might want to make the tokens more complex to store the original location in xpath form
    tokens = []
    for event, node in xml_doc:
        # debug
        # print(event, node)
        if event == CHARACTERS:
            tokens.extend(tokenize_text(node.data))

        elif event == START_ELEMENT:
            tokens.append(ElementToken(node.localName))

        elif event == END_ELEMENT:
            tokens.append(ElementToken("/" + node.localName))
    return tokens
