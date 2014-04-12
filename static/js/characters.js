var characterKeys = ['acronym', 'name', 'color', 'quirk_prefix', 'case'];

var characters = {
	'anonymous/other': {
		'acronym': '??',
		'name': 'anonymous',
		'color': '000000',
		'quote': "some random text for previewing purposes",
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': []
	},
	'original character': {
		'acronym': '**',
		'name': 'Original Character',
		'color': 'FF00FF',
		'quote': "I am too awesome for hussie to include in the canon",
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': []
	},
	// XXX GOTTA REMOVE THIS AT SOME POINT
	'ancestor': {
		'acronym': '??',
		'name': 'Ancestor',
		'color': '000000',
		'quote': "I saw the look he gave. He's so secure in knowing I can't feel what's in his mind he forgets the tr8torous ways of his own face.",
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': []
	},
	'guardian': {
		'acronym': '??',
		'name': 'Guardian',
		'color': '000000',
		'quote': "NOW BE A GOOD GIRL, PUT THE FRIDGE DOWN, AND STAY INSIDE.",
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': []
	},
	'midnight crew': {
		'acronym': '??',
		'name': 'Guardian',
		'color': '000000',
		'quote': "Farmin' all these goddamn horses. Fuckin' pain in the ass.",
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': []
	},
	// XXX END STUFF THAT NEEDS REMOVING
	'trickster': {
		'acronym': '??',
		'name': 'Trickster',
		'color': 'FFAC9F',
		'quote': "Are you serious?",
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': []
	},
	'doc scratch': {
		'acronym': '',
		'name': 'Doc Scratch',
		'color': 'FFFFFF',
		'quote': "You know you're going to anyway. You won't be able to help yourself.",
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': []
	},
	'calliope': {
		'acronym': 'UU',
		'name': 'uranianUmbra',
		'color': '929292',
		'quote': "i am jUst astonished. not at the gUile of yoUr little ploy, bUt by the fact that yoU actUally seem to think this was a clever rUse.",
		'quirk_prefix': '',
		'case': 'lower',
		'replacements': [['u', 'U']]
	},
	'caliborn': {
		'acronym': 'uu',
		'name': 'undyingUmbrage',
		'color': '323232',
		'quote': "YOu CAN'T. ESCAPE. THE MIIIIIIIIIIILES.",
		'quirk_prefix': '',
		'case': 'upper',
		'replacements': [['U', 'u']]
	},
	'other (canon)': {
		'acronym': '??',
		'name': 'Other (canon)',
		'color': 'ff83fb',
		'quote': "NEIGH",
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': []
	},
	'john': {
		'acronym': 'EB',
		'name': 'ectoBiologist',
		'color': '0715CD',
		'quote': "i don't know, maybe! what do i do!",
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': []
	},
	'rose': {
		'acronym': 'TT',
		'name': 'tentacleTherapist',
		'color': 'B536DA',
		'quote': "You know you like the mannequin dick. Accept it.",
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': []
	},
	'dave': {
		'acronym': 'TG',
		'name': 'turntechGodhead',
		'color': 'E00707',
		'quote': "you dont seem to harbor any sympathy for the fact that ive burrowed fuck deep into lively, fluffy muppet buttock",
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': []
	},
	'jade': {
		'acronym': 'GG',
		'name': 'gardenGnostic',
		'color': '4AC925',
		'quote': "i am never going to sleep again!",
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': []
	},
	'jane': {
		'acronym': 'GG',
		'name': 'gutsyGumshoe',
		'color': '00D5F2',
		'quote': "If the chats and surplus dinners were truly important, I wouldn't want to interrupt.",
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': []
	},
	'roxy': {
		'acronym': 'TG',
		'name': 'tipsyGnostalgic',
		'color': 'FF6FF2',
		'quote': "it seems 2 me that there is a (MATHS) % chance of you bein a huge tightass",
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': []
	},
	'dirk': {
		'acronym': 'TT',
		'name': 'timaeusTestified',
		'color': 'F2A400',
		'quote': "It's not 4 you jackass, it's fucking nothing. There is no end.",
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': []
	},
	'jake': {
		'acronym': 'GT',
		'name': 'golgothasTerror',
		'color': '1F9400',
		'quote': "Jesus christofer kringlefucker and here i thought i was rugged!",
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': []
	},
	'aradia': {
		'acronym': 'AA',
		'name': 'apocalypseArisen',
		'color': 'A10000',
		'quote': "maybe if i say st0p en0ugh s0mething else will happen instead 0f the thing that d0es",
		'quirk_prefix': '',
		'case': 'lower',
		'replacements': [['o', '0']]
	},
	'tavros': {
		'acronym': 'AT',
		'name': 'adiosToreador',
		'color': 'A15000',
		'quote': "i THINK i AM PERFECTLY CAPABLE OF MANUFACTURING THESE ALLEGED \"dope\" HUMAN RHYMES",
		'quirk_prefix': '',
		'case': 'inverted',
		'replacements': [['.', ',']]
	},
	'sollux':{
		'acronym': 'TA',
		'name': 'twinArmageddons',
		'color': 'A1A100',
		'quote': "do me a favor and 2pare me your 2pooky conundrum2 twoniight, youre kiind of pii22iing me off.",
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': [["I", "II"], ["i", "ii"], ["S", "2"], ["s", "2"]]
	},
	'karkat':{
		'acronym': 'CG',
		'name': 'carcinoGeneticist',
		'color': '626262',
		'quote': "NO. MORE LIKE TWITCHY EYED PROJECTILE VOMITING IN UTTER DISGUST FRIENDS, WHILE I PERFORATE MY BONE BULGE WITH A CULLING FORK.",
		'quirk_prefix': '',
		'case': 'upper',
		'replacements': []
	},
	'nepeta': {
		'acronym': 'AC',
		'name': 'arsenicCatnip',
		'color': '416600',
		'quote': ":33 < but do you think you could purrhaps please spare your computer for just the most fl33ting of moments?",
		'quirk_prefix': ':33 <',
		'case': 'lower',
		'replacements': [['ee', '33']]
	},
	'kanaya':{
		'acronym':'GA',
		'name':'grimAuxiliatrix',
		'color':'008141',
		'quote':"So You Are Destined To Edit It No Matter What And What You Submit Will Be What I Once Read Regardless",
		'quirk_prefix': '',
		'case': 'title',
		'replacements': []
	},
	'terezi': {
		'acronym': 'GC',
		'name': 'gallowsCalibrator',
		'color': '008282',
		'quote': "JOHN W3 AR3 SO MUCH B3TT3R TH4N YOU IN 3V3RY R3SP3CT 1TS R1D1CULOUS",
		'quirk_prefix': '',
		'case': 'upper',
		'replacements': [["A", "4"], ["E", "3"], ["I", "1"]]
	},
	'vriska': {
		'acronym': 'AG',
		'name': 'arachnidsGrip',
		'color': '005682',
		'quote': "It is 8ight groups of 8ight. I specifically counted them.",
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': [["B", "8"], ["b", "8"]]
	},
	'equius': {
		'acronym': 'CT',
		'name': 'centaursTesticle',
		'color': '000056',
		'quote': "D --> How do you know about my perspiration problem",
		'quirk_prefix': 'D -->',
		'case': 'normal',
		'replacements': [["X", "%"], ["x", "%"], ["loo", "100"], ["ool", "001"]]
	},
	'gamzee': {
		'acronym': 'TC',
		'name': 'terminallyCapricious',
		'color': '2B0057',
		'quote': "ThIs sOuNdS AmAzInG, i cAn't sEe hOw i wOuLdN'T Be aLl kIcKiNg tHe wIcKeD ShIt oUt Of sUcH KiNdS Of oPpOrTuNiTiEs",
		'quirk_prefix': '',
		'case': 'alternating',
		'replacements': []
	},
	'eridan': {
		'acronym': 'CA',
		'name': 'caligulasAquarium',
		'color': '6A006A',
		'quote': "wwho are you tryin to convvince wwith this ludicrous poppycock",
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': [["V", "VV"], ["v", "vv"], ["W", "WW"], ["w", "ww"]]
	},
	'feferi': {
		'acronym': 'CC',
		'name': 'cuttlefishCuller',
		'color': '77003C',
		'quote': ")(oly mackerel, looks like SOM-EON-E woke up on t)(e wrong side of t)(e absurd )(uman bed!",
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': [["E", "-E"], ["H", ")("], ["h", ")("]]
	},
	'damara': {
		'acronym': 'DAMARA',
		'name': 'Damara',
		'color': 'A10000',
		'quote': "私が覚えている。 時々私は、そのメモリに自慰行為。",
		'quirk_prefix': '',
		'case': 'upper',
		'replacements': []
	},
	'rufioh': {
		'acronym': 'RUFIOH',
		'name': 'Rufioh',
		'color': 'A15000',
		'quote': "really, 1 thought 1t would be alr1ght, just flapp1ng w1ngs around... 1 could st1ll fly and just hang there l1mp... m1ght have been a dope look!",
		'quirk_prefix': '',
		'case': 'lower',
		'replacements': [["i", "1"]]
	},
	'mituna':{
		'acronym': 'MITUNA',
		'name': 'Mituna',
		'color': 'A1A100',
		'quote': "K17H5 MY CH4GR1N 7UNK3L Y0U 5N4NK 4ZZ CHUM8UCK357",
		'quirk_prefix': '',
		'case': 'upper',
		'replacements': [["A", "4"], ["B", "8"], ["E", "3"], ["I", "1"], ["O", "0"], ["S", "5"], ["T", "7"]]
	},
	'kankri':{
		'acronym': 'KANKRI',
		'name': 'Kankri',
		'color': 'FF0000',
		'quote': "",
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': [["B", "6"], ["b", "6"], ["O", "9"], ["o", "9"]]
	},
	'meulin': {
		'acronym': 'MEULIN',
		'name': 'Meulin',
		'color': '416600',
		'quote': "(=；ェ；=)  < YOU DON'T UNDERSTAND, M33NAH. THE F33LS. THE F333333333LS!!!!!!!!!",
		'quirk_prefix': '(=｀ω´=) <',
		'case': 'upper',
		'replacements': [["EE", "33"]]
	},
	'porrim':{
		'acronym':'PORRIM',
		'name':'Porrim',
		'color':'008141',
		'quote':" No+ o+ne quite prepares yo+u fo+r the fact that o+n the o+ther side o+f death is an infinite echo+ chamber o+f teen drama.",
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': [["o", "o+"]]
	},
	'latula': {
		'acronym': 'LATULA',
		'name': 'Latula',
		'color': '008282',
		'quote': "do you 3v3n know how l4m3 of 4 sc3n3 1t 1s b31ng th3 only l3g1t 1n your f4c3 pow3rg4m1ng grl 1n 4 bunch of bubbl3s full of brut4l pos3rz???",
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': [["A", "4"], ["a", "4"], ["E", "3"], ["e", "3"], ["I", "1"], ["i", "1"]]
	},
	'aranea': {
		'acronym': 'ARANEA',
		'name': 'Aranea',
		'color': '005682',
		'quote': "You couldn't even wait a few minutes while I retrieved one last guest? I have to come 8ack to THIS????????",
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': [["B", "8"], ["b", "8"]]
	},
	'horuss': {
		'acronym': 'HORUSS',
		'name': 'Horuss',
		'color': '000056',
		'quote': "8=========D < Why the long face?",
		'quirk_prefix': '8=D <',
		'case': 'normal',
		'replacements': [["X", "%"], ["x", "%"], ["loo", "100"], ["ool", "001"]]
	},
	'kurloz': {
		'acronym': 'KURLOZ',
		'name': 'Kurloz',
		'color': '2B0057',
		'quote': "",
		'quirk_prefix': '',
		'case': 'upper',
		'replacements': []
	},
	'cronus': {
		'acronym': 'CRONUS',
		'name': 'Cronus',
		'color': '6A006A',
		'quote': "i just sawv you strutting in my direction, vwith all of your impressivwe moxy and confidence, for the first time in, howv long?",
		'quirk_prefix': '',
		'case': 'lower',
		'replacements': [["B", "8"], ["v", ""], ["w", "wv"], ["", "vw"]]
	},
	'meenah': {
		'acronym': 'MEENAH',
		'name': 'Meenah',
		'color': '77003C',
		'quote': "sayin fish puns is obviously kind of this thing i do stupid G-ET WIT)( T)(-E PROGRAM",
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': [["E", "-E"], ["H", ")("]]
	},
	'dad': {
		'acronym': 'pipefan413',
		'name': 'Dad',
		'color': '4B4B4B',
		'quote': "YES. THIS WILL BE THE CASE REGARDLESS OF THE HAT'S ORIENTATION.",
		'quirk_prefix': '',
		'case': 'upper',
		'replacements': []
	},
	'nanna': {
		'acronym': 'NANNA',
		'name': 'Nanna',
		'color': '000000',
		'quote': "some random text for previewing purposes",
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': []
	},
	'mom': {
		'acronym': 'MOM',
		'name': 'Mom',
		'color': '000000',
		'quote': "some random text for previewing purposes",
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': []
	},
	'bro': {
		'acronym': 'BRO',
		'name': 'Bro',
		'color': '000000',
		'quote': "some random text for previewing purposes",
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': []
	},
	'grandpa': {
		'acronym': 'GRANDPA',
		'name': 'Grandpa',
		'color': '000000',
		'quote': "some random text for previewing purposes",
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': []
	},
	'poppop': {
		'acronym': 'POPPOP',
		'name': 'Poppop',
		'color': '000000',
		'quote': "some random text for previewing purposes",
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': []
	},
	'alpha mom': {
		'acronym': 'MOM',
		'name': 'Mom',
		'color': '000000',
		'quote': "some random text for previewing purposes",
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': []
	},
	'alpha bro': {
		'acronym': 'BRO',
		'name': 'Bro',
		'color': '000000',
		'quote': "some random text for previewing purposes",
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': []
	},
	'grandma': {
		'acronym': 'GRANDMA',
		'name': 'Grandma',
		'color': '000000',
		'quote': "some random text for previewing purposes",
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': []
	},
	'nannasprite': {
		'acronym': 'NANNASPRITE',
		'name': 'Nannasprite',
		'color': '00D5F2',
		'quote': "Hoo hoo hoo! Of course I know what a computer is, John! I was just pulling your leg!",
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': []
	},
	'jaspersprite': {
		'acronym': 'JASPERSPRITE',
		'name': 'Jaspersprite',
		'color': 'F141EF',
		'quote': "Maybe you can win his affection by rubbing your cheek against him thats what i would do.",
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': []
	},
	'calsprite': {
		'acronym': 'CALSPRITE',
		'name': 'Calsprite',
		'color': 'F2A400',
		'quote': "HAA HAA HEE HEE HOO HOO",
		'quirk_prefix': '',
		'case': 'upper',
		'replacements': [["A", "<"], ["B", ">"], ["C", "?"], ["D", "<"], ["E", ">"], ["F", "?"], ["G", "<"], ["H", ">"], ["I", "?"], ["J", "<"], ["K", ">"], ["L", "?"], ["M", "<"], ["N", ">"], ["O", "?"], ["P", "<"], ["Q", ">"], ["R", "?"], ["S", "<"], ["T", ">"], ["U", "?"], ["V", "<"], ["W", ">"], ["X", "?"], ["Y", "<"], ["Z", ">"], ["<", "HAA "], [">", "HEE "], ["?", "HOO "]]
	},
	'davesprite': {
		'acronym': 'DAVESPRITE',
		'name': 'Davesprite',
		'color': 'F2A400',
		'quote': "thats the best fucking question anybody ever asked",
		'quirk_prefix': '',
		'case': 'lower',
		'replacements': []
	},
	'jadesprite': {
		'acronym': 'JADESPRITE',
		'name': 'Jadesprite',
		'color': '1F9400',
		'quote': "yes i figured shenanigans were probably involved",
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': []
	},
	'tavrisprite': {
		'acronym': 'TAVRISPRITE',
		'name': 'Tavrisprite',
		'color': '0715CD',
		'quote': "eEEEEEEEAAAAAAAAUUUUUUUURRRRRRRRUUUUUUUUEEEEEEEEGGGGGGGGHHHHHHHH,,,,,,,,.",
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': []
	},
	'fefetasprite': {
		'acronym': 'FEFETASPRITE',
		'name': 'Fefetasprite',
		'color': 'B536DA',
		'quote': "3833 < 383",
		'quirk_prefix': '3833 <',
		'case': 'normal',
		'replacements': [["E", "-E"], ["ee", "33"], ["H", ")("], ["h", ")("]]
	},
	'erisolsprite': {
		'acronym': 'ERISOLSPRITE',
		'name': 'Erisolsprite',
		'color': '4AC925',
		'quote': "wwoww, iit2 cool ii amu2e you, that really giivve2 meaniing to my joke of an exii2tence, ii mean WWOWW, thank2.",
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': [["I", "II"], ["i", "ii"], ["S", "2"], ["s", "2"], ["V", "VV"], ["v", "vv"], ["W", "WW"], ["w", "ww"]]
	},
	'the handmaid': {
		'acronym': '♈',
		'name': 'The Handmaid',
		'color': 'A10000',
		'quote': "some random text for previewing purposes",
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': []
	},
	'the summoner': {
		'acronym': '♉',
		'name': 'The Summoner',
		'color': 'A15000',
		'quote': "some random text for previewing purposes",
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': []
	},
	'the psiioniic':{
		'acronym': '♊',
		'name': 'The Ψiioniic',
		'color': 'A1A100',
		'quote': "some random text for previewing purposes",
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': []
	},
	'the signless':{
		'acronym': '♋',
		'name': 'The Signless',
		'color': '626262',
		'quote': "some random text for previewing purposes",
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': []
	},
	'the disciple': {
		'acronym': '♌',
		'name': 'The Disciple',
		'color': '416600',
		'quote': "some random text for previewing purposes",
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': []
	},
	'the dolorosa':{
		'acronym': '♍',
		'name': 'The Dolorosa',
		'color': '008141',
		'quote': "some random text for previewing purposes",
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': []
	},
	'redglare': {
		'acronym': '♎',
		'name': 'Neophyte Redglare',
		'color': '008282',
		'quote': "some random text for previewing purposes",
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': []
	},
	'mindfang': {
		'acronym': '♏',
		'name': 'Marquise Spinneret Mindfang',
		'color': '005682',
		'quote': "some random text for previewing purposes",
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': []
	},
	'darkleer': {
		'acronym': '♐',
		'name': 'E%ecutor Darkleer',
		'color': '000056',
		'quote': "some random text for previewing purposes",
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': []
	},
	'grand highblood': {
		'acronym': '♑',
		'name': 'The Grand Highblood',
		'color': '2B0057',
		'quote': "some random text for previewing purposes",
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': []
	},
	'dualscar': {
		'acronym': '♒',
		'name': 'Orphaner Dualscar',
		'color': '6A006A',
		'quote': "some random text for previewing purposes",
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': []
	},
	'the condesce': {
		'acronym': '♓',
		'name': 'Her Imperious Condescension',
		'color': '77003C',
		'quote': "this is what i get for lettin all proper dudes run shit instead of nasty clowns",
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': []
	},
	'spades slick': {
		'acronym': '♠',
		'name': 'Spades Slick',
		'color': '000000',
		'quote': "some random text for previewing purposes",
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': []
	},
	'clubs deuce': {
		'acronym': '♣',
		'name': 'Clubs Deuce',
		'color': '000000',
		'quote': "some random text for previewing purposes",
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': []
	},
	'diamonds droog': {
		'acronym': '♦',
		'name': 'Diamonds Droog',
		'color': '000000',
		'quote': "some random text for previewing purposes",
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': []
	},
	'hearts boxcars': {
		'acronym': '♥',
		'name': 'Hearts Boxcars',
		'color': '000000',
		'quote': "some random text for previewing purposes",
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': []
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
