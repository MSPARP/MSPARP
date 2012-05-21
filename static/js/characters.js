var characters={
	'anonymous/other':{
		'acronym':'??',
		'name':'anonymous',
		'color':'000000',
		'quote':"some random text for previewing purposes",
		'quirks':''
	},
	'original character':{
		'acronym':'**',
		'name':'Original Character',
		'color':'FF00FF',
		'quote':"I am too awesome for hussie to include in the canon",
		'quirks':''
	},
	'doc scratch':{
		'acronym':'',
		'name':'Doc Scratch',
		'color':'FFFFFF',
		'quote':"You know you're going to anyway. You won't be able to help yourself.",
		'quirks':''
	},
	'john':{
		'acronym':'EB',
		'name':'ectoBiologist',
		'color':'0715CD',
		'quote':"i don't know, maybe! what do i do!",
		'quirks':['lower']
	},
	'dave':{
		'acronym':'TG',
		'name':'turntechGodhead',
		'color':'E00707',
		'quote':"you dont seem to harbor any sympathy for the fact that ive burrowed fuck deep into lively, fluffy muppet buttock",
		'quirks':['lower','depunct']
	},
	'rose':{
		'acronym':'TT',
		'name':'tentacleTherapist',
		'color':'B536DA',
		'quote':"You know you like the mannequin dick. Accept it.",
		'quirks':[]
	},
	'jade':{
		'acronym':'GG',
		'name':'gardenGnostic',
		'color':'4AC925',
		'quote':"i am never going to sleep again!",
		'quirks':['lower']
	},
	'jane':{
		'acronym':'GG',
		'name':'gutsyGumshoe',
		'color':'00D5F2',
		'quote':"If the chats and surplus dinners were truly important, I wouldn't want to interrupt.",
		'quirks':[]
	},
	'dirk':{
		'acronym':'TT',
		'name':'timaeusTestified',
		'color':'F2A400',
		'quote':"It's not 4 you jackass, it's fucking nothing. There is no end.",
		'quirks':[]
	},
	'roxy':{
		'acronym':'TG',
		'name':'tipsyGnostalgic',
		'color':'FF6FF2',
		'quote':"it seems 2 me that there is a (MATHS) % chance of you bein a huge tightass",
		'quirks':[]
	},
	'jake':{
		'acronym':'GT',
		'name':'golgothasTerror',
		'color':'1F9400',
		'quote':"Jesus christofer kringlefucker and here i thought i was rugged!",
		'quirks':[]
	},
	'aradia':{
		'acronym':'AA',
		'name':'apocalypseArisen',
		'color':'A10000',
		'quote':"maybe if i say st0p en0ugh s0mething else will happen instead 0f the thing that d0es",
		'quirks':''
	},
	'equius':{
		'acronym':'CT',
		'name':'centaursTesticle',
		'color':'000056',
		'quote':"D --> How do you know about my perspiration problem",
		'quirks':['prefix("D --> ")']
		
	},
	'karkat':{
		'acronym':'CG',
		'name':'carcinoGeneticist',
		'color':'626262',
		'quote':"NO. MORE LIKE TWITCHY EYED PROJECTILE VOMITING IN UTTER DISGUST FRIENDS, WHILE I PERFORATE MY BONE BULGE WITH A CULLING FORK.",
		'quirks':['upper']
	},
	'tavros':{
		'acronym':'AT',
		'name':'adiosToreador',
		'color':'A15000',
		'quote':"i THINK i AM PERFECTLY CAPABLE OF MANUFACTURING THESE ALLEGED \"dope\" HUMAN RHYMES",
		'quirks':['inverseCaps','hornedEmoticons']
	},
	'sollux':{
		'acronym':'TA',
		'name':'twinArmageddons',
		'color':'A1A100',
		'quote':"do me a favor and 2pare me your 2pooky conundrum2 twoniight, youre kiind of pii22iing me off.",
		'quirks':''
	},
	'feferi':{
		'acronym':'CC',
		'name':'cuttlefishCuller',
		'color':'77003C',
		'quote':")(oly mackerel, looks like SOM-EON-E woke up on t)(e wrong side of t)(e absurd )(uman bed!",
		'quirks':''
	},
	'terezi':{
		'acronym':'GC',
		'name':'gallowsCalibrator',
		'color':'008282',
		'quote':"JOHN W3 AR3 SO MUCH B3TT3R TH4N YOU IN 3V3RY R3SP3CT 1TS R1D1CULOUS",
		'quirks':['upper','l33t']
	},
	'kanaya':{
		'acronym':'GA',
		'name':'grimAuxiliatrix',
		'color':'008141',
		'quote':"So You Are Destined To Edit It No Matter What And What You Submit Will Be What I Once Read Regardless",
		'quirks':['titleCase','depunct']
	},
	'eridan':{
		'acronym':'CA',
		'name':'caligulasAquarium',
		'color':'6A006A',
		'quote':"wwho are you tryin to convvince wwith this ludicrous poppycock ",
		'quirks':['depunct','lower']
	},
	'gamzee':{
		'acronym':'TC',
		'name':'terminallyCapricious',
		'color':'2B0057',
		'quote':"ThIs sOuNdS AmAzInG, i cAn't sEe hOw i wOuLdN'T Be aLl kIcKiNg tHe wIcKeD ShIt oUt Of sUcH KiNdS Of oPpOrTuNiTiEs",
		'quirks':['alternatingCaps']
	},
	'nepeta':{
		'acronym':'AC',
		'name':'arsenicCatnip',
		'color':'416600',
		'quote':":33 < but do you think you could purrhaps please spare your computer for just the most fl33ting of moments?",
		'quirks':['prefix(":33 < ")']
	},
	'vriska':{
		'acronym':'AG',
		'name':'arachnidsGrip',
		'color':'005682',
		'quote':"It is 8ight groups of 8ight. I specifically counted them.",
		'quirks':''
	},
}
$(document).ready(function(){
	var config=$('#character-config');
	var settingUp=true;
	function updatePreview(){
		$('#color-preview').css('color','#'+config.find('input[name="color"]').val());
		var acronym=config.find('input[name="acronym"]').val();
		$('#color-preview #acronym').text(acronym+(acronym.length>0?': ':''));
	}
	$('select.character-select').change(function(){
		var val=$(this).attr('value');
		if(characters[val]){
			var chr=characters[val];
			var keys=['acronym','name','color'];
			for(var i=0;i<keys.length;i++){
				config.find('input[name="'+keys[i]+'"]').val(chr[keys[i]]);
			}
			var quirksElement=$('#typing-quirks');
			quirksElement.find('input').val([]);
			var quirks=chr['quirks'];
			for(var i=0;i<quirks.length;i++){
				var name=quirks[i].split("(")[0];
				quirksElement.find('input[name="quirk-'+name+'"]').attr('checked','checked');
				if(quirks[i].indexOf('(')!=-1){
					var parameterRE=new RegExp('"([^"]+)"','g');
					var match,argi=0;
					do{
						var match=parameterRE.exec(quirks[i]);
						if(match){
							quirksElement.find('input[name="qarg-'+name+'-'+argi+'"]').val(match[1]);
							argi++;
						}
					}while(match);
					
				}
			}
			config.find('#color-preview #quote').text(chr['quote']);
			updatePreview();
			if(!settingUp){
				$('#character-config').show();
				$('#typing-quirks').show();
				$('button.show-button[data-target="character-config"]').hide();
				$('button.show-button[data-target="typing-quirks"]').hide();
			}
		}
	});
	config.find('input').change(updatePreview).keyup(updatePreview);
	updatePreview();
	var name = $("select.character-select").attr('value');
	config.find('#color-preview #quote').text(characters[name]['quote']);
	var colorBox=config.find('input[name="color"]')

	colorBox.ColorPicker({
		onSubmit: function(hsb, hex, rgb, el) {
			$(el).val(hex);
			$(el).ColorPickerHide();
		},
		onBeforeShow: function () {
			$(this).ColorPickerSetColor(this.value);
		},
		onChange: function (hsb, hex, rgb) {
			$('#color-preview').css('color', '#' + hex);
			colorBox.val(hex);
		}

	})
	.bind('keyup', function(){
		$(this).ColorPickerSetColor(this.value);
	});

	$('input[name="picky"]').change(function(){
		if($(this).is(':checked')){
			$('#picky-matches').show();
		}else{
			$('#picky-matches').hide();
		}
	}).change();

	$('button.show-button').click(function(){
		$('#'+$(this).attr('data-target')).show();
		$(this).hide();
		return false;
	});
	$('b.picky-header').click(function(){
		var checks=$(this).next('div.picky-group').find('input');
		if(checks[0].checked){
			checks.val([]);
		}else{
			checks.attr('checked','checked');
		}

	});
	$('div.defaults-off').hide();
	settingUp=false;
});
