


from xml_collation import *

witness_a = "<tei><s>x y z</s></tei>"
witness_b = "<tei><s>x</s>y<s>z</s></tei>"
collate_xml(witness_a, witness_b)

# TODO: hmm the following example somehow crashes in the text graph
# collate_xml("<tei><a>f</a></tei>", "<tei><b>a</b></tei>")

