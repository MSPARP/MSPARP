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
		'case': 'normal',
		'replacements': []
	},
	'tavros': {
		'acronym': 'AT',
		'name': 'adiosToreador',
		'color': 'A15000',
		'quote': "i THINK i AM PERFECTLY CAPABLE OF MANUFACTURING THESE ALLEGED \"dope\" HUMAN RHYMES",
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': []
	},
	'sollux':{
		'acronym': 'TA',
		'name': 'twinArmageddons',
		'color': 'A1A100',
		'quote': "do me a favor and 2pare me your 2pooky conundrum2 twoniight, youre kiind of pii22iing me off.",
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': []
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
		'case': 'normal',
		'replacements': []
	},
	'kanaya':{
		'acronym':'GA',
		'name':'grimAuxiliatrix',
		'color':'008141',
		'quote':"So You Are Destined To Edit It No Matter What And What You Submit Will Be What I Once Read Regardless",
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': []
	},
	'terezi': {
		'acronym': 'GC',
		'name': 'gallowsCalibrator',
		'color': '008282',
		'quote': "JOHN W3 AR3 SO MUCH B3TT3R TH4N YOU IN 3V3RY R3SP3CT 1TS R1D1CULOUS",
		'quirk_prefix': '',
		'case': 'upper',
		'replacements': [["A", "4"], ["I", "1"], ["E", "3"]]
	},
	'vriska': {
		'acronym': 'AG',
		'name': 'arachnidsGrip',
		'color': '005682',
		'quote': "It is 8ight groups of 8ight. I specifically counted them.",
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': []
	},
	'equius': {
		'acronym': 'CT',
		'name': 'centaursTesticle',
		'color': '000056',
		'quote': "D --> How do you know about my perspiration problem",
		'quirk_prefix': 'D -->',
		'case': 'normal',
		'replacements': []
		
	},
	'gamzee': {
		'acronym': 'TC',
		'name': 'terminallyCapricious',
		'color': '2B0057',
		'quote': "ThIs sOuNdS AmAzInG, i cAn't sEe hOw i wOuLdN'T Be aLl kIcKiNg tHe wIcKeD ShIt oUt Of sUcH KiNdS Of oPpOrTuNiTiEs",
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': []
	},
	'eridan': {
		'acronym': 'CA',
		'name': 'caligulasAquarium',
		'color': '6A006A',
		'quote': "wwho are you tryin to convvince wwith this ludicrous poppycock",
		'quirk_prefix': '',
		'case': 'normal',
		'replacements': []
	},
	'feferi': {
		'acronym': 'CC',
		'name': 'cuttlefishCuller',
		'color': '77003C',
		'quote': ")(oly mackerel, looks like SOM-EON-E woke up on t)(e wrong side of t)(e absurd )(uman bed!",
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
