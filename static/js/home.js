/*
* /js/home.js
* 
* Versions
*		1_0: Creation [Author: MSPARP Crew]
* 		2_0: Major Overhaul [Author: Alexander Bradley]
*/

// colors and quotes for the site's tagline (#random_greeting)
// greeting_data[x][0] //=> color code
// greeting_data[x][1] //=> quote text
var greeting_data = [
	['#626262', 'WHAT ARE YOU LOOKING AT, FUCKFACE?'],										// Karkat
	['#A15000', 'uM, wELCOME TO OUR WEBSITE, yOU SHOULD, uH, mAKE YOURSELF AT HOME'],		// Tavros
	['#2B0057', 'HaVe sOmE FaYgO AnD GeT YoUr mOtHeRfUcKiN ChAt oN! hOnK :o)'],				// Gamzee
	['#A1A100', 'ii wrote thii2 2iite iin ~ath, 2orry for all the lag'],					// Sollux
	['#A10000', 'y0u can talk t0 pe0ple here 0r n0t i d0nt really care'],					// Aradia
	['#416600', ':33 < *ac thinks this site is a purrfect place to chat* :3'],				// Nepeta
	['#000056', 'D --> Invite me to a chat, lowb100d, I demand it'],						// Equius
	['#005682', 'people keep disconnecting from you? Them\'s the 8r8ks!'],					// Vriska
	['#008141', 'Welcome To Microsoft Paint Adventures Role Playing.'],						// Kanaya
	['#008282', 'TH1S S1T3 T4ST3S 4WFUL! WH3R3S 4LL TH3 R3D?!'],							// Terezi
	['#77003C', 'W)(alecome to MSCARP, land glubb-Er!'],									// Feferi
	['#6A006A', 'wwhy doesnt anyone on this site wwant to talk wwith me']					// Eridan
];
var num_greetings = greeting_data.length;

var pangrams = [
	'Pack my box with five dozen liquor jugs.',
	'How quickly daft jumping zebras vex.',
	'Jackdaws love my big sphinx of quartz.',
	'The five boxing wizards jump quickly.',
	'My ex pub quiz crowd gave joyful thanks.',
	'Few quips galvanized the mock jury box.',
	'The quick brown fox jumps over the lazy dog.',
	'Fix problem quickly with galvanized jets.',
	'Waxy and quivering, jocks fumble the pizza.'
];
var num_pangrams = pangrams.length;

// We have some preliminary work to do when the page is loaded in terms of personas

// Load Prefs in at pageload if they exist, rather than resetting them.
var msparp_prefs = get_prefs();

// if there's nothing in localStorage...
if (!msparp_prefs || !get_length(msparp_prefs.personas)) {
	set_prefs({ 'personas': {} });
	msparp_prefs = get_prefs();
	
	// also, there's nothing to load or manage yet. Hide those!
	$('#load_modal, #manage_modal').addClass('disabled').attr('disabled','disabled');
}

// we are also going to have an array for the personas available. This'll be used in a few ways:
// 1. Save Personas - Prepopulate list for autocompletion. 
// 2. Load Personas - Prepopulate list for selection.
// 3. Manage Personas - Prepopulate list for selection. 
// All of these update on page load and save/manage, so it's always up to date for all modals.

var personas = get_prefs().personas;
propogate_personas();


/*
--------------------------------------------------------------------------------
 * Configure #character, #picky, #picky-exclude using info from characters.js
-------------------------------------------------------------------------------- */
var chars = characters.characters;
var groups = characters.groups;
var NUM_CHARS = chars.length;
var NUM_GROUPS = groups.length;

var $char = $('#character');

for(i = 0; i < NUM_CHARS; i++) {
    $char.append(make_option(i, chars[i].option));
}


/*
--------------------------------------------------------------------------------
 * Updates for Events
-------------------------------------------------------------------------------- */

// Update Preview Text when color, acronym, prefix or suffix change
function update_preview() {
	$('#text_preview')
		.css('color', '#' + $('#color').val())			// color
		.find('.acronym span')
			.text($('#acronym').val())					// acronym
	.end()
		.find('.quote .quirk_prefix')
		.text($('#quirk_prefix').val())					// prefix
	.end()
		.find('.quote .quirk_suffix')
		.text($('#quirk_suffix').val());				// suffix
}

// Update Preview Case
function update_case() {
	var $quote = $('#text_preview').find('.quote .sentence');
	$quote.text(text_manipulations[$('#case').val()]($quote.attr('data-og-quote')));
}

