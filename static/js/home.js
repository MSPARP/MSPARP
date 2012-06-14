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

	$('label.picky-header input').click(function() {
		var checks = $(this.parentNode).next('div.picky-group').find('input');
		if (this.checked) {
			checks.attr('checked','checked');
		} else {
			checks.val([]);
		}
	});

	function setGroupInput(groupDiv) {
		var label = $(groupDiv).prev('label.picky-header').find('input')[0];
		var group = $(groupDiv).find('input');
		var groupChecked = $(groupDiv).find('input:checked');
		if (groupChecked.length==0) {
			$(label).removeAttr('checked').removeAttr('indeterminate');
		} else if (groupChecked.length==group.length) {
			$(label).removeAttr('indeterminate').attr('checked','checked');
		} else {
			$(label).removeAttr('checked').attr('indeterminate','indeterminate');
		}
	}

	var pickyGroups = $('div.picky-group');
	for (i=0; i<pickyGroups.length; i++) {
		setGroupInput(pickyGroups[i]);
	}

	$('div.picky-group input').click(function() {
		setGroupInput(this.parentNode.parentNode);
	});

	$('div.defaults-off').hide();
	settingUp=false;

});

