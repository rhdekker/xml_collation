# This module is intended for demonstration purposes
# use ipython notebook to display images
#
# @author: Ronald Haentjens Dekker


from xml_collation.TextGraph import convert_superwitness_to_textgraph
from xml_collation.collate_xml_hierarchy import convert_xml_string_into_tokens, align_tokens_and_return_superwitness, \
    convert_xml_file_into_tokens
from xml_collation.text_graph_exporter import export_as_dot

# optionally load the IPython dependencies
try:
    from IPython.display import HTML
    from IPython.display import SVG
    from IPython.core.display import display
    # import graphviz python library
    from graphviz import Digraph, Source
except:
    pass


# for now only two XML strings input
# for now only SVG output
def collate_xml(witness_a, witness_b):
    tokens_a = convert_xml_string_into_tokens(witness_a)
    tokens_b = convert_xml_string_into_tokens(witness_b)
    superwitness = align_tokens_and_return_superwitness(tokens_a, tokens_b)
    textgraph = convert_superwitness_to_textgraph(superwitness)
    dot_export = export_as_dot(textgraph, annotations=True)
    dot = Source(dot_export, format="svg")
    svg = dot.render()
    return display(SVG(svg))


def collate_xml_example():
    # convert XML files into tokens
    tokens1 = convert_xml_file_into_tokens("../xml_source_transcriptions/ts-fol-test-small.xml")
    tokens2 = convert_xml_file_into_tokens("../xml_source_transcriptions/tsq-test-small.xml")
    # log
    print(tokens1)
    print(tokens2)
    # end
    superwitness = align_tokens_and_return_superwitness(tokens1, tokens2)
    # log
    print(superwitness)
    # end
    textgraph = convert_superwitness_to_textgraph(superwitness)
    dot_export = export_as_dot(textgraph, annotations=True)
    print(dot_export)


def collate_xml_svg(limit=1000):
    # convert XML files into tokens
    tokens1 = convert_xml_file_into_tokens("xml_source_transcriptions/ts-fol-test-small.xml")
    tokens2 = convert_xml_file_into_tokens("xml_source_transcriptions/tsq-test-small.xml")
    superwitness = align_tokens_and_return_superwitness(tokens1, tokens2)
    print(superwitness[0:20])
    textgraph = convert_superwitness_to_textgraph(superwitness)
    dot_export = export_as_dot(textgraph, annotations=True, limit=limit)
    # print(dot_export)
    # render dot_export as SVG
    dot = Source(dot_export, format="svg")
    svg = dot.render()
    return display(SVG(svg))


if __name__ == '__main__':
    collate_xml_example()


    # print_superwitness(superwitness)
