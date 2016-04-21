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

    def debug_edit_graph_table(self, table):
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

    # what do I want?
    # 1) The XML elements are not by itself visible in table,
    # 2) but do alter the score.
    # 3) Every option should reset the score at the begin of the option to the last score before the choice
    # 4) TODO: At the end the of the choice the best score at the end of each option has to chosen
    def test_or_operator(self):
        wit_a = '<witness n="1">a</witness>'
        wit_b = '<witness n="2"><or><option>a</option><option>b</option><option>c</option></or></witness>'
        tokenizer = OrAwareTokenizer()
        tokens_a = tokenizer.convert_xml_string_into_tokens(wit_a)
        tokens_b = tokenizer.convert_xml_string_into_tokens(wit_b)
        aligner = EditGraphAligner()
        aligner.align(tokens_a, tokens_b)
        self.debug_edit_graph_table(aligner.table)
        table = aligner.table
        self.assertRow([0, -1], table[0])
        self.assertRow([-1, 0], table[1])
        self.assertRow([-1, -2], table[2])
        self.assertRow([-1, -2], table[3]) #TODO: the second -2 should become a 0 after the OR operator is implemented
