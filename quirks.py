class Quirk(object):
    def __init__(self, name, desc, args=0):
        self.name = name
        self.desc = desc
        self.args = args

QUIRKS = [
    Quirk('alternatingCaps', 'AlTeRnAtInG CaPs'),
    Quirk('depunct', 'No punctuation'),
    Quirk('hornedEmoticons', 'Horned Emoticons }:)'),
    Quirk('inverseCaps', 'iNVERTED cAPS'),
    Quirk('l33t', 'L33TSP34K'),
    Quirk('lower', 'All lowercase'),
    Quirk('prefix', 'Prefix with',args=1),
    Quirk('titleCase', 'Title Case'),
    Quirk('upper', 'All uppercase')
]

