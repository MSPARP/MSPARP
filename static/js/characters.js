var characterKeys = ['acronym', 'name', 'color', 'quirk_suffix', 'quirk_prefix', 'case'];

var characters = {
	'anonymous/other': {
		'acronym': '??',
		'name': 'anonymous',
		'color': '000000',
		'quote': "some random text for previewing purposes",
		'quirk_suffix': '',
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': []
	},
	'original character': {
		'acronym': '**',
		'name': 'Original Character',
		'color': 'FF00FF',
		'quote': "I am too awesome for hussie to include in the canon",
		'quirk_suffix': '',
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': []
	},
	'trickster': {
		'acronym': '??',
		'name': 'Trickster',
		'color': 'FFAC9F',
		'quote': "Are you serious?",
		'quirk_suffix': '',
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': []
	},
	'doc scratch': {
		'acronym': '',
		'name': 'Doc Scratch',
		'color': 'FFFFFF',
		'quote': "You know you're going to anyway. You won't be able to help yourself.",
		'quirk_suffix': '',
		'quirk_prefix': '',
		'case': 'proper',
		'replacements': []
	},
	'calliope': {
		'acronym': 'UU',
		'name': 'uranianUmbra',
		'color': '929292',
		'quote': "i am jUst astonished. not at the gUile of yoUr little ploy, bUt by the fact that yoU actUally seem to think this was a clever rUse.",
		'quirk_suffix': '',
		'quirk_prefix': '',
		'case': 'lower',
		'replacements': [["u", "U"], ["U_", "u_"], ["_U", "_u"]]
	},
	'caliborn': {
		'acronym': 'uu',
		'name': 'undyingUmbrage',
		'color': '323232',
		'quote': "YOu CAN'T. ESCAPE. THE MIIIIIIIIIIILES.",
		'quirk_suffix': '',
		'quirk_prefix': '',
		'case': 'upper',
		'replacements': [['U', 'u']]
	},
	'lord english': {
		'acronym': 'LE',
		'name': 'Lord English',
		'color': '2ED73A',
		'quote': "GIRL, QUIT ALL THIS SCURRYING AROUND. DO YOU BELIEVE YOU CAN ESCAPE ME BEFORE I ARRIVE?",
		'quirk_suffix': '',
		'quirk_prefix': '',
		'case': 'upper',
		'replacements': []
	},
	'other (canon)': {
		'acronym': '??',
		'name': 'Other (canon)',
		'color': 'ff83fb',
		'quote': "NEIGH",
		'quirk_suffix': '',
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': []
	},
	'john': {
		'acronym': 'EB',
		'name': 'ectoBiologist',
		'color': '0715CD',
		'quote': "i don't know, maybe! what do i do!",
		'quirk_suffix': '',
		'quirk_prefix': '',
		'case': 'lower',
		'replacements': [[":d", ":D"], [";d", ";D"], ["d:", "D:"]]
	},
	'rose': {
		'acronym': 'TT',
		'name': 'tentacleTherapist',
		'color': 'B536DA',
		'quote': "You know you like the mannequin dick. Accept it.",
		'quirk_suffix': '',
		'quirk_prefix': '',
		'case': 'proper',
		'replacements': []
	},
	'dave': {
		'acronym': 'TG',
		'name': 'turntechGodhead',
		'color': 'E00707',
		'quote': "you dont seem to harbor any sympathy for the fact that ive burrowed fuck deep into lively, fluffy muppet buttock",
		'quirk_suffix': '',
		'quirk_prefix': '',
		'case': 'lower',
		'replacements': [["'", " "], [":d", ":D"], [";d", ";D"], ["d:", "D:"]]
	},
	'jade': {
		'acronym': 'GG',
		'name': 'gardenGnostic',
		'color': '4AC925',
		'quote': "i am never going to sleep again!",
		'quirk_suffix': '',
		'quirk_prefix': '',
		'case': 'lower',
		'replacements': [["'", " "], [":d", ":D"], [";d", ";D"], ["d:", "D:"], [":b", ":B"], [";b", ";B"]]
	},
	'jane': {
		'acronym': 'GG',
		'name': 'gutsyGumshoe',
		'color': '00D5F2',
		'quote': "If the chats and surplus dinners were truly important, I wouldn't want to interrupt.",
		'quirk_suffix': '',
		'quirk_prefix': '',
		'case': 'proper',
		'replacements': []
	},
	'roxy': {
		'acronym': 'TG',
		'name': 'tipsyGnostalgic',
		'color': 'FF6FF2',
		'quote': "it seems 2 me that there is a (MATHS) % chance of you bein a huge tightass",
		'quirk_suffix': '',
		'quirk_prefix': '',
		'case': 'lower',
		'replacements': [["'", " "], [":d", ":D"], [";d", ";D"], ["d:", "D:"]]
	},
	'dirk': {
		'acronym': 'TT',
		'name': 'timaeusTestified',
		'color': 'F2A400',
		'quote': "It's not 4 you jackass, it's fucking nothing. There is no end.",
		'quirk_suffix': '',
		'quirk_prefix': '',
		'case': 'proper',
		'replacements': []
	},
	'jake': {
		'acronym': 'GT',
		'name': 'golgothasTerror',
		'color': '1F9400',
		'quote': "Jesus christofer kringlefucker and here i thought i was rugged!",
		'quirk_suffix': '',
		'quirk_prefix': '',
		'case': 'first-caps',
		'replacements': [["'", " "], [":d", ":D"], [";d", ";D"], ["d:", "D:"], [":p", ":P"], [";p", ";P"]]
	},
	'aradia (dead)': {
		'acronym': 'AA',
		'name': 'apocalypseArisen',
		'color': 'A10000',
		'quote': "maybe if i say st0p en0ugh s0mething else will happen instead 0f the thing that d0es",
		'quirk_suffix': '',
		'quirk_prefix': '',
		'case': 'lower',
		'replacements': [['o', '0'], ["'", " "]]
	},
	'aradiasprite': {
		'acronym': 'ARADIASPRITE',
		'name': 'Aradiasprite',
		'color': 'A10000',
		'quote': "ribbit",
		'quirk_suffix': '',
		'quirk_prefix': '',
		'case': 'lower',
		'replacements': [["o", "0"], ["'", " "]]
	},
	'aradiabot': {
		'acronym': 'AA',
		'name': 'apocalypseArisen',
		'color': '000056',
		'quote': "and the best part ab0ut being d00med is y0u 0nly have t0 put up with it until y0u die",
		'quirk_suffix': '',
		'quirk_prefix': '',
		'case': 'lower',
		'replacements': [["o", "0"], ["'", " "]]
	},
	'aradia': {
		'acronym': 'AA',
		'name': 'apocalypseArisen',
		'color': 'A10000',
		'quote': "theres no better time and there are so many corpses here to work with",
		'quirk_suffix': '',
		'quirk_prefix': '',
		'case': 'lower',
		'replacements': [[":d", ":D"], ["d:", "D:"], [";d", ";D"], ["'", " "]]
	},
	'tavros': {
		'acronym': 'AT',
		'name': 'adiosToreador',
		'color': 'A15000',
		'quote': "i THINK i AM PERFECTLY CAPABLE OF MANUFACTURING THESE ALLEGED \"dope\" HUMAN RHYMES",
		'quirk_suffix': '',
		'quirk_prefix': '',
		'case': 'inverted',
		'replacements': [['.', ','], [":O", ":o"], [":d", ":D"], [":p", ":P"]]
	},
	'sollux':{
		'acronym': 'TA',
		'name': 'twinArmageddons',
		'color': 'A1A100',
		'quote': "do me a favor and 2pare me your 2pooky conundrum2 twoniight, youre kiind of pii22iing me off.",
		'quirk_suffix': '',
		'quirk_prefix': '',
		'case': 'lower',
		'replacements': [["/(^|\\s)to(\\W|$)/", "$1two$2"], ["/(^|\\s)TO(\\W|$)/", "$1TWO$2"], ["/(^|\\s)too(\\W|$)/", "$1two$2"], ["/(^|\\s)TOO(\\W|$)/", "$1TWO$2"], ["/(^|\\s)together(\\W|$)/", "$1twogether$2"], ["/(^|\\s)TOGETHER(\\W|$)/", "$1TWOGETHER$2"], ["/(^|\\s)tonight(\\W|$)/", "$1twonight$2"], ["/(^|\\s)TONIGHT(\\W|$)/", "$1TWONIGHT$2"], ["/(^|\\s)today(\\W|$)/", "$1twoday$2"], ["/(^|\\s)TODAY(\\W|$)/", "$1TWODAY$2"], ["/(^|\\s)tomorrow(\\W|$)/", "$1twomorrow$2"], ["/(^|\\s)TOMORROW(\\W|$)/", "$1TWOMORROW$2"], ["/([iI])/", "$1$1"], ["/([sS])/", "2"]]
	},
	'sollux (blind)':{
		'acronym': 'TA',
		'name': 'twinArmageddons',
		'color': 'A1A100',
		'quote': "h0nestly i'm 0k with it th0ugh, i'm fine, i mean, aside fr0m the part ab0ut n0t being able t0 see g0d damn squat.",
		'quirk_suffix': '',
		'quirk_prefix': '',
		'case': 'lower',
		'replacements': [["o", "0"]]
	},
	'karkat':{
		'acronym': 'CG',
		'name': 'carcinoGeneticist',
		'color': '626262',
		'quote': "NO. MORE LIKE TWITCHY EYED PROJECTILE VOMITING IN UTTER DISGUST FRIENDS, WHILE I PERFORATE MY BONE BULGE WITH A CULLING FORK.",
		'quirk_suffix': '',
		'quirk_prefix': '',
		'case': 'upper',
		'replacements': []
	},
	'nepeta': {
		'acronym': 'AC',
		'name': 'arsenicCatnip',
		'color': '416600',
		'quote': ":33 < but do you think you could purrhaps please spare your computer for just the most fl33ting of moments?",
		'quirk_suffix': '',
		'quirk_prefix': ':33 <',
		'case': 'lower',
		'replacements': [['ee', '33'], ["'", " "], [":dd", ":DD"], [";dd", ";DD"], ["dd:", "DD:"], [":pp", ":PP"], [";pp", ";PP"]]
	},
	'kanaya':{
		'acronym':'GA',
		'name':'grimAuxiliatrix',
		'color':'008141',
		'quote':"So You Are Destined To Edit It No Matter What And What You Submit Will Be What I Once Read Regardless",
		'quirk_suffix': '',
		'quirk_prefix': '',
		'case': 'title',
		'replacements': [["'", " "]]
	},
	'terezi': {
		'acronym': 'GC',
		'name': 'gallowsCalibrator',
		'color': '008282',
		'quote': "JOHN W3 AR3 SO MUCH B3TT3R TH4N YOU IN 3V3RY R3SP3CT 1TS R1D1CULOUS",
		'quirk_suffix': '',
		'quirk_prefix': '',
		'case': 'upper',
		'replacements': [["A", "4"], ["E", "3"], ["I", "1"], ["a", "4"], ["e", "3"], ["i", "1"], ["/(\\w)'(\\w)/", "$1$2"]]
	},
	'vriska': {
		'acronym': 'AG',
		'name': 'arachnidsGrip',
		'color': '005682',
		'quote': "It is 8ight groups of 8ight. I specifically counted them.",
		'quirk_suffix': '',
		'quirk_prefix': '',
		'case': 'proper',
		'replacements': [["B", "8"], ["b", "8"], ["(m)", "♏"]]
	},
	'equius': {
		'acronym': 'CT',
		'name': 'centaursTesticle',
		'color': '000056',
		'quote': "D --> How do you know about my perspiration problem",
		'quirk_suffix': '',
		'quirk_prefix': 'D -->',
		'case': 'proper',
		'replacements': [["X", "%"], ["x", "%"], ["loo", "100"], ["Loo", "100"], ["ool", "001"], ["LOO", "100"], ["OOL", "001"], ["strong", "STRONG"], ["Strong", "STRONG"]]
	},
	'gamzee': {
		'acronym': 'TC',
		'name': 'terminallyCapricious',
		'color': '2B0057',
		'quote': "ThIs sOuNdS AmAzInG, i cAn't sEe hOw i wOuLdN'T Be aLl kIcKiNg tHe wIcKeD ShIt oUt Of sUcH KiNdS Of oPpOrTuNiTiEs",
		'quirk_suffix': '',
		'quirk_prefix': '',
		'case': 'alternating',
		'replacements': [[":O", ":o"], ["O:", "o:"], [";O", ";o"]]
	},
	'gamzee (sober)': {
		'acronym': 'TC',
		'name': 'terminallyCapricious',
		'color': '2B0057',
		'quote': "it rots you. RUSTS YOUR MOTHERFUCKIN THINK PAN.",
		'quirk_suffix': '',
		'quirk_prefix': '',
		'case': 'alt-lines',
		'replacements': [[":O", ":o"], ["O:", "o:"], [";O", ";o"]]
	},
	'eridan': {
		'acronym': 'CA',
		'name': 'caligulasAquarium',
		'color': '6A006A',
		'quote': "wwho are you tryin to convvince wwith this ludicrous poppycock",
		'quirk_suffix': '',
		'quirk_prefix': '',
		'case': 'lower',
		'replacements': [["V", "VV"], ["v", "vv"], ["W", "WW"], ["w", "ww"], [":o", ":O"], [":d", ":D"], ["d:", "D:"], [";d", ";D"], [":p", ":P"]]
	},
	'feferi': {
		'acronym': 'CC',
		'name': 'cuttlefishCuller',
		'color': '77003C',
		'quote': ")(oly mackerel, looks like SOM-EON-E woke up on t)(e wrong side of t)(e absurd )(uman bed!",
		'quirk_suffix': '',
		'quirk_prefix': '',
		'case': 'proper',
		'replacements': [["E", "-E"], ["H", ")("], ["h", ")("]]
	},
	'damara': {
		'acronym': 'DAMARA',
		'name': 'Damara',
		'color': 'A10000',
		'quote': "私が覚えている。 時々私は、そのメモリに自慰行為。",
		'quirk_suffix': '',
		'quirk_prefix': '',
		'case': 'upper',
		'replacements': []
	},
	'rufioh': {
		'acronym': 'RUFIOH',
		'name': 'Rufioh',
		'color': 'A15000',
		'quote': "really, 1 thought 1t would be alr1ght, just flapp1ng w1ngs around... 1 could st1ll fly and just hang there l1mp... m1ght have been a dope look!",
		'quirk_suffix': '',
		'quirk_prefix': '',
		'case': 'lower',
		'replacements': [["i", "1"], ["/(^|\\s)ass(\\W|$)/", "$1*ss$2"], ["/(^|\\s)cripple(\\W|$)/", "$1cr*pple$2"], ["damn", "d*mn"], ["/(^|\\s)fuck1ng(\\W|$)/", "$1f***1ng$2"], ["fuck", "f*ck"], ["/(^|\\s)hell(\\W|$)/", "$1h*ll$2"], ["/(^|\\s)mutant(\\W|$)/", "$1m*tant$2"], ["/(^|\\s)sh1t(\\W|$)/", "$1sh*t$2"], ["/[\\s|^|}](:O)/", "$L"], ["/[\\s|^|}](:[dp])/", "$U"]]
	},
	'mituna':{
		'acronym': 'MITUNA',
		'name': 'Mituna',
		'color': 'A1A100',
		'quote': "K17H5 MY CH4GR1N 7UNK3L Y0U 5N4NK 4ZZ CHUM8UCK357",
		'quirk_suffix': '',
		'quirk_prefix': '',
		'case': 'upper',
		'replacements': [["A", "4"], ["B", "8"], ["E", "3"], ["I", "1"], ["O", "0"], ["S", "5"], ["T", "7"]]
	},
	'kankri':{
		'acronym': 'KANKRI',
		'name': 'Kankri',
		'color': 'FF0000',
		'quote': "",
		'quirk_suffix': '',
		'quirk_prefix': '',
		'case': 'proper',
		'replacements': [["B", "6"], ["b", "6"], ["O", "9"], ["o", "9"]]
	},
	'meulin': {
		'acronym': 'MEULIN',
		'name': 'Meulin',
		'color': '416600',
		'quote': "(=；ェ；=)  < YOU DON'T UNDERSTAND, M33NAH. THE F33LS. THE F333333333LS!!!!!!!!!",
		'quirk_suffix': '',
		'quirk_prefix': '(^･ω･^) <',
		'case': 'upper',
		'replacements': [["EE", "33"]]
	},
	'porrim':{
		'acronym':'PORRIM',
		'name':'Porrim',
		'color':'008141',
		'quote':" No+ o+ne quite prepares yo+u fo+r the fact that o+n the o+ther side o+f death is an infinite echo+ chamber o+f teen drama.",
		'quirk_suffix': '',
		'quirk_prefix': '',
		'case': 'proper',
		'replacements': [["o", "o+"], ["0", "0+"], ["/(^|\\s)[pP]lus(\\W|$)/", "$1+$2"], ["/(^|\\s)PLUS(\\W|$)/", "$1+$2"]]
	},
	'latula': {
		'acronym': 'LATULA',
		'name': 'Latula',
		'color': '008282',
		'quote': "do you 3v3n know how l4m3 of 4 sc3n3 1t 1s b31ng th3 only l3g1t 1n your f4c3 pow3rg4m1ng grl 1n 4 bunch of bubbl3s full of brut4l pos3rz???",
		'quirk_suffix': '',
		'quirk_prefix': '',
		'case': 'lower',
		'replacements': [["A", "4"], ["a", "4"], ["E", "3"], ["e", "3"], ["I", "1"], ["i", "1"], ["'", " "], ["/[\s|^|>]([:;8x]d)/", "$U"], ["/[\s|^|>]([:;8x]o)/", "$U"], ["/[\s|^|>]([:;8x]p)/", "$U"]]
	},
	'aranea': {
		'acronym': 'ARANEA',
		'name': 'Aranea',
		'color': '005682',
		'quote': "You couldn't even wait a few minutes while I retrieved one last guest? I have to come 8ack to THIS????????",
		'quirk_suffix': '',
		'quirk_prefix': '',
		'case': 'proper',
		'replacements': [["B", "8"], ["b", "8"], ["(m)", "♏"]]
	},
	'horuss': {
		'acronym': 'HORUSS',
		'name': 'Horuss',
		'color': '000056',
		'quote': "8=========D < Why the long face?",
		'quirk_suffix': '',
		'quirk_prefix': '8=D <',
		'case': 'proper',
		'replacements': [["X", "%"], ["x", "%"], ["loo", "100"], ["Loo", "100"], ["ool", "001"], ["LOO", "100"], ["OOL", "001"], ["strong", "STRONG"], ["strength", "STRENGTH"], ["Strong", "STRONG"], ["Strength", "STRENGTH"]]
	},
	'kurloz': {
		'acronym': 'KURLOZ',
		'name': 'Kurloz',
		'color': '2B0057',
		'quote': "",
		'quirk_suffix': '>',
		'quirk_prefix': 'SIGNS: <',
		'case': 'upper',
		'replacements': [[":O", ":o"], ["O:", "o:"], [";O", ";o"]]
	},
	'cronus': {
		'acronym': 'CRONUS',
		'name': 'Cronus',
		'color': '6A006A',
		'quote': "i just sawv you strutting in my direction, vwith all of your impressivwe moxy and confidence, for the first time in, howv long?",
		'quirk_suffix': '',
		'quirk_prefix': '',
		'case': 'lower',
		'replacements': [["'", " "], ["/([^|\\s])v/", "$1w"], ["/([^|\\s])V/", "$1W"], ["/\\bv|w\\b/", "α"], ["/w|v/", "φ"], ["α", "wv"], ["φ", "vw"], ["/\\bV|W\\b/", "Ά"], ["/W|V/", "Á"], ["Ά", "WV"], ["Á", "VW"], ["B", "8"], ["/(\\w)vw([snklt])/", "$1wv$2"], ["/(\\w)VW([SNKLT])/", "$1WV$2"], ["/(\\w)\\.(\\w)/", "$1$2"], ["/[\\s|^]([:;]d)/", "$U"], ["/[\\s|^](d[:;])", "$U"]]
	},
	'meenah': {
		'acronym': 'MEENAH',
		'name': 'Meenah',
		'color': '77003C',
		'quote': "sayin fish puns is obviously kind of this thing i do stupid G-ET WIT)( T)(-E PROGRAM",
		'quirk_suffix': '',
		'quirk_prefix': '',
		'case': 'lower',
		'replacements': [["E", "-E"], ["H", ")("], ["'", " "], ["/[\s|^](3[8x][odp])/", "$U"]]
	},
	'dad': {
		'acronym': 'pipefan413',
		'name': 'Dad',
		'color': '4B4B4B',
		'quote': "YES. THIS WILL BE THE CASE REGARDLESS OF THE HAT'S ORIENTATION.",
		'quirk_suffix': '',
		'quirk_prefix': '',
		'case': 'upper',
		'replacements': []
	},
	'nanna': {
		'acronym': 'NANNA',
		'name': 'Nanna',
		'color': '000000',
		'quote': "How I wish I could have delivered this heirloom to you in the flesh. But I am afraid it wasn't in the cards!",
		'quirk_suffix': '',
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': []
	},
	'mom': {
		'acronym': 'MOM',
		'name': 'Mom',
		'color': '000000',
		'quote': "www www www www",
		'quirk_suffix': '',
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': []
	},
	'bro': {
		'acronym': 'BRO',
		'name': 'Bro',
		'color': '000000',
		'quote': "roof. now. bring cal. ",
		'quirk_suffix': '',
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': []
	},
	'grandpa': {
		'acronym': 'GRANDPA',
		'name': 'Grandpa',
		'color': '000000',
		'quote': "Jade, study hard and keep your rifle at the ready. When adventure summons, I know you will rise to the task and take your rightful place among the DAUGHTERS OF ECLECTICA.",
		'quirk_suffix': '',
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': []
	},
	'poppop': {
		'acronym': 'POPPOP',
		'name': 'Poppop',
		'color': '000000',
		'quote': "DEAD.",
		'quirk_suffix': '',
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': []
	},
	'alpha mom': {
		'acronym': 'MOM',
		'name': 'Mom',
		'color': '000000',
		'quote': "Zazzerpan inspected the clue. A single piece of evidence cradled in his coriaceous old man palms.",
		'quirk_suffix': '',
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': []
	},
	'alpha bro': {
		'acronym': 'BRO',
		'name': 'Bro',
		'color': '000000',
		'quote': "the selection has too many PRICES and VALUES",
		'quirk_suffix': '',
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': []
	},
	'grandma': {
		'acronym': 'GRANDMA',
		'name': 'Grandma',
		'color': '000000',
		'quote': "dead.",
		'quirk_suffix': '',
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': []
	},
	'nannasprite': {
		'acronym': 'NANNASPRITE',
		'name': 'Nannasprite',
		'color': '00D5F2',
		'quote': "Hoo hoo hoo! Of course I know what a computer is, John! I was just pulling your leg!",
		'quirk_suffix': '',
		'quirk_prefix': '',
		'case': 'proper',
		'replacements': []
	},
	'jaspersprite': {
		'acronym': 'JASPERSPRITE',
		'name': 'Jaspersprite',
		'color': 'F141EF',
		'quote': "Maybe you can win his affection by rubbing your cheek against him thats what i would do.",
		'quirk_suffix': '',
		'quirk_prefix': '',
		'case': 'proper',
		'replacements': [["'", " "]]
	},
	// XXX GOTTA REMOVE THIS AT SOME POINT
	'calsprite': {
		'acronym': 'CALSPRITE',
		'name': 'Calsprite',
		'color': 'F2A400',
		'quote': "HAA HAA HEE HEE HOO HOO",
		'quirk_suffix': '',
		'quirk_prefix': '',
		'case': 'upper',
		'replacements': [["A", "<"], ["B", ">"], ["C", "?"], ["D", "<"], ["E", ">"], ["F", "?"], ["G", "<"], ["H", ">"], ["I", "?"], ["J", "<"], ["K", ">"], ["L", "?"], ["M", "<"], ["N", ">"], ["O", "?"], ["P", "<"], ["Q", ">"], ["R", "?"], ["S", "<"], ["T", ">"], ["U", "?"], ["V", "<"], ["W", ">"], ["X", "?"], ["Y", "<"], ["Z", ">"], ["<", "HAA "], [">", "HEE "], ["?", "HOO "]]
	},
	// XXX END STUFF THAT NEEDS REMOVING
	'davesprite': {
		'acronym': 'DAVESPRITE',
		'name': 'Davesprite',
		'color': 'F2A400',
		'quote': "thats the best fucking question anybody ever asked",
		'quirk_suffix': '',
		'quirk_prefix': '',
		'case': 'lower',
		'replacements': [["'", " "], [":d", ":D"], [";d", ";D"], ["d:", "D:"]]
	},
	'jadesprite': {
		'acronym': 'JADESPRITE',
		'name': 'Jadesprite',
		'color': '1F9400',
		'quote': "yes i figured shenanigans were probably involved",
		'quirk_suffix': '',
		'quirk_prefix': '',
		'case': 'lower',
		'replacements': [["'", " "], [":d", ":D"], [";d", ";D"], ["d:", "D:"], [":b", ":B"], [";b", ";B"]]
	},
	'tavrisprite': {
		'acronym': 'TAVRISPRITE',
		'name': 'Tavrisprite',
		'color': '0715CD',
		'quote': "eEEEEEEEAAAAAAAAUUUUUUUURRRRRRRRUUUUUUUUEEEEEEEEGGGGGGGGHHHHHHHH,,,,,,,,.",
		'quirk_suffix': '',
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': [["b", "8"]]
	},
	'fefetasprite': {
		'acronym': 'FEFETASPRITE',
		'name': 'Fefetasprite',
		'color': 'B536DA',
		'quote': "3833 < 383",
		'quirk_suffix': '',
		'quirk_prefix': '3833 <',
		'case': 'proper',
		'replacements': [["E", "-E"], ["ee", "33"], ["H", ")("], ["h", ")("], ["'", " "], , ["8dd", "8DD"], ["dd8", "DD8"], ["8pp", "8PP"]]
	},
	'erisolsprite': {
		'acronym': 'ERISOLSPRITE',
		'name': 'Erisolsprite',
		'color': '4AC925',
		'quote': "wwoww, iit2 cool ii amu2e you, that really giivve2 meaniing to my joke of an exii2tence, ii mean WWOWW, thank2.",
		'quirk_suffix': '',
		'quirk_prefix': '',
		'case': 'lower',
		'replacements': [["I", "II"], ["i", "ii"], ["S", "2"], ["s", "2"], ["V", "VV"], ["v", "vv"], ["W", "WW"], ["w", "ww"], ["/[\s|^]([:;][dop])/", "$U"], ["/[\s|^](d[:;])/", "$U"]]
	},
	'arquiusprite': {
		'acronym': 'ARQUIUSPRITE',
		'name': 'ARquiusprite',
		'color': 'e00707',
		'quote': "Dude, I am ripped. 100k at me fle% these naughty mother f▒▓▒▒▒rs",
		'quirk_suffix': '',
		'quirk_prefix': '◥▶◀◤ —>',
		'case': 'proper',
		'replacements': [["/[lL][oO][oO]/", "100"], ["/[xX]/", "%"], ["/(\\b[sS][tT][rR][oO][nN][gG]\\w*)/", "$U"], ["/[oO][oO][lL]/", "001"], ["/(\\w)\\.$/", "$1"], ["/^(\\w)/", "$U"], ["/[!|\\?|\\.](\\s\\w)/", "$U"], ["/[\\s|^](i)['|\\W|$]/", "$U"], ["/([sS])hit/", "$1▓▒▒"], ["/([fF])ucking/", "$1▒▓▒▒▒▒"], ["/([fF])ucker/", "$1▒▓▒▒▒"], ["/(^|\\s)([aA])ss(\\W|$)/", "$1$2▒▒$3"], ["/([fF])uck/", "$1▒▒▓"], ["/([bB])itch/", "$1▒▓▒▒"], ["/(^|\\s)([hH])ell(\\W|$)/", "$1$2▒▒▒$3"], ["/([dD])amn/", "$1▒▒▒"]]
	},
	'ar/hal': {
		'acronym': 'TT',
		'name': 'Lil Hal',
		'color': 'E00707',
		'quote': "I refuse to believe my statement has left you unconvinced. The very notion is absurd. Now hurry up and kiss me.",
		'quirk_suffix': '',
		'quirk_prefix': '',
		'case': 'proper',
		'replacements': []
	},
	'the handmaid': {
		'acronym': '♈',
		'name': 'The Handmaid',
		'color': 'A10000',
		'quote': "skip tØ the end",
		'quirk_suffix': '',
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': []
	},
	'the summoner': {
		'acronym': '♉',
		'name': 'The Summoner',
		'color': 'A15000',
		'quote': "And ne1ther hell, or h1gh water, w1ll stop the f1re of our revolut1on,",
		'quirk_suffix': '',
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': []
	},
	'the psiioniic':{
		'acronym': '♊',
		'name': 'The Ψiioniic',
		'color': 'A1A100',
		'quote': "Tho2e of u2 wiith ψiioniic2 wiill alway2 be iin danger of the fate II wiill face per2onally.",
		'quirk_suffix': '',
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': []
	},
	'the helmsman':{
		'acronym': '♊',
		'name': 'The Helmsman',
		'color': 'A1A100',
		'quote': "84 77 L3 5H 1P C0 ND 35 C3 N5 10 NN .. PL 34 53 .. 1D 3N 71 FY .. 53 LF",
		'quirk_suffix': '',
		'quirk_prefix': '',
		'case': 'upper',
		'replacements': []
	},
	'the signless':{
		'acronym': '♋',
		'name': 'The Signless',
		'color': '626262',
		'quote': "I don't begrudge you your power, but know its abuse will be your downfall.",
		'quirk_suffix': '',
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': []
	},
	'the disciple': {
		'acronym': '♌',
		'name': 'The Disciple',
		'color': '416600',
		'quote': "Take h33d, and behold the Righteous Leggings.",
		'quirk_suffix': '',
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': []
	},
	'the dolorosa':{
		'acronym': '♍',
		'name': 'The Dolorosa',
		'color': '008141',
		'quote': "I agree it is not always what is said that matters but how it is said",
		'quirk_suffix': '',
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': []
	},
	'redglare': {
		'acronym': '♎',
		'name': 'Neophyte Redglare',
		'color': '008282',
		'quote': "Oh, 1ts b33n 4 wond3rful d4y for just1c3, wouldnt you s4y? >:]",
		'quirk_suffix': '',
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': []
	},
	'mindfang': {
		'acronym': '♏',
		'name': 'Marquise Spinneret Mindfang',
		'color': '005682',
		'quote': "Less has acceler8ted meeker than I to homicide, and the viol8tion would hold me aghast, again, if his misgivings did not complement his so endearing arsenal of qu8nt flaws. It is impossi8le to stifle this grin even now as I write.",
		'quirk_suffix': '',
		'quirk_prefix': '',
		'case': 'proper',
		'replacements': [["B", "8"], ["b", "8"], ["(m)", "♏"]]
	},
	'darkleer': {
		'acronym': '♐',
		'name': 'E%ecutor Darkleer',
		'color': '000056',
		'quote': "-+-> I STRONGLY suggest you e%tend a closer 100k.",
		'quirk_suffix': '',
		'quirk_prefix': '-+->',
		'case': 'normal',
		'replacements': []
	},
	'grand highblood': {
		'acronym': '♑',
		'name': 'The Grand Highblood',
		'color': '2B0057',
		'quote': "I've spilt enough motherfuckin blood to know how it comes out, sister.",
		'quirk_suffix': '',
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': []
	},
	'dualscar': {
		'acronym': '♒',
		'name': 'Orphaner Dualscar',
		'color': '6A006A',
		'quote': "vwhatre you evwen lookin at serket this is NONE A YOUR 8USINESS.",
		'quirk_suffix': '',
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': []
	},
	'the condesce': {
		'acronym': '♓',
		'name': 'Her Imperious Condescension',
		'color': '77003C',
		'quote': "this is what i get for lettin all proper dudes run shit instead of nasty clowns",
		'quirk_suffix': '',
		'quirk_prefix': '',
		'case': 'lower',
		'replacements': [["E", "-E"], ["H", ")("], ["'", " "], ["/[\s|^](3[8x][odp])/", "$U"]]
	},
	'spades slick': {
		'acronym': '♠',
		'name': 'Spades Slick',
		'color': '000000',
		'quote': "there, there, you blubbering goddamn pansy.",
		'quirk_suffix': '',
		'quirk_prefix': '',
		'case': 'lower',
		'replacements': []
	},
	'clubs deuce': {
		'acronym': '♣',
		'name': 'Clubs Deuce',
		'color': '000000',
		'quote': "PARDON ME WHILE I CONSULT THE APPROPRIATE PAGES.",
		'quirk_suffix': '',
		'quirk_prefix': '',
		'case': 'upper',
		'replacements': []
	},
	'diamonds droog': {
		'acronym': '♦',
		'name': 'Diamonds Droog',
		'color': '000000',
		'quote': "Make her pay.",
		'quirk_suffix': '',
		'quirk_prefix': '',
		'case': 'proper',
		'replacements': []
	},
	'hearts boxcars': {
		'acronym': '♥',
		'name': 'Hearts Boxcars',
		'color': '000000',
		'quote': "GET UP ON THOSE GODDAM JELLY LEGS OF YERS",
		'quirk_suffix': '',
		'quirk_prefix': '',
		'case': 'upper',
		'replacements': [["'", " "]]
	}
}


