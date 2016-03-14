from unittest import TestCase

from xml_collation.TextGraph import convert_superwitness_to_textgraph
from xml_collation.collate_xml_hierarchy import convert_xml_string_into_tokens, align_tokens_and_return_superwitness


def export_as_dot(textgraph):
    # opener
    output = "digraph TextGraph {\n"

    # we go over the text nodes
    text_token_counter = 0
    for text_token in textgraph.text_tokens:
        text_token_counter += 1
        output += '    '+str(text_token_counter)+' label="'+text_token.token.content+'"\n'

    # closer
    output += "}"
    return output
    pass


class DotTest(TestCase):

    def test_dot1_textnodes_only(self):
        witness_a = "<tei><s>x y z</s></tei>"
        witness_b = "<tei><s>x</s>y<s>z</s></tei>"
        tokens_a = convert_xml_string_into_tokens(witness_a)
        tokens_b = convert_xml_string_into_tokens(witness_b)
        superwitness = align_tokens_and_return_superwitness(tokens_a, tokens_b)
        textgraph = convert_superwitness_to_textgraph(superwitness)
        dot_export = export_as_dot(textgraph)
        expected_out = """digraph TextGraph {
    1 label="x"
    2 label="y"
    3 label="z"
}"""
        self.assertEqual(expected_out, dot_export)

    # 1 -> 2
    # 2 -> 3
