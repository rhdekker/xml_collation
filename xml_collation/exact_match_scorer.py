"""
 This class scores cells in the edit graph table.
 @author: Ronald Haentjens Dekker
"""
#from Levenshtein._levenshtein import ratio


class Scorer(object):
    def __init__(self, near_match=False, properties_filter=None):
        self.blocks = []
        self.global_tokens_to_occurrences = {}
        self.properties_filter=properties_filter
        if near_match:
            self.match_function = self.near_match
        else:
            self.match_function = self.match

    # edit operation:
    #    0 == match/replacement
    #    1 == addition/omission
    def score_cell(self, table_node, parent_node, token_a, token_b, y, x, edit_operation):
        # no matching possible in this case (always treated as a gap)
        # it is either an add or a delete
        if x == 0 or y == 0:
            table_node.g = parent_node.g - 1
            return

        # we score differently depending on the type of edit operation
        # edit operation 0: it is either a match or a replacement (so an add and a delete)
        # edit operation 1: it is either an add/delete
        if edit_operation == 0:
            # it is a match or a replacement
            match = self.match_function(token_a, token_b)
            # print("testing "+token_a.token_string+" and "+token_b.token_string+" "+str(match))
            # match = token_a.token_string == token_b.token_string
            # based on match or not and parent_node calculate new score
            if match==0:
                # mark the fact that this node is match
                table_node.match = True
                # do not change score for now
                table_node.g = parent_node.g
                # count segments
                if not parent_node.match:
                    table_node.segments = parent_node.segments + 1
                return
            if match==1:
                table_node.g = parent_node.g - 0.5 #TODO: TEST TEST TEST
                pass
            else:
                table_node.g = parent_node.g - 2
                return
        else:
            # it is an add/delete
            table_node.g = parent_node.g - 1
            return

    # return values:
    # 0 = FULL_MATCH
    # -1 = NO MATCH
    # 1 = PARTIAL MATCH
    def match(self, token_a, token_b):
        match = token_a.content == token_b.content
        if match:
            # Check whether the user has supplied a properties filter
            if not self.properties_filter:
                return 0
            match = self.properties_filter(token_a.token_data, token_b.token_data)
            if match:
                return 0
            else:
                return -1
        else:
            return -1

    def near_match(self, token_a, token_b):
        result = self.match(token_a, token_b)
        if result==0:
            return 0
        r = ratio(token_a.token_string, token_b.token_string)
        print(str(token_a)+" "+str(token_b)+" "+str(r))
        if r > 0.6:
            return 1
        else:
            return -1
        pass