// update the "X left" help text for acronym, prefix and suffix
function update_chars_left() {
	chars_left = $(this).attr('maxlength') - $(this).val().length;
	
	$(this)
		.siblings('.help-inline')
		.find('span')
			.text(chars_left)
			.toggleClass('badge badge-warning', (chars_left == 0));
			
	update_preview();
}

var $quote_sentence = $('#text_preview').find('.quote .sentence');
// update fields when you change who you are
function update_character() {
	// set label[for=picky] span to the data-verb attribute of the selected #character, or else use 'Pester'
	// TODO THIS IS BROKEN NOW, ALEX. AND IT'S ALL YOUR FAULT!
	// $picky_span.text(($('#character').find('option:selected').attr('data-verb') ? $('#character').find('option:selected').attr('data-verb') : 'Pester'));
	
	// Change Placeholder for Modal
	// TODO there is nothing on the page with #persona -- what was this for? Placeholder attribute of what? Maybe a header?
	// $('#persona').attr('placeholder', $('#character option:selected').text() + ' Prefs');
	
	// load character info from characters.js
	selected_char = chars[$('#character').val()];
	
	// null check (page load)
	if(selected_char) {
		$('#acronym').val(selected_char['acronym']).keyup();
		$('#name').val(selected_char['name']);
		$('#color').val(selected_char['color']);
		$('#quirk_prefix').val(selected_char['quirk_prefix']);
		$('#quirk_suffix').val(selected_char['quirk_suffix']);
		$('#case').val(selected_char['case']);
		
		// Doc Scratch One Off
		if(selected_char['name'] === "Doc Scratch") {
			$('#text_preview').css('background-color', '#0e4603');
		} else {
			$('#text_preview').css('background-color', '#eeeeee');
		}
		
		// update some things that we changed
		update_replacements(selected_char);
		update_colorpicker_from_color();
		update_quote($('#character').val());
		$('.charsleft').keyup();
		$('.chzn-select').trigger("liszt:updated");
	}
}

// update replacements when a new character is chosen
function update_replacements(char_obj) {
	
	// Clear all values before we get started
	$('.replacements')
		.find('[name^=quirk], [name^=regex]')
		.val('');
		
	// Letter Replacements
	var letter = char_obj['replacements'];
	var llen = (letter ? letter.length : 0);
	
	if($('#replacements').find('.controls').length >= llen) {
		// If there's more fields available than we need, get rid of some
		$('#replacements')
			.find('.controls')
			.slice(Math.max(llen, 1))	// don't remove all of them
				.remove();
	} else {
		// and if there's fewer than we need, add some
		while($('#replacements').find('.controls').length < llen) {
			add_letter_replacement();
		}
	}
	
	for(i = 0; i < llen; i++) {
		$('[name=quirk_from]')
			.eq(i)
			.val(letter[i][0]);
		$('[name=quirk_to]')
			.eq(i)
			.val(letter[i][1]);
	}
	
	// RegExp -- this code mirrors the above for Letter Replacements
	// TODO DRY: We should use one set of code for both! 
	var regexp = char_obj['regexes'];
	var rlen = (regexp ? regexp.length : 0);
	
	if($('#regex_replacements').find('.controls').length >= rlen) {
		$('#regex_replacements')
			.find('.controls')
			.slice(Math.max(rlen, 1))
				.remove();
	} else {
		while($('#regex_replacements').find('.controls').length < rlen) {
			add_regex_replacement();
		}
	}
	
	for(i = 0; i < rlen; i++) {
		$('[name=regex_from]')
			.eq(i)
			.val(regexp[i][0]);
		$('[name=regex_to]')
			.eq(i)
			.val(regexp[i][1]);
	}
}

// Take a character ID. Update their quote from character.js
function update_quote(char_id) {
	// make the next few lines a little less messy
	selected_char = chars[char_id];
	
	$quote_sentence
		.attr('data-og-quote', (selected_char['quote'].length > 0 ? selected_char['quote'] : get_pangram()))
		.text($('#text_preview .sentence').attr('data-og-quote'));
}


/*
--------------------------------------------------------------------------------
 * Save Data
-------------------------------------------------------------------------------- */
// commit save data to localStorage
function save_data() {
	// add the new persona to the local object
	var t = get_prefs();
	t.personas[($('#save_persona').val() != 'add_new' ? $('#save_persona').val() : $('#save_new').val())] = prep_save_data();
	
	// save this local object to localStorage
	set_prefs(msparp_prefs);
	
	// clean up #save_modal; hide #save_new
	$('#save_persona, #save_new').val('');
	change_save_persona();
	
	// make sure the personas are placed in all necessary dropdowns
	propogate_personas();
	
	// ensure these buttons are visible
	$('#load_modal, #manage_modal').removeClass('disabled').removeAttr('disabled');
}

