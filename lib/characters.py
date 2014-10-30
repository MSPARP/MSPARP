# -*- coding: utf-8 -*-

CHARACTER_GROUPS = [
    'Special/Other',
    'Humans',
    'Post-scratch Trolls',
    'Pre-scratch Trolls',
    'Guardians',
    'Sprites',
    'Ancestors',
    'Midnight Crew',
]

CHARACTERS = {
    'Special/Other': [
        'Anonymous/Other',
        'Original Character',
        'Trickster',
        'Doc Scratch',
        'AR/Hal',
        'Calliope',
        'Caliborn',
        'Lord English',
        'Other (canon)',
    ],
    'Humans': [
        'John',
        'Rose',
        'Dave',
        'Jade',
        'Jane',
        'Roxy',
        'Dirk',
        'Jake',
    ],
    'Post-scratch Trolls': [
        'Aradia (dead)',
        'Aradia',
        'Aradiabot',
        'Tavros',
        'Sollux',
        'Sollux (blind)',
        'Karkat',
        'Nepeta',
        'Kanaya',
        'Terezi',
        'Vriska',
        'Equius',
        'Gamzee',
        'Gamzee (sober)',
        'Eridan',
        'Feferi',
    ],
    'Pre-scratch Trolls': [
        'Damara',
        'Rufioh',
        'Mituna',
        'Kankri',
        'Meulin',
        'Porrim',
        'Latula',
        'Aranea',
        'Horuss',
        'Kurloz',
        'Cronus',
        'Meenah',
    ],
    'Guardians': [
        'Dad',
        'Nanna',
        'Mom',
        'Bro',
        'Grandpa',
        'Poppop',
        'Alpha Mom',
        'Alpha Bro',
        'Grandma',
    ],
    'Sprites': [
        'Nannasprite',
        'Jaspersprite',
        'Calsprite',
        'Davesprite',
        'Jadesprite',
        'Aradiasprite',
        'Tavrisprite',
        'Fefetasprite',
        'Erisolsprite',
        'ARquiusprite',
    ],
    'Ancestors': [
        'The Handmaid',
        'The Summoner',
        'The Psiioniic',
        'The Helmsman',
        'The Signless',
        'The Disciple',
        'The Dolorosa',
        'Redglare',
        'Mindfang',
        'Darkleer',
        'Grand Highblood',
        'Dualscar',
        'The Condesce',
    ],
    'Midnight Crew': [
        'Spades Slick',
        'Clubs Deuce',
        'Diamonds Droog',
        'Hearts Boxcars',
    ],
}

# XXX THIS IS JUST A DUPLICATE OF CHARACTERS.JS
# XXX also fix the goddamn indentation

