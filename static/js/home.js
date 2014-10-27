$(document).ready(function() {

	if (document.cookie=="") {
		$(".error").append("It seems you have cookies disabled. Unfortunately cookies are essential for MSPARP to work, so you'll need to either enable them or add an exception in order to use MSPARP.");
	}

	var settingUp = true;
	var config = $('#character-config');

	function updatePreview() {
		$('#color-preview').css('color', '#'+config.find('input[name="color"]').val());
		var acronym = config.find('input[name="acronym"]').val();
		$('#color-preview #acronym').text(acronym+(acronym.length>0?': ':''));
	}

	$('select[name="character"]').change(function() {
		if(characters[this.value]) {
			var newCharacter = characters[this.value];
			config.find('#color-preview #quote').text(newCharacter['quote']);
			if (this.value=="kankri") {
				$.get('/static/txt/seri9usly_this_is_fucking_ridicul9us.txt', function(reply) {
					config.find('#color-preview #quote').text(reply);
				});
			}
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
	if (name=="kankri") {
		$.get('/static/txt/seri9usly_this_is_fucking_ridicul9us.txt', function(reply) {
			config.find('#color-preview #quote').text(reply);
		});
	}

	if (localStorage.pstyle == 'text'){
			$('input[name="astext"]').prop('checked',true);
			$('#picky-icon').hide();
			$('#picky-text').show();
			} else {
			$('#picky-icon').show();
			$('#picky-text').hide();
			}
	
	$('input[name="astext"]').change(function() {
			if($(this).is(':checked')) {
				$('#picky-icon').hide();
				$('#picky-text').show();
				localStorage.setItem('pstyle', 'text');
			} else {
				$('#picky-icon').show();
				$('#picky-text').hide();
				localStorage.setItem('pstyle', 'icon');
			}
		}).change();
	
	$('input[name="picky"]').change(function() {
		if($(this).is(':checked')) {
			$('#picky-matches').show();
			if (localStorage.pstyle == 'text'){
				$('input[name="astext"]').prop('checked',true);
				}
		} else {
			$('#picky-matches').hide();
			$('#picky-matches input').removeAttr('checked').removeAttr('indeterminate');
		}
	}).change();

	$('button.show-button').click(function() {
		$('#'+$(this).attr('data-target')).show();
		$(this).hide();
		return false;
	});

	$('label.picky-header input').click(function() {
		var checks = $(this.parentNode.parentNode).next('div.picky-group').find('input');
		if (this.checked) {
			checks.attr('checked','checked');
		} else {
			checks.val([]);
		}
	});

	$('#container').addClass(localStorage.hdpi);
	
	$('.hdpidisable').click(function() {
		$('#container').addClass('hdpi-disabled');
		localStorage.setItem('hdpi', 'hdpi-disabled');
	});
	
	$('.hdpienable').click(function() {
		$('#container').removeClass('hdpi-disabled');
		localStorage.setItem('hdpi', '');
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

