import unittest

from pytest import fail

from xml_collation.collate_xml_hierarchy import convert_xml_string_into_tokens, align_tokens_and_return_superwitness
from xml_collation.core_classes import Witness
from xml_collation.tokenindex import TokenIndex


class Beckett_examples(unittest.TestCase):
    def test_example1(self):
        # we first convert it into a or statement
        # witness_a = '<wit n="1"><subst><del>In</del><add>At</add></subst> the <subst><del>beginning</del><add>outset</add></subst>, finding the <subst><del>correct</del><add>right</add></subst> word.</wit>'
        # witness_b = '<wit n="2">In <subst><del>the</del><add>this</add></subst> very beginning, finding the right word.</wit>'

        witness_a = "<WITNESS><OR><C>In</C><C>At</C></OR> the <OR><C>beginning</C><C>outset</C></OR>, finding the <OR><C>correct</C><C>right</C></OR>word.</WITNESS>"
        witness_b = "<WITNESS>In<OR><C>the</C><C>this</C></OR>very beginning, finding the right word.</WITNESS>"

        # tokenize the two witnesses
        tokens_a = convert_xml_string_into_tokens(witness_a)
        tokens_b = convert_xml_string_into_tokens(witness_b)

        print(tokens_a)
        print(tokens_b)

        # connecting the stuff is not that easy, since the classes are slightly different
        # the witness class is not yet used in xml_collation, so that is going to throw an error
        witnesses = [Witness({"id":1, "tokens":tokens_a}), Witness({"id":2, "tokens":tokens_b})]
        tokenindex = TokenIndex(witnesses)
        tokenindex.prepare()

        intervals = tokenindex.split_lcp_array_into_intervals()
        for interval in intervals:
            print(str(interval))

        fail()





