# -*- coding: utf-8 -*-

CHARACTER_GROUPS = [
    'Special/Other',
    'Humans',
    'Post-scratch Trolls',
    'Pre-scratch Trolls',
    'Sprites',
    'Ancestors',
]

CHARACTERS = {
    'Special/Other': [
        'Anonymous/Other',
        'Original Character',
        'Guardian',
        'Midnight Crew',
        'Trickster',
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
    'Sprites': [
        'Nannasprite',
        'Jaspersprite',
        'Calsprite',
        'Davesprite',
        'Jadesprite',
        'Tavrisprite',
        'Fefetasprite',
        'Erisolsprite',
    ],
    'Ancestors': [
        'The Handmaid',
        'The Summoner',
        'The Psiioniic',
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
}

# XXX THIS IS JUST A DUPLICATE OF CHARACTERS.JS

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
		'replacements': '[]'
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
		'case': 'normal',
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
		'case': 'normal',
		'replacements': '[["I", "II"], ["i", "ii"], ["S", "2"], ["s", "2"]]'
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
		'case': 'normal',
		'replacements': '[["V", "VV"], ["v", "vv"], ["W", "WW"], ["w", "ww"]]'
	},
	'feferi': {
		'acronym': 'CC',
		'name': 'cuttlefishCuller',
		'color': '77003C',
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': '[["E", "-E"], ["H", ")("], ["h", ")("]]'
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
		'replacements': '[["i", "1"]]'
	},
	'mituna':{
		'acronym': 'MITUNA',
		'name': 'Mituna',
		'color': 'A1A100',
		'quirk_prefix': '',
		'case': 'upper',
		'replacements': '[["A", "4"], ["B", "8"], ["E", "3"], ["I", "1"], ["O", "0"], ["S", "5"], ["T", "7"]]'
	},
	'kankri':{
		'acronym': 'KANKRI',
		'name': 'Kankri',
		'color': 'FF0000',
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': '[["B", "6"], ["b", "6"], ["O", "9"], ["o", "9"]]'
	},
	'meulin': {
		'acronym': 'MEULIN',
		'name': 'Meulin',
		'color': '416600',
		'quirk_prefix': '(=｀ω´=) <',
		'case': 'upper',
		'replacements': '[["EE", "33"]]'
	},
	'porrim':{
		'acronym':'PORRIM',
		'name':'Porrim',
		'color':'008141',
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': '[["o", "o+"]]'
	},
	'latula': {
		'acronym': 'LATULA',
		'name': 'Latula',
		'color': '008282',
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': '[["A", "4"], ["a", "4"], ["E", "3"], ["e", "3"], ["I", "1"], ["i", "1"]]'
	},
	'aranea': {
		'acronym': 'ARANEA',
		'name': 'Aranea',
		'color': '005682',
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': '[["B", "8"], ["b", "8"]]'
	},
	'horuss': {
		'acronym': 'HORUSS',
		'name': 'Horuss',
		'color': '000056',
		'quirk_prefix': '8=D <',
		'case': 'normal',
		'replacements': '[["X", "%"], ["x", "%"], ["loo", "100"], ["ool", "001"]]'
	},
	'kurloz': {
		'acronym': 'KURLOZ',
		'name': 'Kurloz',
		'color': '2B0057',
		'quirk_prefix': '',
		'case': 'upper',
		'replacements': '[]'
	},
	'cronus': {
		'acronym': 'CRONUS',
		'name': 'Cronus',
		'color': '6A006A',
		'quirk_prefix': '',
		'case': 'lower',
		'replacements': '[["B", "8"], ["v", ""], ["w", "wv"], ["", "vw"]]'
	},
	'meenah': {
		'acronym': 'MEENAH',
		'name': 'Meenah',
		'color': '77003C',
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': '[["E", "-E"], ["H", ")("]]'
	},
	'nannasprite': {
		'acronym': 'NANNASPRITE',
		'name': 'Nannasprite',
		'color': '00D5F2',
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': '[]'
	},
	'jaspersprite': {
		'acronym': 'JASPERSPRITE',
		'name': 'Jaspersprite',
		'color': 'F141EF',
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': '[]'
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
		'case': 'lower',
		'replacements': '[]'
	},
	'jadesprite': {
		'acronym': 'JADESPRITE',
		'name': 'Jadesprite',
		'color': '1F9400',
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': '[]'
	},
	'tavrisprite': {
		'acronym': 'TAVRISPRITE',
		'name': 'Tavrisprite',
		'color': '0715CD',
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': '[]'
	},
	'fefetasprite': {
		'acronym': 'FEFETASPRITE',
		'name': 'Fefetasprite',
		'color': 'B536DA',
		'quirk_prefix': '3833 <',
		'case': 'normal',
		'replacements': '[["E", "-E"], ["ee", "33"], ["H", ")("], ["h", ")("]]'
	},
	'erisolsprite': {
		'acronym': 'ERISOLSPRITE',
		'name': 'Erisolsprite',
		'color': '4AC925',
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': '[["I", "II"], ["i", "ii"], ["S", "2"], ["s", "2"], ["V", "VV"], ["v", "vv"], ["W", "WW"], ["w", "ww"]]'
	},
	'the handmaid': {
		'acronym': '♈',
		'name': 'The Handmaid',
		'color': 'A10000',
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': '[]'
	},
	'the summoner': {
		'acronym': '♉',
		'name': 'The Summoner',
		'color': 'A15000',
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': '[]'
	},
	'the psiioniic':{
		'acronym': '♊',
		'name': 'The Ψiioniic',
		'color': 'A1A100',
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': '[]'
	},
	'the signless':{
		'acronym': '♋',
		'name': 'The Signless',
		'color': '626262',
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': '[]'
	},
	'the disciple': {
		'acronym': '♌',
		'name': 'The Disciple',
		'color': '416600',
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': '[]'
	},
	'the dolorosa':{
		'acronym': '♍',
		'name': 'The Dolorosa',
		'color': '008141',
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': '[]'
	},
	'redglare': {
		'acronym': '♎',
		'name': 'Neophyte Redglare',
		'color': '008282',
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': '[]'
	},
	'mindfang': {
		'acronym': '♏',
		'name': 'Marquise Spinneret Mindfang',
		'color': '005682',
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': '[]'
	},
	'darkleer': {
		'acronym': '♐',
		'name': 'E%ecutor Darkleer',
		'color': '000056',
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': '[]'
	},
	'grand highblood': {
		'acronym': '♑',
		'name': 'The Grand Highblood',
		'color': '2B0057',
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': '[]'
	},
	'dualscar': {
		'acronym': '♒',
		'name': 'Orphaner Dualscar',
		'color': '6A006A',
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': '[]'
	},
	'the condesce': {
		'acronym': '♓',
		'name': 'Her Imperious Condescension',
		'color': '77003C',
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': '[]'
	}
}