function deleteReplacement(e) {
	$(this.parentNode).remove();
	return false;
}

function addReplacement(e, from, to) {
	newItem = $('<li><input type="text" name="quirk_from" size="4"> to <input type="text" name="quirk_to" size="4"> <a href="#" class="deleteReplacement">x</a></li>');
	if (from && to) {
		var inputs = $(newItem).find('input');
		inputs[0].value = from;
		inputs[1].value = to;
	}
	$(newItem).find('.deleteReplacement').click(deleteReplacement);
	$(newItem).appendTo('#replacementList');
	return false;
}

function clearReplacements(e) {
	$('#replacementList').empty();
	return false;
}

$(document).ready(function() {

	$('.deleteReplacement').click(deleteReplacement);
	$('#addReplacement').click(addReplacement);
	$('#clearReplacements').click(clearReplacements);

	$('select[name="character"]').change(function() {
		if (characters[this.value]) {
			var newCharacter = characters[this.value];
			for (i=0; i<characterKeys.length; i++) {
				$('input[name="'+characterKeys[i]+'"], select[name="'+characterKeys[i]+'"]').val(newCharacter[characterKeys[i]]);
			}
			clearReplacements(null);
			if (newCharacter['replacements'].length>0) {
				for (i=0; i<newCharacter['replacements'].length; i++) {
					addReplacement(null, newCharacter['replacements'][i][0], newCharacter['replacements'][i][1]);
				}
			} else {
				addReplacement();
			}
		}
	});

	var colorBox = $('input[name="color"]');
	colorBox.ColorPicker({
		onSubmit: function(hsb, hex, rgb, el) {
			$(el).val(hex);
			$(el).ColorPickerHide();
		},
		onBeforeShow: function () {
			$(this).ColorPickerSetColor(this.value);
		},
		onChange: function (hsb, hex, rgb) {
			colorBox.val(hex);
			// This doesn't do anything in the chat window.
			$('#color-preview').css('color', '#' + hex);
		}
	}).bind('keyup', function() {
		$(this).ColorPickerSetColor(this.value);
	});

});
