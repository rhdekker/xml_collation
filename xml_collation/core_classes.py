from xml_collation.collate_xml_hierarchy import convert_xml_string_into_tokens


class Witness(object):

    def __init__(self, witnessdata):
        self.sigil = witnessdata['id']
        self._tokens = []
        if 'content' in witnessdata:
            content = witnessdata['content']
            # NOTE: convert etc returns Token objects
            tokens_as_strings = convert_xml_string_into_tokens(content)
            for token_string in tokens_as_strings:
                self._tokens.append(token_string)
        elif 'tokens' in witnessdata:
            # NOTE: tokens are presumed here to be Token object rather than strings
            # NOTE: THat WILL NOT ALWAYS BE THE CASE!
            for tk in witnessdata['tokens']:
                self._tokens.append(tk)

    def tokens(self):
        return self._tokens