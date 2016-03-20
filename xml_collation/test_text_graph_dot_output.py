from unittest import TestCase

from xml_collation.TextGraph import convert_superwitness_to_textgraph
from xml_collation.collate_xml_hierarchy import convert_xml_string_into_tokens, align_tokens_and_return_superwitness
from xml_collation.text_graph_exporter import export_as_dot


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
    1 [label="x"]
    2 [label="y"]
    3 [label="z"]
    1 -> 2
    2 -> 3
{ rank=same; 1; 2; 3 }
}"""
        self.assertEqual(expected_out, dot_export)


# for the next test there are again two things...
# vertices for the markup
# how do we make sure that we influence the previous test too much
# note that annotation vertices
# need to have unique id (in comparison to the text vertices)

# we need to add the edges here to the expectations

    def test_dot_markup_only(self):
        witness_a = "<tei><s1>x y z</s1></tei>"
        witness_b = "<tei><s2>x</s2>y<s3>z</s3></tei>"
        tokens_a = convert_xml_string_into_tokens(witness_a)
        tokens_b = convert_xml_string_into_tokens(witness_b)
        superwitness = align_tokens_and_return_superwitness(tokens_a, tokens_b)
        textgraph = convert_superwitness_to_textgraph(superwitness)
        dot_export = export_as_dot(textgraph, annotations=True)
        expected_out = """digraph TextGraph {
    1 [label="x"]
    2 [label="y"]
    3 [label="z"]
    1 -> 2
    2 -> 3
{ rank=same; 1; 2; 3 }
    a1 [label="tei"]
    a2 [label="s1"]
    a3 [label="s2"]
    a4 [label="s3"]
    a2 -> a1
    a3 -> a1
    1 -> a2
    1 -> a3
    a2 -> a1
    2 -> a2
    a2 -> a1
    a4 -> a1
    3 -> a2
    3 -> a4
}"""
        # TODO: There are some duplication annotation edges here that should be removed! (a1 - a2)
        # vertices only for the moment
        self.assertEqual(expected_out, dot_export)

