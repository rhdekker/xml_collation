import unittest
from collections import deque
from xml.dom import getDOMImplementation

from xml_collation.TextGraph import convert_superwitness_to_textgraph
from xml_collation.collate_xml_hierarchy import convert_xml_string_into_tokens, align_tokens_and_return_superwitness


def convert_textgraph_to_xml(textgraph):
    impl = getDOMImplementation()
    newdoc = impl.createDocument(None, "root", None)
    root = newdoc.documentElement
    latest = root
    annotations_to_add = deque(textgraph.annotations_sorted)
    for counter, text_token in enumerate(textgraph.text_tokens):
        print(counter, text_token)
        if annotations_to_add[0].range_start == counter:
            print(annotations_to_add.popleft())
    return newdoc
    pass


class EED(unittest.TestCase):
    @unittest.skip("showing class skipping")
    def test_dot1_textnodes_only(self):
        witness_a = "<tei><s>x y z</s></tei>"
        witness_b = "<tei><s>x</s>y<s>z</s></tei>"
        tokens_a = convert_xml_string_into_tokens(witness_a)
        tokens_b = convert_xml_string_into_tokens(witness_b)
        superwitness = align_tokens_and_return_superwitness(tokens_a, tokens_b)
        textgraph = convert_superwitness_to_textgraph(superwitness)
        xml = convert_textgraph_to_xml(textgraph)
        expected = '''<xml><tei><s cx:witness="a"><s cx:witness="b">x</s>y<s cx:witness="b">z</s></s></tei>
        '''
        self.assertEqual(expected, xml)