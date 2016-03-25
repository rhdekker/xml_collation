from collections import deque
from itertools import tee


def export_as_dot(textgraph, annotations=False, limit=1000):
    # opener
    output = "strict digraph TextGraph {\n"

    # add nodes for text nodes
    # we go over the text nodes
    text_token_counter = 0
    for text_token in textgraph.text_tokens[0:limit]:
        text_token_counter += 1
        output += '    '+str(text_token_counter)+' [label="'+text_token.token.content+'"]\n'

    # We have to map text nodes to a number
    # TODO: some duplication with code above
    # TODO: this could probably done simpler by setting up a range based on the length of the text tokens
    text_tokens_as_numbers = [ counter+1 for counter, text_token in enumerate(textgraph.text_tokens[0:limit]) ]

    # add edges for text nodes
    for v, w in pairwise(text_tokens_as_numbers):
        output += '    '+str(v)+' -> '+str(w)+'\n'

    # add rank directive
    # { rank=same, b, c, d }
    output += '{ rank=same; '
    output += "; ".join([str(number) for number in text_tokens_as_numbers])
    output += " }\n"

    if annotations:
        # I need to sort the annotations that are on the text graph
        annotation_counter = 0
        for annotation in textgraph.annotations_sorted:
            annotation_counter += 1
            output += '    a'+str(annotation_counter)+' [label="'+annotation.tagname+'"]\n'

        # add edges for annotation nodes
        # so we go over the text nodes from left to right
        # we also go over the stream of annotations
        annotations_to_process = deque(textgraph.annotations_sorted)
        open_annotations = []
        annotation_counter = 0
        for text_token_as_number in text_tokens_as_numbers:
            # print("current text token: "+str(text_token_as_number))

            # first handle the annotations that should be opened
            while annotations_to_process and annotations_to_process[0].range_start == text_token_as_number - 1:
                next_annotation = annotations_to_process.popleft()
                annotation_counter += 1
                open_annotations.append((next_annotation, annotation_counter))
                # print("current top level annotation: "+str(next_annotation))

            # draw edges
            open_annotation_counter = 0

            # detect the highest level present in the open annotations.
            # the highest level annotations need to be connect to text nodes.
            highest_level = open_annotations[-1][0].level if open_annotations else -1

            for open_annotation in open_annotations:
                open_annotation_counter += 1
                # check highest_level
                if open_annotation[0].level == highest_level:
                    output += "    "+str(text_token_as_number)+ " -> a"+str(open_annotation[1])+"\n"
                else:
                    for other_annotation in open_annotations[open_annotation_counter:]:
                        # print(open_annotation, other_annotation)
                        condition1 = other_annotation[0].level - open_annotation[0].level == 1
                        condition2 = (witness for witness in other_annotation[0].witnesses if witness in open_annotation[0].witnesses)
                        if condition1 and next(condition2, None):
                            output += "    a"+str(other_annotation[1]) + " -> a"+str(open_annotation[1])+"\n"

            # handle the annotations that should be closed
            while open_annotations and open_annotations[-1][0].range_end == text_token_as_number - 1:
                annotation_to_close = open_annotations.pop()
                # print("closing: "+str(annotation_to_close))

    # closer
    output += "}"
    return output


def pairwise(iterable):
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


