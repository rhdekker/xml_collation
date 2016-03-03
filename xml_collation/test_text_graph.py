import unittest

from xml_collation.TextGraph import convert_superwitness_to_textgraph, Annotation
from xml_collation.collate_xml_hierarchy import convert_xml_string_into_tokens, align_tokens_and_return_superwitness


class TestTextGraph(unittest.TestCase):

    def test_tokenization(self):
        witness_a = "<tei><s>x y z</s></tei>"
        witness_b = "<tei><s>x</s>y<s>z</s></tei>"
        tokens_a = convert_xml_string_into_tokens(witness_a)
        self.assertEqual("[tei, s, x, y, z, /s, /tei]", str(tokens_a))
        tokens_b = convert_xml_string_into_tokens(witness_b)
        self.assertEqual("[tei, s, x, /s, y, s, z, /s, /tei]", str(tokens_b))

    def test_superwitness(self):
        witness_a = "<tei><s>x y z</s></tei>"
        witness_b = "<tei><s>x</s>y<s>z</s></tei>"
        tokens_a = convert_xml_string_into_tokens(witness_a)
        tokens_b = convert_xml_string_into_tokens(witness_b)
        superwitness = align_tokens_and_return_superwitness(tokens_a, tokens_b)
        self.assertEquals("[tei, s, x, +/s, y, +s, z, /s, /tei]", str(superwitness))

    def test_extended_tokens_witnesses(self):
        witness_a = "<tei><s>x y z</s></tei>"
        witness_b = "<tei><s>x</s>y<s>z</s></tei>"
        tokens_a = convert_xml_string_into_tokens(witness_a)
        tokens_b = convert_xml_string_into_tokens(witness_b)
        superwitness = align_tokens_and_return_superwitness(tokens_a, tokens_b)
        # self.assertEquals("[tei, s, x, +/s, y, +s, z, /s, /tei]", str(superwitness))
        self.assertEquals(["A", "B"], superwitness[0].witnesses)
        self.assertEquals(["B"], superwitness[3].witnesses)

    def test_textgraph_text(self):
        witness_a = "<tei><s>x y z</s></tei>"
        witness_b = "<tei><s>x</s>y<s>z</s></tei>"
        tokens_a = convert_xml_string_into_tokens(witness_a)
        tokens_b = convert_xml_string_into_tokens(witness_b)
        superwitness = align_tokens_and_return_superwitness(tokens_a, tokens_b)
        textgraph = convert_superwitness_to_textgraph(superwitness)
        text_tokens = textgraph.text_tokens
        self.assertEquals("[x, y, z]", str(text_tokens))

    def test_textgraph_annotations(self):
        witness_a = "<tei><s>x y z</s></tei>"
        witness_b = "<tei><s>x</s>y<s>z</s></tei>"
        tokens_a = convert_xml_string_into_tokens(witness_a)
        tokens_b = convert_xml_string_into_tokens(witness_b)
        superwitness = align_tokens_and_return_superwitness(tokens_a, tokens_b)
        textgraph = convert_superwitness_to_textgraph(superwitness)
        annotations = textgraph.annotations
        self.assertIn(Annotation("s", ["B"], 0, 0), annotations)
        self.assertIn(Annotation("s", ["A"], 0, 2), annotations)
        self.assertIn(Annotation("s", ["B"], 2, 2), annotations)
        self.assertIn(Annotation("tei", ["A", "B"], 0, 2), annotations)
        self.assertEqual(4, len(annotations))



