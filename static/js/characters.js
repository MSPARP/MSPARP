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
		'case': 'lower',
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
		'case': 'lower',
		'replacements': [['i', 'ii'], ['s', '2']]
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
		'case': 'lower',
		'replacements': [["v", "vv"], ["w", "ww"]]
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
	'kankri':{
		'acronym': 'KANKRI',
		'name': 'Kankri',
		'color': 'FF0000',
		'quote': "",
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': [["B", "6"], ["b", "6"], ["O", "9"], ["o", "9"]]
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
	'meenah': {
		'acronym': 'MEENAH',
		'name': 'Meenah',
		'color': '77003C',
		'quote': "sayin fish puns is obviously kind of this thing i do stupid G-ET WIT)( T)(-E PROGRAM",
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': [["E", "-E"], ["H", ")("]]
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