// returns an object containing persona data
function prep_save_data() {
	var temp = { 'prefname': $('#save_new').val() };
	var replacements = [];
	var regexes = [];

	// replacements
	$('[name=quirk_from]').each(function () {
	    if($(this).val().length && $(this).siblings('[name=quirk_to]').val().length) {
	        replacements.push([ $(this).val(), $(this).siblings('[name=quirk_to]').val()]);
	    }
	});
	
	$('[name=regex_from]').each(function () {
	    if($(this).val().length && $(this).siblings('[name=regex_to]').val().length) {
	        regexes.push([ $(this).val(), $(this).siblings('[name=regex_to]').val()]);
	    }
	});
	
	temp['character'] = $('#character').val();
	temp['picky'] = $('#picky').val();
	temp['exclude'] = $('#picky_exclude').val();
	temp['acronym'] = $('#acronym').val();
	temp['name'] = $('#name').val();
	temp['color'] = $('#color').val();
	temp['case'] = $('#case').val();
	temp['quirk_prefix'] = $('#quirk_prefix').val();
	temp['quirk_suffix'] = $('#quirk_suffix').val();
	temp['replacements'] = replacements;
	temp['regexes'] = regexes;
	
	return temp;
}

// shows / hides "Name New Persona" field in Save Modal
function change_save_persona() {
	if($('#save_persona').val() == 'add_new') {
		$('#save_new')
			.closest('.control-group')
			.show();
		
		$('#save_persona_warning').hide();
	} else {
		$('#save_new')
			.val('')
			.closest('.control-group')
				.hide();
				
		if($('#save_persona').val()) {
			$('#save_persona_warning')
				.show()
				.find('span')
					.text($(this).find('option:selected').text());
		}
	}
}


/*
--------------------------------------------------------------------------------
 * Load Data
-------------------------------------------------------------------------------- */
function load_data() {
	var temp = JSON.parse(localStorage.getItem('msparp_prefs')).personas[$('#load_persona').val()];
	
	$('#character').val(temp['character']);
	$('#picky').val(temp['picky']);
	$('#picky_exclude').val(temp['exclude']);
	$('#acronym').val(temp['acronym']);
	$('#name').val(temp['name']);
	$('#color').val(temp['color']);
	$('#case').val(temp['case']);
	$('#quirk_prefix').val(temp['quirk_prefix']);
	$('#quirk_suffix').val(temp['quirk_suffix']);	
	update_replacements(temp);	
	
	// updates
	update_colorpicker_from_color();
	update_preview();
	update_case();
	$('.charsleft').keyup();
	
	// When you load a persona, load their quote in from characters.js
	update_quote(temp['character']);
		
	// Update Chosen so the changes to the hidden inputs are reflected
	$('.chzn-select').trigger("liszt:updated");
}

/*
--------------------------------------------------------------------------------
 * Manage Data
-------------------------------------------------------------------------------- */
// Rename
function manage_data() {
	if($.trim($('#rename_persona').val()).length > 0) {
		rename_persona($('#manage_persona').val(), $('#rename_persona').val())
	}
	$('#rename_persona').val('');
	
	propogate_personas();
}

// Erase ALL Personas from localStorage
function clear_localStorage() {
	var confirm = prompt('THIS WILL DELETE ALL PERSONA DATA FROM\nYOUR BROWSER. THIS IS NOT REVERSIBLE.\nTO CONFIRM, TYPE "DELETE" (ALL CAPS) HERE:');
	if(confirm === 'DELETE') {
		set_prefs({ 'personas': {} });
		propogate_personas();
	}
}

// Delete a single Persona
function delete_persona(persona_name) {
	if(confirm('Are you sure you\'d like to delete the persona ' + persona_name + '? This cannot be undone.')) {
		// close the modal first
		$('#modal_managedata').modal('hide');
		
		var t = get_prefs();
		delete t.personas[persona_name];

		if(!get_length(t.personas)) {
			t = { 'personas': {} };
		}
		
		set_prefs(t);
		propogate_personas();
	}
}

