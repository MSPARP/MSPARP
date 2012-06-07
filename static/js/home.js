$(document).ready(function() {

	var settingUp = true;
	var config = $('#character-config');

	function updatePreview() {
		$('#color-preview').css('color', '#'+config.find('input[name="color"]').val());
		var acronym = config.find('input[name="acronym"]').val();
		$('#color-preview #acronym').text(acronym+(acronym.length>0?': ':''));
	}

	$('select.character-select').change(function() {
		var val = $(this).attr('value');
		if(characters[val]) {
			var chr = characters[val];
			var keys = ['acronym', 'name', 'color'];
			for(var i=0; i<keys.length; i++) {
				config.find('input[name="'+keys[i]+'"]').val(chr[keys[i]]);
			}
			var quirksElement = $('#typing-quirks');
			quirksElement.find('input').val([]);
			var quirks = chr['quirks'];
			for(var i=0; i<quirks.length; i++) {
				var name = quirks[i].split("(")[0];
				quirksElement.find('input[name="quirk-'+name+'"]').attr('checked','checked');
				if(quirks[i].indexOf('(')!=-1) {
					var parameterRE = new RegExp('"([^"]+)"','g');
					var match, argi = 0;
					do {
						var match = parameterRE.exec(quirks[i]);
						if(match){
							quirksElement.find('input[name="qarg-'+name+'-'+argi+'"]').val(match[1]);
							argi++;
						}
					} while(match);
					
				}
			}
			config.find('#color-preview #quote').text(chr['quote']);
			updatePreview();
			if(!settingUp) {
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

	var colorBox = config.find('input[name="color"]');
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

	}).bind('keyup', function() {
		$(this).ColorPickerSetColor(this.value);
	});

	$('input[name="picky"]').change(function() {
		if($(this).is(':checked')) {
			$('#picky-matches').show();
		} else {
			$('#picky-matches').hide();
		}
	}).change();

	$('button.show-button').click(function() {
		$('#'+$(this).attr('data-target')).show();
		$(this).hide();
		return false;
	});

	$('b.picky-header').click(function() {
		var checks = $(this).next('div.picky-group').find('input');
		if(checks[0].checked){
			checks.val([]);
		}else{
			checks.attr('checked','checked');
		}
	});

	$('div.defaults-off').hide();
	settingUp=false;

});

