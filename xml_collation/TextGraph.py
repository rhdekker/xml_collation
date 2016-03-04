from collections import namedtuple, defaultdict

from xml_collation.collate_xml_hierarchy import TextToken

Annotation = namedtuple('Annotation', ['tagname', 'witnesses', 'range_start', 'range_end'])


class Stack(list):
    def push(self, item):
        self.append(item)

    def peek(self):
        return self[-1]


class TextGraph(object):
    def __init__(self, text_tokens=list, annotations=list):
        self.text_tokens = text_tokens
        self.annotations = annotations


def convert_superwitness_to_textgraph(superwitness):
    text_tokens = [extended_token for extended_token in superwitness if isinstance(extended_token.token, TextToken)]

    annotations = []
    open_tags_per_witness = defaultdict(Stack)
    text_token_counter = -1

    for extended_token in superwitness:
        token = extended_token.token
        if isinstance(token, TextToken):
            text_token_counter += 1
        else:
            if token.content.startswith("/"):
                # end tag
                print("closing: "+token.content)
                if extended_token.aligned:
                    administration_a = open_tags_per_witness["A"].pop()
                    administration_b = open_tags_per_witness["B"].pop()
                    if administration_a == administration_b:
                        print("1")
                        # combine in 1 annotation
                        # annotation is the same element and on the same position in both witnesses
                        # stacks not necessarily same height
                        annotations.append(Annotation(administration_a[0], administration_a[1], administration_a[2], text_token_counter))
                        # print(annotations[-1])
                    else:
                        print("2")
                        # create two separate annotations
                        # annotation could be the same tag but not the same element
                        # add the item to the annotations list given the coordinates of the range
                        annotations.append(Annotation(administration_a[0], ["A"], administration_a[2], text_token_counter))
                        # print(annotations[-1])
                        annotations.append(Annotation(administration_b[0], ["B"], administration_b[2], text_token_counter))
                        # print(annotations[-1])
                else:
                    print("3")
                    # annotations are not aligned:
                    # --> one of the two witnesses is a closing tag
                    # witnesses is list: aligned, addition, omission (A, A, B)
                    administration = open_tags_per_witness[extended_token.witnesses[0]].pop()
                    annotations.append(Annotation(administration[0], extended_token.witnesses, administration[2], text_token_counter))
                    # print(annotations[-1])
            else:
                # open tag... push tag to one or both stacks
                administration = (token.content, extended_token.witnesses, text_token_counter+1)
                for sigil in extended_token.witnesses:
                    open_tags_per_witness[sigil].push(administration)
                # log
                print("opening "+str(administration))
                print("top of stack witness A: "+str(open_tags_per_witness["A"].peek()))
                print("top of stack witness B: "+str(open_tags_per_witness["B"].peek()))

    textgraph = TextGraph(text_tokens, annotations)
    return textgraph
