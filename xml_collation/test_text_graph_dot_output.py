from itertools import tee
from unittest import TestCase

from xml_collation.TextGraph import convert_superwitness_to_textgraph
from xml_collation.collate_xml_hierarchy import convert_xml_string_into_tokens, align_tokens_and_return_superwitness


def export_as_dot(textgraph, annotations=False):
    # opener
    output = "digraph TextGraph {\n"

    # add nodes for text nodes
    # we go over the text nodes
    text_token_counter = 0
    for text_token in textgraph.text_tokens:
        text_token_counter += 1
        output += '    '+str(text_token_counter)+' label="'+text_token.token.content+'"\n'

    # We have to map text nodes to a number
    # TODO: some duplication with code above
    text_tokens_as_numbers = [ counter+1 for counter, text_token in enumerate(textgraph.text_tokens) ]

    # add edges for text nodes
    for v, w in pairwise(text_tokens_as_numbers):
        output += '    '+str(v)+' -> '+str(w)+'\n'

    if annotations:
        # I need to sort the annotations that are on the text graph
        annotation_counter = 0
        for annotation in textgraph.annotations_sorted:
            annotation_counter += 1
            output += '    a'+str(annotation_counter)+' label="'+annotation.tagname+'"\n'

    # closer
    output += "}"
    return output


def pairwise(iterable):
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


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
    1 -> 2
    2 -> 3
}"""
        self.assertEqual(expected_out, dot_export)


# for the next test there are again two things...
# vertices for the markup
# how do we make sure that we influence the previous test too much
# note that annotation vertices
# need to have unique id (in comparison to the text vertices)

    def test_dot_markup_only(self):
        witness_a = "<tei><s>x y z</s></tei>"
        witness_b = "<tei><s>x</s>y<s>z</s></tei>"
        tokens_a = convert_xml_string_into_tokens(witness_a)
        tokens_b = convert_xml_string_into_tokens(witness_b)
        superwitness = align_tokens_and_return_superwitness(tokens_a, tokens_b)
        textgraph = convert_superwitness_to_textgraph(superwitness)
        dot_export = export_as_dot(textgraph, annotations=True)
        expected_out = """digraph TextGraph {
    1 label="x"
    2 label="y"
    3 label="z"
    1 -> 2
    2 -> 3
    a1 label="tei"
    a2 label="s"
    a3 label="s"
    a4 label="s"
}"""
        # vertices only for the moment
        self.assertEqual(expected_out, dot_export)

