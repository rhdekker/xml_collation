"""
    EditGraphAligner
    @author: Ronald Haentjens Dekker
    This class uses dynamic programming to find the optimal alignment between
    two lists of strings/tokens given a certain scoring function.
"""
from xml_collation.exact_match_scorer import Scorer


class EditGraphNode(object):
    def __init__(self):
        self.g = 0 # global score
        self.segments = 0 # number of segments
        self.match = False # this node represents a match or not

    def __repr__(self):
        return repr(self.g)


class Segment(object):
    def __init__(self, tokens, aligned, addition):
        self.tokens = tokens
        self.aligned = aligned
        self.addition = addition

    def __str__(self):
        return " ".join(self.tokens)

    def __repr__(self):
        return " ".join(self.tokens)


class EditGraphAligner(object):
    def __init__(self):
        self.scorer = Scorer()

    def align_table(self, tokens_witness_a, tokens_witness_b):
        self.tokens_witness_a = tokens_witness_a
        self.tokens_witness_b = tokens_witness_b
        self.length_witness_a = len(self.tokens_witness_a)
        self.length_witness_b = len(self.tokens_witness_b)

        # clear table: fill table with empty nodes
        # Note: in a large table this init takes a lot of time
        self.table = [[EditGraphNode() for _ in range(self.length_witness_a+1)] for _ in range(self.length_witness_b+1)]

        # per diagonal calculate the score (taking into account the three surrounding nodes)
        self.traverse_table_diagonally_and_score_cells()

        alignment = self.calculate_alignment_and_superwitness()
        return alignment

    def calculate_alignment_and_superwitness(self):
        alignment = {}
        # note we traverse from right to left!
        self.last_x = self.length_witness_a
        self.last_y = self.length_witness_b
        self.segments = []
        # start lower right cell
        x = self.length_witness_a
        y = self.length_witness_b
        # work our way to the upper left
        while x > 0 and y > 0:
            self._process_cell(self.tokens_witness_a, self.tokens_witness_b, alignment, x, y)
            # examine neighbor nodes
            nodes_to_examine = set()
            nodes_to_examine.add(self.table[y][x - 1])
            nodes_to_examine.add(self.table[y - 1][x])
            nodes_to_examine.add(self.table[y - 1][x - 1])
            # calculate the maximum scoring parent node
            parent_node = max(nodes_to_examine, key=lambda x: x.g)
            # move position
            if self.table[y - 1][x - 1] == parent_node:
                # another match or replacement
                y -= 1
                x -= 1
            else:
                if self.table[y - 1][x] == parent_node:
                    # omission?
                    y -= 1
                else:
                    if self.table[y][x - 1] == parent_node:
                        # addition?
                        x -= 1
        # process additions/omissions in the beginning of the witnesses
        self.add_to_segments(self.tokens_witness_a, self.tokens_witness_b, 0, 0)
        return alignment

    def add_to_segments(self, witness_a, witness_b, x, y):
        # detect additions/omissions compared to the first witness
        # print self.last_x - x - 1, self.last_y - y - 1
        if self.last_y - y - 1 > 0:
            added_witness = Segment(witness_b[y:self.last_y - 1], False, True)
            # update segments with additions, omissions
            self.segments.insert(0, added_witness)
        if self.last_x - x - 1 > 0:
            # print x, self.last_x, y, self.last_y
            # create new segment
            omitted_base = Segment(witness_a[x:self.last_x - 1], False, False)
            # print omitted_base
            self.segments.insert(0, omitted_base)

    def _process_cell(self, witness_a, witness_b, alignment, x, y):
        cell = self.table[y][x]
        # process segments
        if cell.match:
            self.add_to_segments(witness_a, witness_b, x, y)
            self.last_x = x
            self.last_y = y
        # process alignment
        if cell.match:
            token = witness_a[x-1]
            token2 = witness_b[y-1]
            alignment[token2] = token
#             print("match")
#             print(token2)
            # TODO: it is not so nice that every aligned token is it's own segment.
            self.segments.insert(0, Segment([token2], True, False))
        return cell

    # This function traverses the table diagonally and scores each cell.
    # Original function from Mark Byers; translated from C into Python.
    def traverse_table_diagonally_and_score_cells(self):
        m = self.length_witness_b+1
        n = self.length_witness_a+1
        for _slice in range(0, m + n - 1, 1):
            z1 = 0 if _slice < n else _slice - n + 1;
            z2 = 0 if _slice < m else _slice - m + 1;
            j = _slice - z2
            while j >= z1:
                x = _slice - j
                y = j
                self.score_cell(y, x)
                j -= 1

    def score_cell(self, y, x):
        # initialize root node score to zero (no edit operations have
        # been performed)
        if y == 0 and x == 0:
            self.table[y][x].g = 0
            return
        # examine neighbor nodes
        nodes_to_examine = set()
        # fetch existing score from the left node if possible
        if x > 0:
            nodes_to_examine.add(self.table[y][x-1])
        if y > 0:
            nodes_to_examine.add(self.table[y-1][x])
        if x > 0 and y > 0:
            nodes_to_examine.add(self.table[y-1][x-1])
        # calculate the maximum scoring parent node
        parent_node = max(nodes_to_examine, key=lambda x: x.g)
        if parent_node == self.table[y-1][x-1]:
            edit_operation = 0
        else:
            edit_operation = 1
        token_a = self.tokens_witness_a[x-1]
        token_b = self.tokens_witness_b[y-1]
        self.scorer.score_cell(self.table[y][x], parent_node, token_a, token_b, y, x, edit_operation)

    # def _debug_edit_graph_table(self, table):
    #     # print the table horizontal
    #     x = PrettyTable()
    #     x.header=False
    #     for y in range(0, len(table)):
    #         cells = table[y]
    #         x.add_row(cells)
    #     # alignment can only be set after the field names are known.
    #     # since add_row sets the field names, it has to be set after x.add_row(cells)
    #     x.align="l"
    #     print(x)
    #     return x
