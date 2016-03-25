from collections import namedtuple, defaultdict
# defaultdict is a subclass of dict

from xml_collation.collate_xml_hierarchy import TextToken

Annotation = namedtuple('Annotation', ['tagname', 'witnesses', 'range_start', 'range_end', 'level'])


class Stack(list):
    def push(self, item):
        self.append(item)

    def peek(self):
        return self[-1]


class TextGraph(object):
    def __init__(self, text_tokens=list, annotations=list):
        self.text_tokens = text_tokens
        self.annotations = annotations

    @property
    def annotations_sorted(self):
        return sorted(self.annotations, key = lambda x: (x.range_start, -x.range_end, x.level))


def calculate_level(open_tags_per_witness, extended_token):
    # find all relevant stacks
    relevant_stacks = []
    for sigil in extended_token.witnesses:
        stack = open_tags_per_witness[sigil]
        relevant_stacks.append(stack)
    # get parent_levels of stacks (NB stacks can be empty)
    parent_levels = []
    for stack in relevant_stacks:
        if stack:
            administration = stack.peek()
            level = administration[3]
            parent_levels.append(level)
        else:
            # root element level is 0, parent_level non-existent and thus faked
            parent_levels.append(-1)
    # calculate highest level of stacks
    highest_parent_level = max(parent_levels)
    # calculate level of node in graph
    actual_level = highest_parent_level +1
    return actual_level


def convert_superwitness_to_textgraph(superwitness):
    text_tokens = [extended_token for extended_token in superwitness if isinstance(extended_token.token, TextToken)]

    annotations = []
    open_tags_per_witness = defaultdict(Stack)
    # key-value pairs are grouped in a dictionary of stacks
    text_token_counter = -1

    for extended_token in superwitness:
        token = extended_token.token
        if isinstance(token, TextToken):
            text_token_counter += 1
        else:
            if token.content.startswith("/"):
                # end tag
                # print("closing: "+token.content)
                if extended_token.aligned:
                    administration_a = open_tags_per_witness["A"].pop()
                    administration_b = open_tags_per_witness["B"].pop()
                    if administration_a == administration_b:
                        # print("1")
                        # combine in 1 annotation
                        # annotation is the same element and on the same position in both witnesses
                        # stacks not necessarily same height
                        tagname = administration_a[0]
                        witnesses = administration_a[1]
                        range_start = administration_a[2]
                        range_end = text_token_counter
                        level = administration_a[3]
                        create_new_annotation_and_add_to_annotations(annotations, tagname, witnesses, range_start,
                                                                     range_end, level)
                        # print(annotations[-1])
                    else:
                        # print("2")
                        # create two separate annotations
                        # annotation could be the same tag but not the same element
                        # add the item to the annotations list given the coordinates of the range
                        create_new_annotation_and_add_to_annotations(annotations, administration_a[0], ["A"],
                                                                     administration_a[2], text_token_counter,
                                                                     administration_a[3])
                        # print(annotations[-1])
                        create_new_annotation_and_add_to_annotations(annotations, administration_b[0], ["B"],
                                                                     administration_b[2], text_token_counter,
                                                                     administration_b[3])
                        # print(annotations[-1])
                else:
                    # print("3")
                    # annotations are not aligned:
                    # --> one of the two witnesses is not a closing tag
                    # witnesses is list: aligned, addition, omission (A(+B), A, B)
                    administration = open_tags_per_witness[extended_token.witnesses[0]].pop()
                    create_new_annotation_and_add_to_annotations(annotations, administration[0],
                                                                 extended_token.witnesses, administration[2],
                                                                 text_token_counter, administration[3])
                    # print(annotations[-1])
            else:
                level = calculate_level(open_tags_per_witness, extended_token)
                administration = (token.content, extended_token.witnesses, text_token_counter+1, level)
                # open tag... push tag to one or both stacks
                for sigil in extended_token.witnesses:
                    open_tags_per_witness[sigil].push(administration)
                # log
                # print("opening "+str(administration))
                # print("top of stack witness A: "+str(open_tags_per_witness["A"].peek()))
                # print("top of stack witness B: "+str(open_tags_per_witness["B"].peek()))

    textgraph = TextGraph(text_tokens, annotations)
    return textgraph


def create_new_annotation_and_add_to_annotations(annotations, tagname, witnesses, range_start, range_end, level):
    # check whether there are text nodes in between the range
    if range_end < range_start:
        return

    annotations.append(Annotation(tagname, witnesses, range_start, range_end, level))
