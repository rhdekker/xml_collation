import unittest

from xml_collation.EditGraphAligner import EditGraphAligner
from xml_collation.tokenizer import OrAwareTokenizer, TextToken
from prettytable import PrettyTable




class EditGraphAlignerTest(unittest.TestCase):
    # global score
    def assertRow(self, expected, cell_data):
        actual = []
        for cell in cell_data:
            actual.append(cell.g)
        self.assertEqual(expected, actual)

    def _debug_edit_graph_table(self, table):
        # print the table horizontal
        x = PrettyTable()
        x.header=False
        for y in range(0, len(table)):
            cells = table[y]
            x.add_row(cells)
        # alignment can only be set after the field names are known.
        # since add_row sets the field names, it has to be set after x.add_row(cells)
        x.align="l"
        print(x)
        return x

    def test_tokenizer_with_or_operator(self):
        wit_a = '<witness n="1">a</witness>'
        wit_b = '<witness n="2"><or><option>a</option><option>b</option><option>c</option></or></witness>'
        tokenizer = OrAwareTokenizer()
        tokens_a = tokenizer.convert_xml_string_into_tokens(wit_a)
        self.assertEquals(TextToken("a", 0), tokens_a[0])
        self.assertEquals(1, len(tokens_a))

        tokens_b = tokenizer.convert_xml_string_into_tokens(wit_b)
        self.assertEquals(TextToken("a", 0), tokens_b[0])
        self.assertEquals(TextToken("b", 0), tokens_b[1])
        self.assertEquals(TextToken("c", 0, [1, 2, 3]), tokens_b[2])
        self.assertEquals(3, len(tokens_b))



    # def test_or_operator(self):
    #     wit_a = '<witness n="1">a</witness>'
    #     wit_b = '<witness n="2"><or><option>a</option><option>b</option><option>c</option></or></witness>'
    #     # TODO: make tokenizer a separate class
    #     tokens_a = convert_xml_string_into_tokens(wit_a)
    #     tokens_b = convert_xml_string_into_tokens(wit_b)
    #     aligner = EditGraphAligner()
    #     aligner.align(tokens_a, tokens_b)
    #     aligner._debug_edit_graph_table(aligner.table)
    #     table = aligner.table
    #     # what do I want? Well XML elements should not alter the score in anyway, just take the lowest neighbor score
    #     self.assertRow([0, 0, -1, -1], table[0])
    #     self.fail()