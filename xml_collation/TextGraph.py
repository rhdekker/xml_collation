from _license import defaultdict
from collections import namedtuple

from xml_collation.collate_xml_hierarchy import TextToken

Annotation = namedtuple('Annotation', ['tagname', 'range_start', 'range_end'])

class TextGraph(object):
    def __init__(self, text_tokens=[], annotations=[]):
        self.text_tokens = text_tokens
        self.annotations = annotations


def convert_superwitness_to_textgraph(superwitness):
    text_tokens = [extended_token for extended_token in superwitness if isinstance(extended_token.token, TextToken)]
    textgraph = TextGraph(text_tokens)
    return textgraph