// Import / Export Personas
function import_personas() {
	var t = get_prefs();
	try {
		var u = JSON.parse($('#persona_data').val());
	} catch (err) {
		if(err.name == 'SyntaxError') {
			alert("It looks like you've entered in some bad persona data.\nYou may want to try copying and pasting into this field again.");
		} else {
			alert('An error occurred. Please try again.');
		}
		
		propogate_personas();
		
		return;
	}	

	console.log('success!');

	$.each(u.personas, function(key, value){
	    if(t.personas[key]) {
	        t.personas[key + ' (Imported ' + (new Date().getTime()) + ')'] = value;
	    } else {
	        t.personas[key] = value;
	    }
	});	
	
	set_prefs(t);
	propogate_personas();
}

// Rename a single Persona
function rename_persona(oldname, newname) {
	var t = get_prefs();
	
	// Simple swap
	t.personas[newname] = t.personas[oldname];
	delete t.personas[oldname];
	
	set_prefs(t);
}

/*
--------------------------------------------------------------------------------
 * Quirk Replacements
-------------------------------------------------------------------------------- */

var $letter_replace = $('#replacements .controls').first().clone();
function add_letter_replacement() {
	$('#replacements').append($letter_replace.clone());
}

var $regex_replace = $('#regex_replacements .controls').first().clone();
function add_regex_replacement() {
	$('#regex_replacements').append($regex_replace.clone());
}


/*
--------------------------------------------------------------------------------
 * localStorage Calls
-------------------------------------------------------------------------------- */
function set_prefs(pref_object) {
	localStorage.setItem('msparp_prefs', JSON.stringify(pref_object));	
}

function get_prefs() {
	return (localStorage.msparp_prefs ? JSON.parse(localStorage.msparp_prefs) : undefined);
}

function propogate_personas() {
	var $dropdowns = $('#save_persona, #load_persona, #manage_persona');
	var $add_new = $('<option />', {
				'text': 'Add New Persona...',
				'value': 'add_new'
			});
	
	// load personas from localStorage\
	personas = get_prefs().personas;
	if(get_length(personas) > 0) {
		// ensure these buttons are enabled
		$('#load_modal, #manage_modal').removeClass('disabled').removeAttr('disabled');
	} else {
		$('#load_modal, #manage_modal').addClass('disabled').attr('disabled','disabled');
	}
	
	// clear all the values out
	$dropdowns
		.find('option')
		.remove();
	
	// populate the dropdown with available personas
	for (persona in personas) {
		$dropdowns.append(make_option(persona, persona));
	};
	
	$('#save_persona').append($add_new.clone());
	
	// TODO Man this is getting sloppy. Barf.
	if($('#save_persona option').length == 1) {
		$('#save_persona')
			.closest('.control-group')
			.hide();
			
		$('#save_overwrite').hide();
		
		$('#save_new')
			.closest('.control-group')
			.show();
	} else {
		$('#save_persona')
			.closest('.control-group')
			.show();
			
		$('#save_overwrite').show();
		
		$('#save_new')
			.closest('.control-group')
			.hide();
	}
	
	$('#persona_data')
		.val(JSON.stringify(get_prefs()))
		.focus(function () {
			$(this).select();
		});
	
	// Refresh Chosen
	$dropdowns.trigger("liszt:updated");
}


/*
--------------------------------------------------------------------------------
 * String Manipulation for Previews
-------------------------------------------------------------------------------- */
String.prototype.toTitleCase = function () {
    return this.replace(/\w\S*/g, function(txt){return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();});
}

String.prototype.toAlternatingCase = function () {
	tmp = this.toLowerCase(); (this[0] == this[0].toLowerCase() ? i = 1 : i = 0); for(; i < tmp.length; i = i+2) { tmp = tmp.substr(0,i) + tmp[i].toUpperCase() + tmp.substr(i+1); } return tmp;
}

String.prototype.toInvertedCase = function () {
	tmp = ""; for (i=0; i< this.length; i++) { t=this[i]; t=(t==t.toUpperCase()?t.toLowerCase():t.toUpperCase()); tmp+=t; } return tmp;
}

// fast string replacement via http://dumpsite.com/forum/index.php?topic=4.msg8#msg8
String.prototype.replaceAll = function(str1, str2, ignore) {
	return this.replace(new RegExp(str1.replace(/([\/\,\!\\\^\$\{\}\[\]\(\)\.\*\+\?\|\<\>\-\&])/g,"\\$&"),(ignore?"gi":"g")),(typeof(str2)=="string")?str2.replace(/\$/g,"$$$$"):str2);
};