CHARACTER_DETAILS = {
    'anonymous/other': {
        'acronym': '??',
        'name': 'anonymous',
        'color': '000000',
        'quirk_prefix': '',
        'case': 'normal',
        'replacements': '[]'
    },
    'original character': {
        'acronym': '**',
        'name': 'Original Character',
        'color': 'FF00FF',
        'quirk_prefix': '',
        'case': 'normal',
        'replacements': '[]'
    },
    # XXX GOTTA REMOVE THIS AT SOME POINT.
    # needs conversion though otherwise we're gonna get a raft of 500s
    'ancestor': {
        'acronym': '??',
        'name': 'Ancestor',
        'color': '000000',
        'quirk_prefix': '',
        'case': 'normal',
        'replacements': '[]'
    },
    'guardian': {
        'acronym': '??',
        'name': 'Guardian',
        'color': '000000',
        'quirk_prefix': '',
        'case': 'normal',
        'replacements': '[]'
    },
    'midnight crew': {
        'acronym': '??',
        'name': 'Guardian',
        'color': '000000',
        'quirk_prefix': '',
        'case': 'normal',
        'replacements': '[]'
    },
    # XXX END STUFF THAT NEEDS REMOVING
    'trickster': {
        'acronym': '??',
        'name': 'Trickster',
        'color': 'FFAC9F',
        'quirk_prefix': '',
        'case': 'normal',
        'replacements': '[]'
    },
    'doc scratch': {
        'acronym': '',
        'name': 'Doc Scratch',
        'color': 'FFFFFF',
        'quirk_prefix': '',
        'case': 'normal',
        'replacements': '[["/^(\w)/", "$U"], ["/[!|\?|\.](\s\w)/", "$U"], ["/[\s|^](i)[\'|\W|$]/", "$U"]]'
    },
    'ar/hal': {
        'acronym': 'TT',
        'name': 'Lil Hal',
        'color': 'E00707',
        'quirk_prefix': '',
        'case': 'normal',
        'replacements': '[["/^(\w)/", "$U"], ["/[!|\?|\.](\s\w)/", "$U"], ["/[\s|^](i)[\'|\W|$]/", "$U"]]'
	},
    'calliope': {
        'acronym': 'UU',
        'name': 'uranianUmbra',
        'color': '929292',
        'quirk_prefix': '',
        'case': 'lower',
        'replacements': '[["/u_(\S)/", "£_$1"], ["/(\S)_u/", "$1_£"], ["u", "U"], ["_£", "_u"], ["£_", "u_"]]'
	},
    'caliborn': {
        'acronym': 'uu',
        'name': 'undyingUmbrage',
        'color': '323232',
        'quirk_prefix': '',
        'case': 'upper',
        'replacements': '[["U", "u"]]'
    },
    'lord english': {
        'acronym': 'LE',
        'name': 'Lord English',
        'color': '2ED73A',
        'quirk_prefix': '',
        'case': 'upper',
        'replacements': '[]'
    },
    'other (canon)': {
        'acronym': '??',
        'name': 'Other (canon)',
        'color': 'ff83fb',
        'quirk_prefix': '',
        'case': 'normal',
        'replacements': '[]'
    },
    'john': {
        'acronym': 'EB',
        'name': 'ectoBiologist',
        'color': '0715CD',
        'quirk_prefix': '',
        'case': 'normal',
        'replacements': '[["/([A-Z][a-z]+\b)/", "$L"], ["/(\b)([A-Z][A-Z]+)(\b)/", "¥$2¥"], ["/(\b)([A-Z]\'[A-Z]+)(\b)/", "¥$2¥"], ["/.*/", "$L"], ["/¥([\w|\']+)¥/", "$U"], ["¥", " "], ["/([A-Z]\W[a-z]\W[A-Z])/", "$U"], ["/([A-Z]\'[a-z])/", "$U"], ["/[\s|^]([:;]d)/", "$U"], ["[\s|^](d[:;])", "$U"]]'
	},
    'rose': {
        'acronym': 'TT',
        'name': 'tentacleTherapist',
        'color': 'B536DA',
        'quirk_prefix': '',
        'case': 'normal',
        'replacements': '[["/^(\w)/", "$U"], ["/[!|\?|\.](\s\w)/", "$U"], ["/[\s|^](i)[\'|\W|$]/", "$U"]]'
	},
    'dave': {
        'acronym': 'TG',
        'name': 'turntechGodhead',
        'color': 'E00707',
        'quirk_prefix': '',
        'case': 'normal',
        'replacements': '[["/([A-Z][a-z]+\b)/", "$L"], ["/(\b)([A-Z][A-Z]+)(\b)/", "¥$2¥"], ["/(\b)([A-Z]\'[A-Z]+)(\b)/", "¥$2¥"], ["/.*/", "$L"], ["/¥([\w|\']+)¥/", "$U"], ["¥", " "], ["/([A-Z]\W[a-z]\W[A-Z])/", "$U"], ["/([A-Z]\'[a-z])/", "$U"], ["/(\w)\'(\w)/", "$1$2"], ["/(\w)\.$/", "$1"], ["/[\s|^]([:;]d)/", "$U"], ["/[\s|^](d[:;])/", "$U"]]'
	},
    'jade': {
        'acronym': 'GG',
        'name': 'gardenGnostic',
        'color': '4AC925',
        'quirk_prefix': '',
        'case': 'normal',
        'replacements': '[["/([A-Z][a-z]+\b)/", "$L"], ["/(\b)([A-Z][A-Z]+)(\b)/", "¥$2¥"], ["/(\b)([A-Z]\'[A-Z]+)(\b)/", "¥$2¥"], ["/.*/", "$L"], ["/¥([\w|\']+)¥/", "$U"], ["¥", " "], ["/([A-Z]\W[a-z]\W[A-Z])/", "$U"], ["/([A-Z]\'[a-z])/", "$U"], ["/(\w)\'(\w)/", "$1$2"], ["/(\w)\.$/", "$1"], ["/[\s|^]([:;]d)/", "$U"], ["/[\s|^](d[:;])/", "$U"], ["/[\s|^]([:;]b)/", "$U"]]'
	},
    'jane': {
        'acronym': 'GG',
        'name': 'gutsyGumshoe',
        'color': '00D5F2',
        'quirk_prefix': '',
        'case': 'normal',
        'replacements': '[["/^(\w)/", "$U"], ["/[!|\?|\.](\s\w)/", "$U"], ["/[\s|^](i)[\'|\W|$]/", "$U"]]'
	},
    'roxy': {
        'acronym': 'TG',
        'name': 'tipsyGnostalgic',
        'color': 'FF6FF2',
        'quirk_prefix': '',
        'case': 'normal',
        'replacements': '[["/([A-Z][a-z]+\b)/", "$L"], ["/(\b)([A-Z][A-Z]+)(\b)/", "¥$2¥"], ["/(\b)([A-Z]\'[A-Z]+)(\b)/", "¥$2¥"], ["/.*/", "$L"], ["/¥([\w|\']+)¥/", "$U"], ["¥", " "], ["/([A-Z]\W[a-z]\W[A-Z])/", "$U"], ["/([A-Z]\'[a-z])/", "$U"], ["/(\w)\'(\w)/", "$1$2"], ["/(\w)\.$/", "$1"], ["/[\s|^]([:;]d)/", "$U"], ["/[\s|^](d[:;])/", "$U"]]'
	},
    'dirk': {
        'acronym': 'TT',
        'name': 'timaeusTestified',
        'color': 'F2A400',
        'quirk_prefix': '',
        'case': 'normal',
        'replacements': '[["/^(\w)/", "$U"], ["/[!|\?|\.](\s\w)/", "$U"], ["/[\s|^](i)[\'|\W|$]/", "$U"]]'
	 },
    'jake': {
        'acronym': 'GT',
        'name': 'golgothasTerror',
        'color': '1F9400',
        'quirk_prefix': '',
        'case': 'normal',
       'replacements': '[["\'", " "], ["/.*/", "$L"], ["/^(\w)/", "$U"], ["/[!|\?|\.](\s\w)/", "$U"], ["/[\s|^]([:;]d)/", "$U"], ["/[\s|^]([:;]p)/", "$U"]]'
	},
    'aradia (dead)': {
        'acronym': 'AA',
        'name': 'apocalypseArisen',
        'color': 'A10000',
        'quirk_prefix': '',
        'case': 'lower',
        'replacements': '[["o", "0"], ["/(\w)\'(\w)/", "$1$2"], ["/(\w)\.$/", "$1"]]'
	},
    'aradia': {
        'acronym': 'AA',
        'name': 'apocalypseArisen',
        'color': 'A10000',
        'quirk_prefix': '',
        'case': 'lower',
        'replacements': '[["/(\w)\'(\w)/", "$1$2"], ["/(\w)\.$/", "$1"], ["/[\s|^]([:;][dop])/", "$U"], ["/[\s|^](d[:;])/", "$U"]]'
	},
    'aradiabot': {
        'acronym': 'AA',
        'name': 'apocalypseArisen',
        'color': '000056',
        'quirk_prefix': '',
        'case': 'lower',
        'replacements': '[["o", "0"], ["/(\w)\'(\w)/", "$1$2"], ["/(\w)\.$/", "$1"]]'
	},
    'tavros': {
        'acronym': 'AT',
        'name': 'adiosToreador',
        'color': 'A15000',
        'quirk_prefix': '',
        'case': 'normal',
        'replacements': '[["/(?:^|¦¤¤¦¦)(.*?)(?:$|¦¤¤¤¦)/", "$U"], ["/^(\w)/", "$L"], ["/([iI])\b/", "$L"], ["/[\.\?!]/", ","], ["/(,\s?\w)/", "$L"], ["/[\s|^|}](:O)/", "$L"], ["/[\s|^|}](:[dp])/", "$U"]]'
	},
    'sollux': {
        'acronym': 'TA',
        'name': 'twinArmageddons',
        'color': 'A1A100',
        'quirk_prefix': '',
        'case': 'normal',
        'replacements': '[["/([A-Z][a-z]+\b)/", "$L"], ["/(\b)([A-Z][A-Z]+)(\b)/", "¥$2¥"], ["/(\b)([A-Z]\'[A-Z]+)(\b)/", "¥$2¥"], ["/.*/", "$L"], ["/¥([\w|\']+)¥/", "$U"], ["¥", " "], ["/([A-Z]\W[a-z]\W[A-Z])/", "$U"], ["/([A-Z]\'[a-z])/", "$U"], ["/(^|\s)to(\W|$)/", "$1two$2"], ["/(^|\s)TO(\W|$)/", "$1TWO$2"], ["/(^|\s)too(\W|$)/", "$1two$2"], ["/(^|\s)TOO(\W|$)/", "$1TWO$2"], ["/(^|\s)together(\W|$)/", "$1twogether$2"], ["/(^|\s)TOGETHER(\W|$)/", "$1TWOGETHER$2"], ["/(^|\s)tonight(\W|$)/", "$1twonight$2"], ["/(^|\s)TONIGHT(\W|$)/", "$1TWONIGHT$2"], ["/(^|\s)today(\W|$)/", "$1twoday$2"], ["/(^|\s)TODAY(\W|$)/", "$1TWODAY$2"], ["/(^|\s)tomorrow(\W|$)/", "$1twomorrow$2"], ["/(^|\s)TOMORROW(\W|$)/", "$1TWOMORROW$2"], ["/([iI])/", "$1$1"], ["/([sS])/", "2"]]'
	},
    'sollux (blind)': {
        'acronym': 'TA',
        'name': 'twinArmageddons',
        'color': 'A1A100',
        'quirk_prefix': '',
        'case': 'normal',
        'replacements': '[["/([A-Z][a-z]+\b)/", "$L"], ["/(\b)([A-Z][A-Z]+)(\b)/", "¥$2¥"], ["/(\b)([A-Z]\'[A-Z]+)(\b)/", "¥$2¥"], ["/.*/", "$L"], ["/¥([\w|\']+)¥/", "$U"], ["¥", " "], ["/([A-Z]\W[a-z]\W[A-Z])/", "$U"], ["/([A-Z]\'[a-z])/", "$U"], ["/([oO])/", "0"]]'
	},
    'karkat': {
        'acronym': 'CG',
        'name': 'carcinoGeneticist',
        'color': '626262',
        'quirk_prefix': '',
        'case': 'upper',
        'replacements': '[["/¦¤¤¤¦(.*?)¦¤¤¦¦/", "$L"]]'
	},
    'nepeta': {
        'acronym': 'AC',
        'name': 'arsenicCatnip',
        'color': '416600',
        'quirk_prefix': ':33 <',
        'case': 'normal',
        'replacements': '[["/([A-Z][a-z]+\b)/", "$L"], ["/(\b)([A-Z][A-Z]+)(\b)/", "¥$2¥"], ["/(\b)([A-Z]\'[A-Z]+)(\b)/", "¥$2¥"], ["/.*/", "$L"], ["/¥([\w|\']+)¥/", "$U"], ["¥", " "], ["/([A-Z]\W[a-z]\W[A-Z])/", "$U"], ["/([A-Z]\'[a-z])/", "$U"], ["/(\w)\'(\w)/", "$1$2"], ["/(\w)\.$/", "$1"], ["/[eE][eE]/", "33"], ["/[\s|^]([:;][dp][dp])/", "$U"], ["/[\s|^](dd[:;])/", "$U"]]'
	},
    'kanaya': {
        'acronym': 'GA',
        'name': 'grimAuxiliatrix',
        'color': '008141',
        'quirk_prefix': '',
        'case': 'normal',
        'replacements': '[["\'", " "], ["/(^[a-z])/", "$U"], ["/(\s[a-z])/", "$U"], ["/(-[a-z])/", "$U"], ["/(\w)\.$/", "$1"], ["/(\w),(\s\w)/", "$1$2"]]'
	},
    'terezi': {
        'acronym': 'GC',
        'name': 'gallowsCalibrator',
        'color': '008282',
        'quirk_prefix': '',
        'case': 'upper',
        'replacements': '[["/[aA]/", "4"], ["/[iI]/", "1"], ["/[eE]/", "3"], ["/(\w)\'(\w)/", "$1$2"], ["/\w)\.$/", "$1"], ["/¦¤¤¤¦(.*?)¦¤¤¦¦/", "$L"]]'
	},
    'vriska': {
        'acronym': 'AG',
        'name': 'arachnidsGrip',
        'color': '005682',
        'quirk_prefix': '',
        'case': 'normal',
        'replacements': '[["/[bB]/", "8"], ["(m)", "♏"], ["/^(\w)/", "$U"], ["/[!|\?|\.](\s\w)/", "$U"], ["/[\s|^](i)[\'|\W|$]/", "$U"]]'
	},
    'equius': {
        'acronym': 'CT',
        'name': 'centaursTesticle',
        'color': '000056',
        'quirk_prefix': 'D -->',
        'case': 'normal',
        'replacements': '[["/[lL][oO][oO]/", "100"], ["/[xX]/", "%"], ["/(\b[sS][tT][rR][oO][nN][gG]\w*)/", "$U"], ["/[oO][oO][lL]/", "001"], ["/(\w)\.$/", "$1"], ["/^(\w)/", "$U"], ["/[!|\?|\.](\s\w)/", "$U"], ["/[\s|^](i)[\'|\W|$]/", "$U"]]'
	},
    'gamzee': {
        'acronym': 'TC',
        'name': 'terminallyCapricious',
        'color': '2B0057',
        'quirk_prefix': '',
        'case': 'alternating',
        'replacements': '[["/.*/", "$L"], ["/([\w\s]|[\w\'\w])([\w\'\w]|[\w\s])?/", "$U"], ["/:O\)/", ":o)"], ["/;O\)/", ";o)"], ["/:O\(", ":o("]]'
	},
    'gamzee (sober)': {
        'acronym': 'TC',
        'name': 'terminallyCapricious',
        'color': '2B0057',
        'quirk_prefix': '',
        'case': 'normal',
        'replacements': []
    },
    'eridan': {
        'acronym': 'CA',
        'name': 'caligulasAquarium',
        'color': '6A006A',
        'quirk_prefix': '',
        'case': 'normal',
        'replacements': '[["/([A-Z][a-z]+\b)/", "$L"], ["/(\b)([A-Z][A-Z]+)(\b)/", "¥$2¥"], ["/(\b)([A-Z]\'[A-Z]+)(\b)/", "¥$2¥"], ["/.*/", "$L"], ["/¥([\w|\']+)¥/", "$U"], ["¥", " "], ["/([A-Z]\W[a-z]\W[A-Z])/", "$U"], ["/([A-Z]\'[a-z])/", "$U"], ["/(\w)\'(\w)/", "$1$2"], ["/(\w)\.$/", "$1"], ["/([vVwW]/", "$1$1"], ["/[\s|^]([:;][dop])/", "$U"], ["/[\s|^](d[:;])/", "$U"]]'
	},
    'feferi': {
        'acronym': 'CC',
        'name': 'cuttlefishCuller',
        'color': '77003C',
        'quirk_prefix': '',
        'case': 'normal',
        'replacements': '[["/^(\w)/", "$U"], ["/[!|\?|\.](\s\w)/", "$U"], ["/[\s|^](i)[\'|\W|$]/", "$U"], ["/[hH]/", ")("], ["E", "-E"]]'
	},
    'damara': {
        'acronym': 'DAMARA',
        'name': 'Damara',
        'color': 'A10000',
        'quirk_prefix': '',
        'case': 'upper',
        'replacements': '[]'
    },
    'rufioh': {
        'acronym': 'RUFIOH',
        'name': 'Rufioh',
        'color': 'A15000',
        'quirk_prefix': '',
        'case': 'lower',
        'replacements': '[["i", "1"], ["/(^|\s)ass(\W|$)/", "$1*ss$2"], ["/(^|\s)cripple(\W|$)/", "$1cr*pple$2"], ["damn", "d*mn"], ["/(^|\s)fuck1ng(\W|$)/", "$1f***1ng$2"], ["fuck", "f*ck"], ["/(^|\s)hell(\W|$)/", "$1h*ll$2"], ["/(^|\s)mutant(\W|$)/", "$1m*tant$2"], ["/(^|\s)sh1t(\W|$)/", "$1sh*t$2"], ["/[\s|^|}](:O)/", "$L"], ["/[\s|^|}](:[dp])/", "$U"]]'
	},
    'mituna':{
        'acronym': 'MITUNA',
        'name': 'Mituna',
        'color': 'A1A100',
        'quirk_prefix': '',
        'case': 'upper',
        'replacements': '[["A", "4"], ["B", "8"], ["E", "3"], ["I", "1"], ["O", "0"], ["S", "5"], ["T", "7"], ["/(\w)\'(\w)/", "$1$2"], ["/(\w)\.$/", "$1"]]'
	},
    'kankri':{
        'acronym': 'KANKRI',
        'name': 'Kankri',
        'color': 'FF0000',
        'quirk_prefix': '',
        'case': 'normal',
        'replacements': '[["/[bB]/", "6"], ["/[oO]/", "9"], ["/^(\w)/", "$U"], ["/[!|\?|\.](\s\w)/", "$U"], ["/[\s|^](i)[\'|\W|$]/", "$U"]]'
	},
    'meulin': {
        'acronym': 'MEULIN',
        'name': 'Meulin',
        'color': '416600',
        'quirk_prefix': '(^･ω･^) <',
        'case': 'upper',
        'replacements': '[["EE", "33"]]'
    },
    'porrim':{
        'acronym':'PORRIM',
        'name':'Porrim',
        'color':'008141',
        'quirk_prefix': '',
        'case': 'normal',
        'replacements': '[["/^(\w)/", "$U"], ["/[!|\?|\.](\s\w)/", "$U"], ["/[\s|^](i)[\'|\W|$]/", "$U"], ["o", "o+"], ["0", "0+"], ["/(^|\s)[pP]lus(\W|$)/", "$1+$2"], ["/(^|\s)PLUS(\W|$)/", "$1+$2"]]'
	},
    'latula': {
        'acronym': 'LATULA',
        'name': 'Latula',
        'color': '008282',
        'quirk_prefix': '',
        'case': 'normal',
        'replacements': '[["/([A-Z][a-z]+\b)/", "$L"], ["/(\b)([A-Z][A-Z]+)(\b)/", "¥$2¥"], ["/(\b)([A-Z]\'[A-Z]+)(\b)/", "¥$2¥"], ["/.*/", "$L"], ["/¥([\w|\']+)¥/", "$U"], ["¥", " "], ["/([A-Z]\W[a-z]\W[A-Z])/", "$U"], ["/([A-Z]\'[a-z])/", "$U"], ["/(\w)\'(\w)/", "$1$2"], ["/[aA]/", "4"], ["/[iI]/", "1"], ["/[eE]/", "3"], ["/[\s|^|>|&gt;]([:;8x]d)/", "$U"], ["/[\s|^|>|&gt;]([:;8x]o)/", "$U"], ["/[\s|^|>|&gt;]([:;8x]p)/", "$U"]]'
	},
    'aranea': {
        'acronym': 'ARANEA',
        'name': 'Aranea',
        'color': '005682',
        'quirk_prefix': '',
        'case': 'normal',
        'replacements': '[["/[bB]/", "8"], ["(m)", "♏"], ["/^(\w)/", "$U"], ["/[!|\?|\.](\s\w)/", "$U"], ["/[\s|^](i)[\'|\W|$]/", "$U"]]'
	},
    'horuss': {
        'acronym': 'HORUSS',
        'name': 'Horuss',
        'color': '000056',
        'quirk_prefix': '8=D <',
        'case': 'normal',
        'replacements': '[["/[lL][oO][oO]/", "100"],["/[xX]/", "%"], ["/(\b[sS][tT][rR][oO][nN][gG]\w*)/", "$U"], ["/(\b[sS][tT][rR][eE][nN][gG][tT][hH]\w*)/", "$U"], ["/[oO][oO][lL]/", "001"], ["/^(\w)/", "$U"], ["/[!|\?|\.](\s\w)/", "$U"], ["/[\s|^](i)[\'|\W|$]/", "$U"]]'
	},
    'kurloz': {
        'acronym': 'KURLOZ',
        'name': 'Kurloz',
        'color': '2B0057',
        'quirk_prefix': 'SIGNS: <',
        'case': 'upper',
        'replacements': '[]'
    },
    'cronus': {
        'acronym': 'CRONUS',
        'name': 'Cronus',
        'color': '6A006A',
        'quirk_prefix': '',
        'case': 'normal',
        'replacements': '[["/([A-Z][a-z]+\b)/", "$L"], ["/(\b)([A-Z][A-Z]+)(\b)/", "¥$2¥"], ["/(\b)([A-Z]\'[A-Z]+)(\b)/", "¥$2¥"], ["/.*/", "$L"], ["/¥([\w|\']+)¥/", "$U"], ["¥", " "], ["/([A-Z]\W[a-z]\W[A-Z])/", "$U"], ["/([A-Z]\'[a-z])/", "$U"], ["/(\w)\'(\w)/", "$1$2"], ["/([^|\s])v/", "$1w"], ["/([^|\s])V/", "$1W"], ["/\bv|w\b/", "α"], ["/w|v/", "φ"], ["α", "wv"], ["φ", "vw"], ["/\bV|W\b/", "Ά"], ["/W|V/", "Á"], ["Ά", "WV"], ["Á", "VW"], ["B", "8"], ["/(\w)vws(\s|\.|!|\?|$)/", "$1wvs$2"], ["/(\w)VWS(\s|\.|!|\?|$)/", "$1WVS$2"], ["/(\w)\.(\w)/", "$1$2"], ["/[\s|^]([:;]d)/", "$U"], ["/[\s|^](d[:;])", "$U"]]'
	},
    'meenah': {
        'acronym': 'MEENAH',
        'name': 'Meenah',
        'color': '77003C',
        'quirk_prefix': '',
        'case': 'normal',
        'replacements': '[["/([A-Z][a-z]+\b)/", "$L"], ["/(\b)([A-Z][A-Z]+)(\b)/", "¥$2¥"], ["/(\b)([A-Z]\'[A-Z]+)(\b)/", "¥$2¥"], ["/.*/", "$L"], ["/¥([\w|\']+)¥/", "$U"], ["¥", " "], ["/([A-Z]\W[a-z]\W[A-Z])/", "$U"], ["/([A-Z]\'[a-z])/", "$U"], ["/(\w)\'(\w)/", "$1$2"], ["/(\w)\.$/", "$1"], ["E", "-E"], ["H", ")("], ["/[\s|^](3[8x][odp])/", "$U"]]'
	},
    'dad': {
        'acronym': 'pipefan413',
        'name': 'Dad',
        'color': '4B4B4B',
        'quirk_prefix': '',
        'case': 'upper',
        'replacements': '[]'
    },
    'nanna': {
        'acronym': 'NANNA',
        'name': 'Nanna',
        'color': '000000',
        'quirk_prefix': '',
        'case': 'normal',
        'replacements': '[["/^(\w)/", "$U"], ["/[!|\?|\.](\s\w)/", "$U"], ["/[\s|^](i)[\'|\W|$]/", "$U"]]'
	},
    'mom': {
        'acronym': 'MOM',
        'name': 'Mom',
        'color': '000000',
        'quirk_prefix': '',
        'case': 'normal',
        'replacements': '[["/([A-Z][a-z]+\b)/", "$L"], ["/(\b)([A-Z][A-Z]+)(\b)/", "¥$2¥"], ["/(\b)([A-Z]\'[A-Z]+)(\b)/", "¥$2¥"], ["/.*/", "$L"], ["/¥([\w|\']+)¥/", "$U"], ["¥", " "], ["/([A-Z]\W[a-z]\W[A-Z])/", "$U"], ["/([A-Z]\'[a-z])/", "$U"], ["/(\w)\'(\w)/", "$1$2"], ["/(\w)\.$/", "$1"], ["/[\s|^]([:;]d)/", "$U"], ["/[\s|^](d[:;])/", "$U"]]'
	},
    'bro': {
        'acronym': 'BRO',
        'name': 'Bro',
        'color': '000000',
        'quirk_prefix': '',
        'case': 'normal',
        'replacements': '[["/^(\w)/", "$U"], ["/[!|\?|\.](\s\w)/", "$U"], ["/[\s|^](i)[\'|\W|$]/", "$U"]]'
	},
    'grandpa': {
        'acronym': 'GRANDPA',
        'name': 'Grandpa',
        'color': '000000',
        'quirk_prefix': '',
        'case': 'normal',
        'replacements': '[["\'", " "], ["/.*/", "$L"], ["/^(\w)/", "$U"], ["/[!|\?|\.](\s\w)/", "$U"], ["/[\s|^]([:;]d)/", "$U"], ["/[\s|^]([:;]p)/", "$U"]]'
	},
    'poppop': {
        'acronym': 'POPPOP',
        'name': 'Poppop',
        'color': '000000',
        'quirk_prefix': '',
        'case': 'normal',
        'replacements': '[["/([A-Z][a-z]+\b)/", "$L"], ["/(\b)([A-Z][A-Z]+)(\b)/", "¥$2¥"], ["/(\b)([A-Z]\'[A-Z]+)(\b)/", "¥$2¥"], ["/.*/", "$L"], ["/¥([\w|\']+)¥/", "$U"], ["¥", " "], ["/([A-Z]\W[a-z]\W[A-Z])/", "$U"], ["/([A-Z]\'[a-z])/", "$U"], ["/[\s|^]([:;]d)/", "$U"], ["[\s|^](d[:;])", "$U"]]'
	},
    'alpha mom': {
        'acronym': 'MOM',
        'name': 'Mom',
        'color': '000000',
        'quirk_prefix': '',
        'case': 'normal',
        'replacements': '[["/^(\w)/", "$U"], ["/[!|\?|\.](\s\w)/", "$U"], ["/[\s|^](i)[\'|\W|$]/", "$U"]]'
	},
    'alpha bro': {
        'acronym': 'BRO',
        'name': 'Bro',
        'color': '000000',
        'quirk_prefix': '',
        'case': 'normal',
        'replacements': '[["/([A-Z][a-z]+\b)/", "$L"], ["/(\b)([A-Z][A-Z]+)(\b)/", "¥$2¥"], ["/(\b)([A-Z]\'[A-Z]+)(\b)/", "¥$2¥"], ["/.*/", "$L"], ["/¥([\w|\']+)¥/", "$U"], ["¥", " "], ["/([A-Z]\W[a-z]\W[A-Z])/", "$U"], ["/([A-Z]\'[a-z])/", "$U"], ["/(\w)\'(\w)/", "$1$2"], ["/(\w)\.$/", "$1"], ["/[\s|^]([:;]d)/", "$U"], ["/[\s|^](d[:;])/", "$U"]]'
	},
    'grandma': {
        'acronym': 'GRANDMA',
        'name': 'Grandma',
        'color': '000000',
        'quirk_prefix': '',
        'case': 'normal',
        'replacements': '[["/([A-Z][a-z]+\b)/", "$L"], ["/(\b)([A-Z][A-Z]+)(\b)/", "¥$2¥"], ["/(\b)([A-Z]\'[A-Z]+)(\b)/", "¥$2¥"], ["/.*/", "$L"], ["/¥([\w|\']+)¥/", "$U"], ["¥", " "], ["/([A-Z]\W[a-z]\W[A-Z])/", "$U"], ["/([A-Z]\'[a-z])/", "$U"], ["/(\w)\'(\w)/", "$1$2"], ["/(\w)\.$/", "$1"], ["/[\s|^]([:;]d)/", "$U"], ["/[\s|^](d[:;])/", "$U"], ["/[\s|^]([:;]b)/", "$U"]]'
	},
    'nannasprite': {
        'acronym': 'NANNASPRITE',
        'name': 'Nannasprite',
        'color': '00D5F2',
        'quirk_prefix': '',
        'case': 'normal',
        'replacements': '[["/^(\w)/", "$U"], ["/[!|\?|\.](\s\w)/", "$U"], ["/[\s|^](i)[\'|\W|$]/", "$U"]]'
	},
    'jaspersprite': {
        'acronym': 'JASPERSPRITE',
        'name': 'Jaspersprite',
        'color': 'F141EF',
        'quirk_prefix': '',
        'case': 'normal',
        'replacements': '[["/^(\w)/", "$U"], ["/[!|\?|\.](\s\w)/", "$U"], ["/[\s|^](i)[\'|\W|$]/", "$U"], ["/(\w)\'(\w)/", "$1$2"]]'
	},
    'calsprite': {
        'acronym': 'CALSPRITE',
        'name': 'Calsprite',
        'color': 'F2A400',
        'quirk_prefix': '',
        'case': 'upper',
        'replacements': '[["A", "<"], ["B", ">"], ["C", "?"], ["D", "<"], ["E", ">"], ["F", "?"], ["G", "<"], ["H", ">"], ["I", "?"], ["J", "<"], ["K", ">"], ["L", "?"], ["M", "<"], ["N", ">"], ["O", "?"], ["P", "<"], ["Q", ">"], ["R", "?"], ["S", "<"], ["T", ">"], ["U", "?"], ["V", "<"], ["W", ">"], ["X", "?"], ["Y", "<"], ["Z", ">"], ["<", "HAA "], [">", "HEE "], ["?", "HOO "]]'
    },
    'davesprite': {
        'acronym': 'DAVESPRITE',
        'name': 'Davesprite',
        'color': 'F2A400',
        'quirk_prefix': '',
        'case': 'normal',
		'replacements': '[["/([A-Z][a-z]+\b)/", "$L"], ["/(\b)([A-Z][A-Z]+)(\b)/", "¥$2¥"], ["/(\b)([A-Z]\'[A-Z]+)(\b)/", "¥$2¥"], ["/.*/", "$L"], ["/¥([\w|\']+)¥/", "$U"], ["¥", " "], ["/([A-Z]\W[a-z]\W[A-Z])/", "$U"], ["/([A-Z]\'[a-z])/", "$U"], ["/(\w)\'(\w)/", "$1$2"], ["/(\w)\.$/", "$1"], ["/[\s|^]([:;]d)/", "$U"], ["/[\s|^](d[:;])/", "$U"]]'
	},
    'jadesprite': {
        'acronym': 'JADESPRITE',
        'name': 'Jadesprite',
        'color': '1F9400',
        'quirk_prefix': '',
        'case': 'normal',
        'replacements': '[["/([A-Z][a-z]+\b)/", "$L"], ["/(\b)([A-Z][A-Z]+)(\b)/", "¥$2¥"], ["/(\b)([A-Z]\'[A-Z]+)(\b)/", "¥$2¥"], ["/.*/", "$L"], ["/¥([\w|\']+)¥/", "$U"], ["¥", " "], ["/([A-Z]\W[a-z]\W[A-Z])/", "$U"], ["/([A-Z]\'[a-z])/", "$U"], ["/(\w)\'(\w)/", "$1$2"], ["/(\w)\.$/", "$1"], ["/[\s|^]([:;]d)/", "$U"], ["/[\s|^](d[:;])/", "$U"], ["/[\s|^]([:;]b)/", "$U"]]'
	},
    'aradiasprite': {
        'acronym': 'ARADIASPRITE',
        'name': 'Aradiasprite',
        'color': 'A10000',
        'quirk_prefix': '',
        'case': 'lower',
       'replacements': '[["o", "0"], ["/(\w)\'(\w)/", "$1$2"], ["/(\w)\.$/", "$1"]]'
	},
    'tavrisprite': {
        'acronym': 'TAVRISPRITE',
        'name': 'Tavrisprite',
        'color': '0715CD',
        'quirk_prefix': '',
        'case': 'normal',
        'replacements': '[["b", "8"]]'
    },
    'fefetasprite': {
        'acronym': 'FEFETASPRITE',
        'name': 'Fefetasprite',
        'color': 'B536DA',
        'quirk_prefix': '3833 <',
        'case': 'normal',
        'replacements': '[["/^(\w)/", "$U"], ["/[!|\?|\.](\s\w)/", "$U"], ["/[\s|^](i)[\'|\W|$]/", "$U"], ["/(\w)\'(\w)/", "$1$2"], ["/(\w)\.$/", "$1"], ["/[eE][eE]/", "33"], ["/[hH]/", ")("], ["E", "-E"]]'
	},
    'erisolsprite': {
        'acronym': 'ERISOLSPRITE',
        'name': 'Erisolsprite',
        'color': '4AC925',
        'quirk_prefix': '',
        'case': 'normal',
        'replacements': '[["/([A-Z][a-z]+\b)/", "$L"], ["/(\b)([A-Z][A-Z]+)(\b)/", "¥$2¥"], ["/(\b)([A-Z]\'[A-Z]+)(\b)/", "¥$2¥"], ["/.*/", "$L"], ["/¥([\w|\']+)¥/", "$U"], ["¥", " "], ["/([A-Z]\W[a-z]\W[A-Z])/", "$U"], ["/([A-Z]\'[a-z])/", "$U"], ["/(\w)\'(\w)/", "$1$2"], ["/([iI])/", "$1$1"], ["/[sS]/", "2"], ["/([vVwW])/", "$1$1"], ["/[\s|^]([:;][dop])/", "$U"], ["/[\s|^](d[:;])/", "$U"]]'
	},
    'arquiusprite': {
        'acronym': 'ARQUIUSPRITE',
        'name': 'ARquiusprite',
        'color': 'e00707',
        'quirk_prefix': '◥▶◀◤ —>',
        'case': 'normal',
        'replacements': '[["/[lL][oO][oO]/", "100"], ["/[xX]/", "%"], ["/(\b[sS][tT][rR][oO][nN][gG]\w*)/", "$U"], ["/[oO][oO][lL]/", "001"], ["/(\w)\.$/", "$1"], ["/^(\w)/", "$U"], ["/[!|\?|\.](\s\w)/", "$U"], ["/[\s|^](i)[\'|\W|$]/", "$U"], ["/([sS])hit/", "$1▓▒▒"], ["/([fF])ucking/", "$1▒▓▒▒▒▒"], ["/([fF])ucker/", "$1▒▓▒▒▒"], ["/(^|\s)([aA])ss(\W|$)/", "$1$2▒▒$3"], ["/([fF])uck/", "$1▒▒▓"], ["/([bB])itch/", "$1▒▓▒▒"], ["/([hH])ell/", "$1▒▒▒"], ["/([dD])amn/", "$1▒▒▒"]]'
	},
    'the handmaid': {
        'acronym': '♈',
        'name': 'The Handmaid',
        'color': 'A10000',
        'quirk_prefix': '',
        'case': 'normal',
        'replacements': '[["/([A-Z][a-z]+\b)/", "$L"], ["/(\b)([A-Z][A-Z]+)(\b)/", "¥$2¥"], ["/(\b)([A-Z]\'[A-Z]+)(\b)/", "¥$2¥"], ["/.*/", "$L"], ["/¥([\w|\']+)¥/", "$U"], ["¥", " "], ["/([A-Z]\W[a-z]\W[A-Z])/", "$U"], ["/([A-Z]\'[a-z])/", "$U"], ["/(\w)\'(\w)/", "$1$2"], ["/(\w)\.$/", "$1"], ["/[oO]/", "Ø"]]'
	},
    'the summoner': {
        'acronym': '♉',
        'name': 'The Summoner',
        'color': 'A15000',
        'quirk_prefix': '',
        'case': 'normal',
        'replacements': '[["/^(\w)/", "$U"], ["/[!|\?|\.](\s\w)/", "$U"], ["/[\s|^](i)[\'|\W|$]/", "$U"], [".", ","], ["/[iI]/", "1"]]'
	},
    'the psiioniic':{
        'acronym': '♊',
        'name': 'The Ψiioniic',
        'color': 'A1A100',
        'quirk_prefix': '',
        'case': 'normal',
        'replacements': '[["/^(\w)/", "$U"], ["/[!|\?|\.](\s\w)/", "$U"], ["/[\s|^](i)[\'|\W|$]/", "$U"], ["/(\w)\'(\w)/", "$1$2"], ["/psi|psy/", "ψi"], ["/Psi|Psy/", "Ψi"], ["/PSI|PSY/", "Ψi"], ["/([iI])/", "$1$1"], ["/[sS]/", "2"]]'
	},
    'the helmsman': {
        'acronym': '♊',
        'name': 'The Helmsman',
        'color': 'A1A100',
        'quirk_prefix': '',
        'case': 'upper',
        'replacements': '[["\'", " "], ["/(\w\w)/", "-$1"], ["/(\w\w)(\.$)/", "$1-.."],["/(\w\w)(!$)/", "$1-!!"],["/(\w\w)(\?$)/", "$1-??"], ["/(\w\w)(\w$)/", "$1-$2$2"],["/(-\w)\.(?=$|\s)/", "$10-.."],["/(-\w\w)\.(?=$|\s)/", "$1-.."],["/(-\w)!(?=$|\s)/", "$10-!!"], ["/(-\w\w)!(?=$|\s)/", "$1-!!"],["/(-\w)\?(?=$|\s)/", "$10-??"],["/(-\w\w)\?(?=$|\s)/", "$1-??"],["/(-\w)(?=\s)/", "$10"],["/(\w\w)(\w)\./", "$1-$2$2-.."],["/(\w\w)(\w)!/", "$1-$2$2-!!"],["/(\w\w)(\w)\?/", "$1-$2$2-??"],["/(\w\w)(\w)/", "$1-$2$2"], ["/(^|\W)(\w)\./", "$1-$2$2-.."], ["/(^|\S)-(\S|$)/", "$1 $2"], ["-", " "], ["/[oO]/", "0"], ["/[iI]/", "1"], ["/[eE]/", "3"], ["/[aA]/", "4"], ["/[gG]/", "6"], ["/[zZ]/", "2"], ["/[sS]/", "5"], ["/[tT]/", "7"], ["/[bB]/", "8"]]'
	},
    'the signless': {
        'acronym': '♋',
        'name': 'The Signless',
        'color': '626262',
        'quirk_prefix': '',
        'case': 'normal',
        'replacements': '[["/^(\w)/", "$U"], ["/[!|\?|\.](\s\w)/", "$U"], ["/[\s|^](i)[\'|\W|$]/", "$U"]]'
	},
    'the disciple': {
        'acronym': '♌',
        'name': 'The Disciple',
        'color': '416600',
        'quirk_prefix': '',
        'case': 'normal',
        'replacements': '[["/[eE][eE]/", "33"], ["/^(\w)/", "$U"], ["/[!|\?|\.](\s\w)/", "$U"], ["/[\s|^](i)[\'|\W|$]/", "$U"], ["/(\w)\'(\w)/", "$1$2"]]'
	},
    'the dolorosa': {
        'acronym': '♍',
        'name': 'The Dolorosa',
        'color': '008141',
        'quirk_prefix': '',
        'case': 'normal',
        'replacements': '[["/^(\w)/", "$U"], ["/[!|\?|\.](\s\w)/", "$U"], ["/[\s|^](i)[\'|\W|$]/", "$U"], ["/(\w)\'(\w)/", "$1$2"], ["/(\w)\.$/", "$1"], ["/(\w),(\s\w)/", "$1$2"]]'
	},
    'redglare': {
        'acronym': '♎',
        'name': 'Neophyte Redglare',
        'color': '008282',
        'quirk_prefix': '',
        'case': 'normal',
        'replacements': '[["/[aA]/", "4"], ["/[eE]", "3"], ["/[iI]/", "1"],  ["/^(\w)/", "$U"], ["/[!|\?|\.](\s\w)/", "$U"], ["/[\s|^](i)[\'|\W|$]/", "$U"], ["/(\w)\'(\w)/", "$1$2"]]'
	},
    'mindfang': {
        'acronym': '♏',
        'name': 'Marquise Spinneret Mindfang',
        'color': '005682',
        'quirk_prefix': '',
        'case': 'normal',
        'replacements': '[["/[bB]/", "8"], ["(m)", "♏"], ["/^(\w)/", "$U"], ["/[!|\?|\.](\s\w)/", "$U"], ["/[\s|^](i)[\'|\W|$]/", "$U"]]'
	},
    'darkleer': {
        'acronym': '♐',
        'name': 'E%ecutor Darkleer',
        'color': '000056',
        'quirk_prefix': '-+->',
        'case': 'normal',
        'replacements': '[["/[lL][oO][oO]/", "100"],["/[xX]/", "%"], ["/(\b[sS][tT][rR][oO][nN][gG]\w*)/", "$U"], ["/(\b[sS][tT][rR][eE][nN][gG][tT][hH]\w*)/", "$U"], ["/[oO][oO][lL]/", "001"], ["/^(\w)/", "$U"], ["/[!|\?|\.](\s\w)/", "$U"], ["/[\s|^](i)[\'|\W|$]/", "$U"]]'
	},
    'grand highblood': {
        'acronym': '♑',
        'name': 'The Grand Highblood',
        'color': '2B0057',
        'quirk_prefix': '',
        'case': 'normal',
        'replacements': '[["/^(\w)/", "$U"], ["/[!|\?|\.](\s\w)/", "$U"], ["/[\s|^](i)[\'|\W|$]/", "$U"]]'
	},
    'dualscar': {
        'acronym': '♒',
        'name': 'Orphaner Dualscar',
        'color': '6A006A',
        'quirk_prefix': '',
        'case': 'normal',
        'replacements': '[["/([A-Z][a-z]+\b)/", "$L"], ["/(\b)([A-Z][A-Z]+)(\b)/", "¥$2¥"], ["/(\b)([A-Z]\'[A-Z]+)(\b)/", "¥$2¥"], ["/.*/", "$L"], ["/¥([\w|\']+)¥/", "$U"], ["¥", " "], ["/([A-Z]\W[a-z]\W[A-Z])/", "$U"], ["/([A-Z]\'[a-z])/", "$U"], ["/(\w)\'(\w)/", "$1$2"], ["/([^|\s])v/", "$1w"], ["/([^|\s])V/", "$1W"], ["/\bv|w\b/", "α"], ["/w|v/", "φ"], ["α", "wv"], ["φ", "vw"], ["/\bV|W\b/", "Ά"], ["/W|V/", "Á"], ["Ά", "WV"], ["Á", "VW"], ["B", "8"], ["/(\w)vws(\s|\.|!|\?|$)/", "$1wvs$2"], ["/(\w)VWS(\s|\.|!|\?|$)/", "$1WVS$2"], ["/(\w)\.(\w)/", "$1$2"], ["/[\s|^]([:;]d)/", "$U"], ["/[\s|^](d[:;])", "$U"]]'
	},
    'the condesce': {
        'acronym': '♓',
        'name': 'Her Imperious Condescension',
        'color': '77003C',
        'quirk_prefix': '',
        'case': 'normal',
        'replacements': '[["/([A-Z][a-z]+\b)/", "$L"], ["/(\b)([A-Z][A-Z]+)(\b)/", "¥$2¥"], ["/(\b)([A-Z]\'[A-Z]+)(\b)/", "¥$2¥"], ["/.*/", "$L"], ["/¥([\w|\']+)¥/", "$U"], ["¥", " "], ["/([A-Z]\W[a-z]\W[A-Z])/", "$U"], ["/([A-Z]\'[a-z])/", "$U"], ["/(\w)\'(\w)/", "$1$2"], ["/(\w)\.$/", "$1"], ["E", "-E"], ["H", ")("], ["/[\s|^](3[8x][odp])/", "$U"]]'
	},
    'spades slick': {
        'acronym': '♠',
        'name': 'Spades Slick',
        'color': '000000',
        'quirk_prefix': '',
        'case': 'lower',
        'replacements': '[]'
    },
    'clubs deuce': {
        'acronym': '♣',
        'name': 'Clubs Deuce',
        'color': '000000',
        'quirk_prefix': '',
        'case': 'upper',
        'replacements': '[]'
    },
    'diamonds droog': {
        'acronym': '♦',
        'name': 'Diamonds Droog',
        'color': '000000',
        'quirk_prefix': '',
        'case': 'normal',
        'replacements': '[["/^(\w)/", "$U"], ["/[!|\?|\.](\s\w)/", "$U"], ["/[\s|^](i)[\'|\W|$]/", "$U"]]'
	},
    'hearts boxcars': {
        'acronym': '♥',
        'name': 'Hearts Boxcars',
        'color': '000000',
        'quirk_prefix': '',
        'case': 'upper',
        'replacements': '[["/(\w)\'(\w)/", "$1$2"], ["/(\w),(\s\w)/", "$1$2"], ["/(\w)\.(\s\w)/", "$1$2"], ["/(\w)\.$/", "$1"], ["/(^|\s)YOURE(\W|$)/", "$1YER$2"], ["/(^|\s)FOR(\W|$)/", "$1FER$2"], ["/(^|\s)YOURS(\W|$)/", "$1YERS$2"], ["/(^|\s)YOUR(\W|$)/", "$1YER$2"], ["/(^|\s)THEM(\W|$)/", "$1EM$2"] ]'
	}
}

