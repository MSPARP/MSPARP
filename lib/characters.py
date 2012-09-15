CHARACTER_GROUPS = [
    'Special/Other',
    'Humans',
    'Post-scratch Trolls',
    'Pre-scratch Trolls',
]

CHARACTERS = {
    'Special/Other': [
        'Anonymous/Other',
        'Original Character',
        'Doc Scratch',
        'Calliope',
        'Caliborn',
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
        'Aradia',
        'Tavros',
        'Sollux',
        'Karkat',
        'Nepeta',
        'Kanaya',
        'Terezi',
        'Vriska',
        'Equius',
        'Gamzee',
        'Eridan',
        'Feferi',
    ],
    'Pre-scratch Trolls': [
        'Kankri',
        'Porrim',
        'Latula',
        'Aranea',
        'Meenah',
    ],
}

# XXX THIS IS JUST A DUPLICATE OF CHARACTERS.JS

CHARACTER_DETAILS = {
	'anonymous/other': {
		'acronym': '??',
		'name': 'anonymous',
		'color': '000000',
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': []
	},
	'original character': {
		'acronym': '**',
		'name': 'Original Character',
		'color': 'FF00FF',
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': []
	},
	'doc scratch': {
		'acronym': '',
		'name': 'Doc Scratch',
		'color': 'FFFFFF',
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': []
	},
	'calliope': {
		'acronym': 'UU',
		'name': 'uranianUmbra',
		'color': '929292',
		'quirk_prefix': '',
		'case': 'lower',
		'replacements': '[["u", "U"]]'
	},
	'caliborn': {
		'acronym': 'uu',
		'name': 'undyingUmbrage',
		'color': '323232',
		'quirk_prefix': '',
		'case': 'upper',
		'replacements': '[["U", "u"]]'
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
		'replacements': '[]'
	},
	'rose': {
		'acronym': 'TT',
		'name': 'tentacleTherapist',
		'color': 'B536DA',
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': '[]'
	},
	'dave': {
		'acronym': 'TG',
		'name': 'turntechGodhead',
		'color': 'E00707',
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': '[]'
	},
	'jade': {
		'acronym': 'GG',
		'name': 'gardenGnostic',
		'color': '4AC925',
		'quirk_prefix': '',
		'case': 'lower',
		'replacements': '[]'
	},
	'jane': {
		'acronym': 'GG',
		'name': 'gutsyGumshoe',
		'color': '00D5F2',
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': '[]'
	},
	'roxy': {
		'acronym': 'TG',
		'name': 'tipsyGnostalgic',
		'color': 'FF6FF2',
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': '[]'
	},
	'dirk': {
		'acronym': 'TT',
		'name': 'timaeusTestified',
		'color': 'F2A400',
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': '[]'
	},
	'jake': {
		'acronym': 'GT',
		'name': 'golgothasTerror',
		'color': '1F9400',
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': '[]'
	},
	'aradia': {
		'acronym': 'AA',
		'name': 'apocalypseArisen',
		'color': 'A10000',
		'quirk_prefix': '',
		'case': 'lower',
		'replacements': '[["o", "0"]]'
	},
	'tavros': {
		'acronym': 'AT',
		'name': 'adiosToreador',
		'color': 'A15000',
		'quirk_prefix': '',
		'case': 'inverted',
		'replacements': '[[".", ","]]'
	},
	'sollux':{
		'acronym': 'TA',
		'name': 'twinArmageddons',
		'color': 'A1A100',
		'quirk_prefix': '',
		'case': 'lower',
		'replacements': '[["i", "ii"], ["s", "2"]]'
	},
	'karkat':{
		'acronym': 'CG',
		'name': 'carcinoGeneticist',
		'color': '626262',
		'quirk_prefix': '',
		'case': 'upper',
		'replacements': '[]'
	},
	'nepeta': {
		'acronym': 'AC',
		'name': 'arsenicCatnip',
		'color': '416600',
		'quirk_prefix': ':33 <',
		'case': 'lower',
		'replacements': '[["ee", "33"]]'
	},
	'kanaya':{
		'acronym':'GA',
		'name':'grimAuxiliatrix',
		'color':'008141',
		'quirk_prefix': '',
		'case': 'title',
		'replacements': '[]'
	},
	'terezi': {
		'acronym': 'GC',
		'name': 'gallowsCalibrator',
		'color': '008282',
		'quirk_prefix': '',
		'case': 'upper',
		'replacements': '[["A", "4"], ["E", "3"], ["I", "1"]]'
	},
	'vriska': {
		'acronym': 'AG',
		'name': 'arachnidsGrip',
		'color': '005682',
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': '[["B", "8"], ["b", "8"]]'
	},
	'equius': {
		'acronym': 'CT',
		'name': 'centaursTesticle',
		'color': '000056',
		'quirk_prefix': 'D -->',
		'case': 'normal',
		'replacements': '[["X", "%"], ["x", "%"], ["loo", "100"], ["ool", "001"]]'
		
	},
	'gamzee': {
		'acronym': 'TC',
		'name': 'terminallyCapricious',
		'color': '2B0057',
		'quirk_prefix': '',
		'case': 'alternating',
		'replacements': '[]'
	},
	'eridan': {
		'acronym': 'CA',
		'name': 'caligulasAquarium',
		'color': '6A006A',
		'quirk_prefix': '',
		'case': 'lower',
		'replacements': '[["v", "vv"], ["w", "ww"]]'
	},
	'feferi': {
		'acronym': 'CC',
		'name': 'cuttlefishCuller',
		'color': '77003C',
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': '[["E", "-E"], ["H", ")("], ["h", ")("]]'
	},
	'aranea': {
		'acronym': 'ARANEA',
		'name': 'Aranea',
		'color': '005682',
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': '[["B", "8"], ["b", "8"]]'
	},
	'meenah': {
		'acronym': 'MEENAH',
		'name': 'Meenah',
		'color': '77003C',
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': '[["E", "-E"], ["H", ")("]]'
	}
}

