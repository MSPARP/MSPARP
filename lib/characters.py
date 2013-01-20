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
		'replacements': '[]',
		'regexes': '[]'
	},
	'original character': {
		'acronym': '**',
		'name': 'Original Character',
		'color': 'FF00FF',
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': '[]',
		'regexes': '[]'
	},
	# XXX GOTTA REMOVE THIS AT SOME POINT.
	# needs conversion though otherwise we're gonna get a raft of 500s
	'ancestor': {
		'acronym': '??',
		'name': 'Ancestor',
		'color': '000000',
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': '[]',
		'regexes': '[]'
	},
	'guardian': {
		'acronym': '??',
		'name': 'Guardian',
		'color': '000000',
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': '[]',
		'regexes': '[]'
	},
	'midnight crew': {
		'acronym': '??',
		'name': 'Guardian',
		'color': '000000',
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': '[]',
		'regexes': '[]'
	},
	# XXX END STUFF THAT NEEDS REMOVING
	'trickster': {
		'acronym': '??',
		'name': 'Trickster',
		'color': 'FFAC9F',
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': '[]',
		'regexes': '[]'
	},
	'doc scratch': {
		'acronym': '',
		'name': 'Doc Scratch',
		'color': 'FFFFFF',
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': '[]',
		'regexes': '[]'
	},
	'calliope': {
		'acronym': 'UU',
		'name': 'uranianUmbra',
		'color': '929292',
		'quirk_prefix': '',
		'case': 'lower',
		'replacements': '[["u", "U"]]',
		'regexes': '[]'
	},
	'caliborn': {
		'acronym': 'uu',
		'name': 'undyingUmbrage',
		'color': '323232',
		'quirk_prefix': '',
		'case': 'upper',
		'replacements': '[["U", "u"]]',
		'regexes': '[]'
	},
	'other (canon)': {
		'acronym': '??',
		'name': 'Other (canon)',
		'color': 'ff83fb',
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': '[]',
		'regexes': '[]'
	},
	'john': {
		'acronym': 'EB',
		'name': 'ectoBiologist',
		'color': '0715CD',
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': '[]',
		'regexes': '[]'
	},
	'rose': {
		'acronym': 'TT',
		'name': 'tentacleTherapist',
		'color': 'B536DA',
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': '[]',
		'regexes': '[]'
	},
	'dave': {
		'acronym': 'TG',
		'name': 'turntechGodhead',
		'color': 'E00707',
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': '[]',
		'regexes': '[]'
	},
	'jade': {
		'acronym': 'GG',
		'name': 'gardenGnostic',
		'color': '4AC925',
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': '[]',
		'regexes': '[]'
	},
	'jane': {
		'acronym': 'GG',
		'name': 'gutsyGumshoe',
		'color': '00D5F2',
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': '[]',
		'regexes': '[]'
	},
	'roxy': {
		'acronym': 'TG',
		'name': 'tipsyGnostalgic',
		'color': 'FF6FF2',
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': '[]',
		'regexes': '[]'
	},
	'dirk': {
		'acronym': 'TT',
		'name': 'timaeusTestified',
		'color': 'F2A400',
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': '[]',
		'regexes': '[]'
	},
	'jake': {
		'acronym': 'GT',
		'name': 'golgothasTerror',
		'color': '1F9400',
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': '[]',
		'regexes': '[]'
	},
	'aradia': {
		'acronym': 'AA',
		'name': 'apocalypseArisen',
		'color': 'A10000',
		'quirk_prefix': '',
		'case': 'lower',
		'replacements': '[["o", "0"]]',
		'regexes': '[]'
	},
	'tavros': {
		'acronym': 'AT',
		'name': 'adiosToreador',
		'color': 'A15000',
		'quirk_prefix': '',
		'case': 'inverted',
		'replacements': '[[".", ","]]',
		'regexes': '[]'
	},
	'sollux':{
		'acronym': 'TA',
		'name': 'twinArmageddons',
		'color': 'A1A100',
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': '[["I", "II"], ["i", "ii"], ["S", "2"], ["s", "2"]]',
		'regexes': '[]'
	},
	'karkat':{
		'acronym': 'CG',
		'name': 'carcinoGeneticist',
		'color': '626262',
		'quirk_prefix': '',
		'case': 'upper',
		'replacements': '[]',
		'regexes': '[]'
	},
	'nepeta': {
		'acronym': 'AC',
		'name': 'arsenicCatnip',
		'color': '416600',
		'quirk_prefix': ':33 <',
		'case': 'lower',
		'replacements': '[["ee", "33"]]',
		'regexes': '[]'
	},
	'kanaya':{
		'acronym':'GA',
		'name':'grimAuxiliatrix',
		'color':'008141',
		'quirk_prefix': '',
		'case': 'title',
		'replacements': '[]',
		'regexes': '[]'
	},
	'terezi': {
		'acronym': 'GC',
		'name': 'gallowsCalibrator',
		'color': '008282',
		'quirk_prefix': '',
		'case': 'upper',
		'replacements': '[["A", "4"], ["E", "3"], ["I", "1"]]',
		'regexes': '[]'
	},
	'vriska': {
		'acronym': 'AG',
		'name': 'arachnidsGrip',
		'color': '005682',
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': '[["B", "8"], ["b", "8"]]',
		'regexes': '[]'
	},
	'equius': {
		'acronym': 'CT',
		'name': 'centaursTesticle',
		'color': '000056',
		'quirk_prefix': 'D -->',
		'case': 'normal',
		'replacements': '[["X", "%"], ["x", "%"], ["loo", "100"], ["ool", "001"]]',
		'regexes': '[]'
		
	},
	'gamzee': {
		'acronym': 'TC',
		'name': 'terminallyCapricious',
		'color': '2B0057',
		'quirk_prefix': '',
		'case': 'alternating',
		'replacements': '[]',
		'regexes': '[]'
	},
	'eridan': {
		'acronym': 'CA',
		'name': 'caligulasAquarium',
		'color': '6A006A',
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': '[["V", "VV"], ["v", "vv"], ["W", "WW"], ["w", "ww"]]',
		'regexes': '[]'
	},
	'feferi': {
		'acronym': 'CC',
		'name': 'cuttlefishCuller',
		'color': '77003C',
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': '[["E", "-E"], ["H", ")("], ["h", ")("]]',
		'regexes': '[]'
	},
	'damara': {
		'acronym': 'DAMARA',
		'name': 'Damara',
		'color': 'A10000',
		'quirk_prefix': '',
		'case': 'upper',
		'replacements': '[]',
		'regexes': '[]'
	},
	'rufioh': {
		'acronym': 'RUFIOH',
		'name': 'Rufioh',
		'color': 'A15000',
		'quirk_prefix': '',
		'case': 'lower',
		'replacements': '[["i", "1"]]',
		'regexes': '[]'
	},
	'mituna':{
		'acronym': 'MITUNA',
		'name': 'Mituna',
		'color': 'A1A100',
		'quirk_prefix': '',
		'case': 'upper',
		'replacements': '[["A", "4"], ["B", "8"], ["E", "3"], ["I", "1"], ["O", "0"], ["S", "5"], ["T", "7"]]',
		'regexes': '[]'
	},
	'kankri':{
		'acronym': 'KANKRI',
		'name': 'Kankri',
		'color': 'FF0000',
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': '[["B", "6"], ["b", "6"], ["O", "9"], ["o", "9"]]',
		'regexes': '[]'
	},
	'meulin': {
		'acronym': 'MEULIN',
		'name': 'Meulin',
		'color': '416600',
		'quirk_prefix': '(=｀ω´=) <',
		'case': 'upper',
		'replacements': '[["EE", "33"]]',
		'regexes': '[]'
	},
	'porrim':{
		'acronym':'PORRIM',
		'name':'Porrim',
		'color':'008141',
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': '[["o", "o+"]]',
		'regexes': '[]'
	},
	'latula': {
		'acronym': 'LATULA',
		'name': 'Latula',
		'color': '008282',
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': '[["A", "4"], ["a", "4"], ["E", "3"], ["e", "3"], ["I", "1"], ["i", "1"]]',
		'regexes': '[]'
	},
	'aranea': {
		'acronym': 'ARANEA',
		'name': 'Aranea',
		'color': '005682',
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': '[["B", "8"], ["b", "8"]]',
		'regexes': '[]'
	},
	'horuss': {
		'acronym': 'HORUSS',
		'name': 'Horuss',
		'color': '000056',
		'quirk_prefix': '8=D <',
		'case': 'normal',
		'replacements': '[["X", "%"], ["x", "%"], ["loo", "100"], ["ool", "001"]]',
		'regexes': '[]'
	},
	'kurloz': {
		'acronym': 'KURLOZ',
		'name': 'Kurloz',
		'color': '2B0057',
		'quirk_prefix': '',
		'case': 'upper',
		'replacements': '[]',
		'regexes': '[]'
	},
	'cronus': {
		'acronym': 'CRONUS',
		'name': 'Cronus',
		'color': '6A006A',
		'quirk_prefix': '',
		'case': 'lower',
		'replacements': '[["B", "8"], ["v", ""], ["w", "wv"], ["", "vw"]]',
		'regexes': '[]'
	},
	'meenah': {
		'acronym': 'MEENAH',
		'name': 'Meenah',
		'color': '77003C',
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': '[["E", "-E"], ["H", ")("]]',
		'regexes': '[]'
	},
	'dad': {
		'acronym': 'pipefan413',
		'name': 'Dad',
		'color': '4B4B4B',
		'quirk_prefix': '',
		'case': 'upper',
		'replacements': '[]',
		'regexes': '[]'
	},
	'nanna': {
		'acronym': 'NANNA',
		'name': 'Nanna',
		'color': '000000',
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': '[]',
		'regexes': '[]'
	},
	'mom': {
		'acronym': 'MOM',
		'name': 'Mom',
		'color': '000000',
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': '[]',
		'regexes': '[]'
	},
	'bro': {
		'acronym': 'BRO',
		'name': 'Bro',
		'color': '000000',
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': '[]',
		'regexes': '[]'
	},
	'grandpa': {
		'acronym': 'GRANDPA',
		'name': 'Grandpa',
		'color': '000000',
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': '[]',
		'regexes': '[]'
	},
	'poppop': {
		'acronym': 'POPPOP',
		'name': 'Poppop',
		'color': '000000',
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': '[]',
		'regexes': '[]'
	},
	'alpha mom': {
		'acronym': 'MOM',
		'name': 'Mom',
		'color': '000000',
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': '[]',
		'regexes': '[]'
	},
	'alpha bro': {
		'acronym': 'BRO',
		'name': 'Bro',
		'color': '000000',
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': '[]',
		'regexes': '[]'
	},
	'grandma': {
		'acronym': 'GRANDMA',
		'name': 'Grandma',
		'color': '000000',
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': '[]',
		'regexes': '[]'
	},
	'nannasprite': {
		'acronym': 'NANNASPRITE',
		'name': 'Nannasprite',
		'color': '00D5F2',
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': '[]',
		'regexes': '[]'
	},
	'jaspersprite': {
		'acronym': 'JASPERSPRITE',
		'name': 'Jaspersprite',
		'color': 'F141EF',
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': '[]',
		'regexes': '[]'
	},
	'calsprite': {
		'acronym': 'CALSPRITE',
		'name': 'Calsprite',
		'color': 'F2A400',
		'quirk_prefix': '',
		'case': 'upper',
		'replacements': '[["A", "<"], ["B", ">"], ["C", "?"], ["D", "<"], ["E", ">"], ["F", "?"], ["G", "<"], ["H", ">"], ["I", "?"], ["J", "<"], ["K", ">"], ["L", "?"], ["M", "<"], ["N", ">"], ["O", "?"], ["P", "<"], ["Q", ">"], ["R", "?"], ["S", "<"], ["T", ">"], ["U", "?"], ["V", "<"], ["W", ">"], ["X", "?"], ["Y", "<"], ["Z", ">"], ["<", "HAA "], [">", "HEE "], ["?", "HOO "]]',
		'regexes': '[]'
	},
	'davesprite': {
		'acronym': 'DAVESPRITE',
		'name': 'Davesprite',
		'color': 'F2A400',
		'quirk_prefix': '',
		'case': 'lower',
		'replacements': '[]',
		'regexes': '[]'
	},
	'jadesprite': {
		'acronym': 'JADESPRITE',
		'name': 'Jadesprite',
		'color': '1F9400',
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': '[]',
		'regexes': '[]'
	},
	'tavrisprite': {
		'acronym': 'TAVRISPRITE',
		'name': 'Tavrisprite',
		'color': '0715CD',
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': '[]',
		'regexes': '[]'
	},
	'fefetasprite': {
		'acronym': 'FEFETASPRITE',
		'name': 'Fefetasprite',
		'color': 'B536DA',
		'quirk_prefix': '3833 <',
		'case': 'normal',
		'replacements': '[["E", "-E"], ["ee", "33"], ["H", ")("], ["h", ")("]]',
		'regexes': '[]'
	},
	'erisolsprite': {
		'acronym': 'ERISOLSPRITE',
		'name': 'Erisolsprite',
		'color': '4AC925',
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': '[["I", "II"], ["i", "ii"], ["S", "2"], ["s", "2"], ["V", "VV"], ["v", "vv"], ["W", "WW"], ["w", "ww"]]',
		'regexes': '[]'
	},
	'the handmaid': {
		'acronym': '♈',
		'name': 'The Handmaid',
		'color': 'A10000',
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': '[]',
		'regexes': '[]'
	},
	'the summoner': {
		'acronym': '♉',
		'name': 'The Summoner',
		'color': 'A15000',
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': '[]',
		'regexes': '[]'
	},
	'the psiioniic':{
		'acronym': '♊',
		'name': 'The Ψiioniic',
		'color': 'A1A100',
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': '[]',
		'regexes': '[]'
	},
	'the signless':{
		'acronym': '♋',
		'name': 'The Signless',
		'color': '626262',
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': '[]',
		'regexes': '[]'
	},
	'the disciple': {
		'acronym': '♌',
		'name': 'The Disciple',
		'color': '416600',
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': '[]',
		'regexes': '[]'
	},
	'the dolorosa':{
		'acronym': '♍',
		'name': 'The Dolorosa',
		'color': '008141',
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': '[]',
		'regexes': '[]'
	},
	'redglare': {
		'acronym': '♎',
		'name': 'Neophyte Redglare',
		'color': '008282',
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': '[]',
		'regexes': '[]'
	},
	'mindfang': {
		'acronym': '♏',
		'name': 'Marquise Spinneret Mindfang',
		'color': '005682',
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': '[]',
		'regexes': '[]'
	},
	'darkleer': {
		'acronym': '♐',
		'name': 'E%ecutor Darkleer',
		'color': '000056',
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': '[]',
		'regexes': '[]'
	},
	'grand highblood': {
		'acronym': '♑',
		'name': 'The Grand Highblood',
		'color': '2B0057',
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': '[]',
		'regexes': '[]'
	},
	'dualscar': {
		'acronym': '♒',
		'name': 'Orphaner Dualscar',
		'color': '6A006A',
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': '[]',
		'regexes': '[]'
	},
	'the condesce': {
		'acronym': '♓',
		'name': 'Her Imperious Condescension',
		'color': '77003C',
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': '[]',
		'regexes': '[]'
	},
	'spades slick': {
		'acronym': '♠',
		'name': 'Spades Slick',
		'color': '000000',
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': '[]',
		'regexes': '[]'
	},
	'clubs deuce': {
		'acronym': '♣',
		'name': 'Clubs Deuce',
		'color': '000000',
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': '[]',
		'regexes': '[]'
	},
	'diamonds droog': {
		'acronym': '♦',
		'name': 'Diamonds Droog',
		'color': '000000',
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': '[]',
		'regexes': '[]'
	},
	'hearts boxcars': {
		'acronym': '♥',
		'name': 'Hearts Boxcars',
		'color': '000000',
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': '[]',
		'regexes': '[]'
	}
}

