from _license import defaultdict
from collections import namedtuple

from xml_collation.collate_xml_hierarchy import TextToken

# TODO: add range start and range end back in
Annotation = namedtuple('Annotation', ['tagname', 'witnesses'])


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

    for extended_token in superwitness:
        token = extended_token.token
        if isinstance(token, TextToken):
            # TODO
            pass
        else:
            if token.content.startswith("/"):
                # end tag
                print("closing: "+token.content)
                if extended_token.aligned:
                    tuple1 = open_tags_per_witness["A"].pop()
                    tuple2 = open_tags_per_witness["B"].pop()
                    if tuple1 == tuple2:
                        print("1")
                        # combine in 1 annotation
                        annotations.append(Annotation(tuple1[0], tuple1[1]))
                    else:
                        print("2")
                        # create two separate annotations
                        annotations.append(Annotation(tuple1[0], ["A"]))
                        annotations.append(Annotation(tuple2[0], ["B"]))
                else:
                    print("3")
                    tuple = open_tags_per_witness[extended_token.witnesses[0]].pop()
                    annotations.append(Annotation(tuple[0], tuple[1]))
            else:
                # open tag... push tag to one or both stacks
                tag = (token.content, extended_token.witnesses)
                for sigil in extended_token.witnesses:
                    open_tags_per_witness[sigil].push(tag)
                # log
                print("opening "+str(tag))
                print("top of stack witness A: "+str(open_tags_per_witness["A"].peek()))
                print("top of stack witness B: "+str(open_tags_per_witness["B"].peek()))

    textgraph = TextGraph(text_tokens, annotations)
    return textgraph
