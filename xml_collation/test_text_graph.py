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
        self.assertIn(Annotation("s", ["B"], 0, 0, 1), annotations)
        self.assertIn(Annotation("s", ["A"], 0, 2, 1), annotations)
        self.assertIn(Annotation("s", ["B"], 2, 2, 1), annotations)
        self.assertIn(Annotation("tei", ["A", "B"], 0, 2, 0), annotations)
        self.assertEqual(4, len(annotations))

    def test_2_superwitness(self):
        witness_a = "<tei><p><s>a b<s>c</s>d</s></p></tei>"
        witness_b = "<tei><p><s>a b d</s></p></tei>"
        tokens_a = convert_xml_string_into_tokens(witness_a)
        tokens_b = convert_xml_string_into_tokens(witness_b)
        superwitness = align_tokens_and_return_superwitness(tokens_a, tokens_b)
        self.assertEquals("[tei, p, s, a, b, -s, -c, -/s, d, /s, /p, /tei]", str(superwitness))

    def test_2_textgraph_text(self):
        witness_a = "<tei><p><s>a b<s>c</s>d</s></p></tei>"
        witness_b = "<tei><p><s>a b d</s></p></tei>"
        tokens_a = convert_xml_string_into_tokens(witness_a)
        tokens_b = convert_xml_string_into_tokens(witness_b)
        superwitness = align_tokens_and_return_superwitness(tokens_a, tokens_b)
        textgraph = convert_superwitness_to_textgraph(superwitness)
        text_tokens = textgraph.text_tokens
        self.assertEquals("[a, b, -c, d]", str(text_tokens))

    def test_2_textgraph_annotations(self):
        witness_a = "<tei><p><s>a b<s>c</s>d</s></p></tei>"
        witness_b = "<tei><p><s>a b d</s></p></tei>"
        tokens_a = convert_xml_string_into_tokens(witness_a)
        tokens_b = convert_xml_string_into_tokens(witness_b)
        superwitness = align_tokens_and_return_superwitness(tokens_a, tokens_b)
        textgraph = convert_superwitness_to_textgraph(superwitness)
        annotations = textgraph.annotations
        self.assertIn(Annotation("s", ["A"], 2, 2, 3), annotations)
        self.assertIn(Annotation("s", ["A", "B"], 0, 3, 2), annotations)
        self.assertIn(Annotation("p", ["A", "B"], 0, 3, 1), annotations)
        self.assertIn(Annotation("tei", ["A", "B"], 0, 3, 0), annotations)
        self.assertEqual(4, len(annotations))

    def test_3_superwitness(self):
        witness_a = "<tei><p><s>a b<s>c</s>d</s></p></tei>"
        witness_b = "<tei><div><p><s>a b d</s></p></div></tei>"
        tokens_a = convert_xml_string_into_tokens(witness_a)
        tokens_b = convert_xml_string_into_tokens(witness_b)
        superwitness = align_tokens_and_return_superwitness(tokens_a, tokens_b)
        self.assertEquals("[tei, +div, p, s, a, b, -s, -c, -/s, d, /s, /p, +/div, /tei]", str(superwitness))

    def test_3_textgraph_text(self):
        witness_a = "<tei><p><s>a b<s>c</s>d</s></p></tei>"
        witness_b = "<tei><div><p><s>a b d</s></p></div></tei>"
        tokens_a = convert_xml_string_into_tokens(witness_a)
        tokens_b = convert_xml_string_into_tokens(witness_b)
        superwitness = align_tokens_and_return_superwitness(tokens_a, tokens_b)
        textgraph = convert_superwitness_to_textgraph(superwitness)
        text_tokens = textgraph.text_tokens
        self.assertEquals("[a, b, -c, d]", str(text_tokens))

    def test_3_textgraph_annotations(self):
        witness_a = "<tei><p><s>a b<s>c</s>d</s></p></tei>"
        witness_b = "<tei><div><p><s>a b d</s></p></div></tei>"
        tokens_a = convert_xml_string_into_tokens(witness_a)
        tokens_b = convert_xml_string_into_tokens(witness_b)
        superwitness = align_tokens_and_return_superwitness(tokens_a, tokens_b)
        textgraph = convert_superwitness_to_textgraph(superwitness)
        annotations = textgraph.annotations
        self.assertIn(Annotation("s", ["A"], 2, 2, 4), annotations)
        self.assertIn(Annotation("s", ["A", "B"], 0, 3, 3), annotations)
        self.assertIn(Annotation("p", ["A", "B"], 0, 3, 2), annotations)
        self.assertIn(Annotation("div", ["B"], 0, 3, 1), annotations)
        self.assertIn(Annotation("tei", ["A", "B"], 0, 3, 0), annotations)
        self.assertEqual(5, len(annotations))

    def test_sort_annotations_based_on_positions_and_level(self):
        witness_a = "<tei><s>x y z</s></tei>"
        witness_b = "<tei><s>x</s>y<s>z</s></tei>"
        tokens_a = convert_xml_string_into_tokens(witness_a)
        tokens_b = convert_xml_string_into_tokens(witness_b)
        superwitness = align_tokens_and_return_superwitness(tokens_a, tokens_b)
        textgraph = convert_superwitness_to_textgraph(superwitness)
        # sort on range start, then on range end, then on level
        a1 = Annotation("tei", ["A", "B"], 0, 2, 0)
        a2 = Annotation("s", ["A"], 0, 2, 1)
        a3 = Annotation("s", ["B"], 0, 0, 1)
        a4 = Annotation("s", ["B"], 2, 2, 1)
        expected_annotations = [a1, a2, a3, a4]
        annotations = textgraph.annotations_sorted
        self.assertEqual(expected_annotations, annotations)

    # NOTE: Currently milestone elements are ignore as annotations (since there are no text nodes to hang them on)
    def test_textgraph_milestones_annotations(self):
        witness_a = "<tei><lb/></tei>"
        witness_b = "<tei><lb/></tei>"
        tokens_a = convert_xml_string_into_tokens(witness_a)
        tokens_b = convert_xml_string_into_tokens(witness_b)
        superwitness = align_tokens_and_return_superwitness(tokens_a, tokens_b)
        textgraph = convert_superwitness_to_textgraph(superwitness)
        annotations = textgraph.annotations
        self.assertEqual(0, len(annotations))



