# Python module to tokenize XML strings and files into tokens
import re
from xml.dom.pulldom import CHARACTERS, START_ELEMENT, parse, END_ELEMENT, parseString

from xml_collation.util import Stack


class Token(object):
    def __init__(self, content):
        self.content = content

    def __str__(self):
        return self.content

    def __repr__(self):
        return self.content


class TextToken(Token):
    def __init__(self, content, parents=None, after=[]):
        super(TextToken, self).__init__(content)
        # TODO: rename parents to parent
        self.parents = parents
        self.after = after

    def __hash__(self):
        return hash(self.content) + hash(self.parents) + hash(self.after)

    def __eq__(self, other):
        return self.content == other.content and self.parents == other.parents and self.after == other.after

    def __repr__(self):
        return str(self.content)+":"+str(self.parents)+":"+str(self.after)

    def __str__(self):
        return "!!"


class ElementToken(Token):
    pass


class OrAwareTokenizer(object):
    def __init__(self):
        # TODO: make last_text_token a local variable instead?
        self.last_text_token = 0

    def convert_xml_file_into_tokens(self, xml_filename):
        doc = parse(xml_filename)
        return self.convert_xml_doc_into_tokens(doc)

    def convert_xml_string_into_tokens(self, xml_string):
        doc = parseString(xml_string)
        return self.convert_xml_doc_into_tokens(doc)

    def convert_xml_doc_into_tokens(self, xml_doc):
        # init output
        # NOTE: tokens objects are made so to make them unique (localName can be repeated)
        # NOTE: we might want to make the tokens more complex to store the original location in xpath form
        tokens = []
        important_elements = Stack()
        for event, node in xml_doc:
            # debug
            # print(event, node)
            if event == CHARACTERS:
                # we work with a list here in stead of a generator because we have to do multiple things here
                # the previous position that we have to give here can get quite complex
                # it depends whether we are in an or and whether we are at the start of the option
                # at the start of the option we have to pass a different previous position than in the rest of the
                # text
                # last position = self.last_text_token + idx if idx > 0 or when NOT in a or
                # otherwise: last_position = last_or_open_stack
                last_or_open = [element[1] for element in important_elements if element[0]=="or_open"]
                text_tokens = [TextToken(content, self.last_text_token + idx if idx > 0 or not last_or_open else
                        last_or_open[-1]) for idx, content in enumerate(re.findall(r'\w+|[^\w\s]+', node.data))]
                self.last_text_token += len(text_tokens)
                tokens.extend(text_tokens)

            elif event == START_ELEMENT:
                # XML elements that represent system stuff like "witness" and "or" and "option" should not get their
                # own tokens
                # however we do store information on the stack
                if node.localName == "or":
                    important_elements.append(("or_open", self.last_text_token))
                # OLD behaviour
                # tokens.append(ElementToken(node.localName))
                pass

            elif event == END_ELEMENT:
                # In case of an end OR XML element
                # we have to fill the end of the last text token (although in the case of mixed content; the last token
                # doesn't have to be a text token; we focus on that later
                # fetch all the end options from the stack till the open OR is found
                if node.localName == "option":
                    important_elements.append(("option_close", self.last_text_token))
                elif node.localName == "or":
                    # gather all the last text tokens from all the options of this OR statement
                    closing_option_text_token_positions = []
                    while important_elements.peek()[0] != "or_open":
                        closing_option_text_token_positions.insert(0, important_elements.pop()[1])
                    print(closing_option_text_token_positions)
                    # place all the positions as the "after" property on the last token (for now only text tokens)
                    tokens[-1].after = closing_option_text_token_positions
                # OLD behaviour
                # tokens.append(ElementToken("/" + node.localName))
                pass

        # reset state; not so nice
        self.last_text_token = 0
        return tokens