var text_manipulations = {
	'normal': function (str) {
		return str;
	},
	'lower': function (str) {
		return str.toLowerCase();
	},
	'upper': function (str) {
		return str.toUpperCase();
	},
	'title': function (str) {
		return str.toTitleCase();
	},
	'alternating': function (str) {
		return str.toAlternatingCase();
	},
	'inverted': function (str) {
		return str.toInvertedCase();
	}
};


/*
--------------------------------------------------------------------------------
 * Helpers
-------------------------------------------------------------------------------- */
// returns a number 0 - x
function rand(x) {
	return Math.floor(Math.random()*x);
}

// returns an <option> for appending to dropdowns
function make_option(val, txt) {
    return $('<option />', { 'value': val, 'text': txt });
}

// returns a string containing a random pangram 
function get_pangram() {
	return pangrams[rand(num_pangrams)];
}

// update colors; these are annoying, but necessary
function update_color_from_colorpicker(hex) {
	$('#color').val(hex);
	$('#text_preview').css('color', '#' + hex);
}

function update_colorpicker_from_color() {
	$('#color').ColorPickerSetColor($('#color').val());
	$('#text_preview').css('color', '#' + $('#color').val());
}

// get an object's length
function get_length(obj) {
	return $.map(obj, function(n, i) { return i; }).length;
}


/*
--------------------------------------------------------------------------------
 * jQuery
-------------------------------------------------------------------------------- */
$(function() {
	// generate an index for greeting_data
	var greeting = rand(num_greetings);
	
	// set the color and text for the #random_greeting
	$('#random_greeting')
		.css('color', greeting_data[greeting][0])
		.text(greeting_data[greeting][1]);

	// put a pangram into the quote field by default
	$('#text_preview')
		.find('.quote .sentence')
		.attr('data-og-quote', get_pangram())
		.text($('#text_preview .sentence').attr('data-og-quote'));
	
	// turn on and configure the color picker
	$('#color').ColorPicker({
		'color': '#000000',
		'onShow': function (colpkr) {
			$(colpkr).fadeIn(500);
			return false;
		},
		'onHide': function (colpkr) {
			$(colpkr).fadeOut(500);
			return false;
		},
		'onChange': function (hsb, hex, rgb) {
			update_color_from_colorpicker(hex);
		}
	}).keyup(function(){	
		update_colorpicker_from_color();
	});
	
	// Activates Chosen on specific dropdowns
	$(".chzn-select").chosen();
	
	// Hard to be responsive with fixed widths!
	/* // TODO fix this so it works at all widths
	$('#char_form')
		.find('.chzn-container')
		.removeAttr('style');
	*/
	
	// Chosen to update Label text for #picky
	update_character();
	$('#character').change(update_character);
	
	// Show New Persona Name if you choose to rename an existing persona
	$('#save_persona').change(change_save_persona);
	change_save_persona();
	
	//Set up event handler for removal of quirks	
	$('.replacements')
		.on('click', '.close:not(.add)', function(e) {
		    $(this).closest('.controls').remove();
		    e.preventDefault();
		});
		
	$('#replacements')
		.on('click', '.add', function(e) {
		    add_letter_replacement();
		    e.preventDefault();
		});
		
	$('#regex_replacements')
		.on('click', '.add', function(e) {
		    add_regex_replacement();
		    e.preventDefault();
		});
	
	// Bootstrap
	$(".alert").alert();
	$('#exclude_help').tooltip({
		'placement': 'right',
		'delay': 300
	}).click(function (e) {
		e.preventDefault();
	});
	
	// Characters left for Prefix / Suffix / Acronym
	$('.charsleft').keyup(update_chars_left).keyup();
	
	// Update preview on page load
	update_preview();
	
	// trigger preview update on case change
	update_case()
	$('#case').change(update_case);
	
	// Save / Load / Manage Personas
	if (!Modernizr.localstorage) {
		$('#save_modal').closest('.control-group').remove();
		$('#modal_import_export').remove();
	}
	
	//$('#save_modal').click(save_modal);
	//$('#load_modal').click(load_modal);
	// $('#manage_modal').click(cls);
	
	$('#save_data').click(save_data);
	$('#load_data').click(load_data);
	
	// Manage
	$('#clear_localStorage').click(clear_localStorage);
	$('#import_export_data').click(import_personas);
	$('#manage_data').click(manage_data);
	$('#manage_modal_form .controls')
		.on('click', '.close', function(e) {
			delete_persona($('#manage_persona').val());
		    e.preventDefault();
		});
});

