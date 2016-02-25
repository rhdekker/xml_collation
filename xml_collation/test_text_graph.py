import unittest

from pytest import fail

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