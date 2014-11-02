$(document).ready(function() {

	if (document.cookie=="") {
		$(".error").append("It seems you have cookies disabled. Unfortunately cookies are essential for MSPARP to work, so you'll need to either enable them or add an exception in order to use MSPARP.");
	}

	var settingUp = true;
	var config = $('#character-config');

	var storage = (function() {
	  var uid = new Date;
	  var result;
	  try {
		localStorage.setItem(uid, uid);
		result = localStorage.getItem(uid) == uid;
		localStorage.removeItem(uid);
		return result && localStorage;
	  } catch (exception) {}
	}());
	
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

	if (storage){
		if (localStorage.pstyle == 'text'){
				$('input[name="astext"]').prop('checked',true);
				disablePicky('#picky-text');
				enablePicky('#picky-icon');
				$('#picky-icon').hide();
				$('#picky-text').show();
				} else {
				disablePicky('#picky-icon');
				enablePicky('#picky-text');
				$('#picky-icon').show();
				$('#picky-text').hide();
				}
	}
	
	$('input[name="astext"]').change(function() {
			if($(this).is(':checked')) {
				disablePicky('#picky-icon');
				enablePicky('#picky-text');
				$('#picky-icon').hide();
				$('#picky-text').show();
				if (storage){
				localStorage.setItem('pstyle', 'text');}
			} else {
				disablePicky('#picky-text');
				enablePicky('#picky-icon');
				$('#picky-icon').show();
				$('#picky-text').hide();
				if (storage){
				localStorage.setItem('pstyle', 'icon');}
			}
		}).change();
		
	if(storage){	
		if (localStorage.creppy == 'creppy'){
			$('head').append('<link rel="stylesheet" id="creppyid" href="/static/css/mscreppy.css?41101" type="text/css" />');
			$('input[name="enablecreppy"]').prop('checked',true);
			$('.hidecreppy').show();
			}
		else {
			$('.hidecreppy').hide();
		}
	}
		
		$('input[name="enablecreppy"]').change(function() {
			if($(this).is(':checked')) {
				$('head').append('<link rel="stylesheet" id="creppyid" href="/static/css/mscreppy.css?41101" type="text/css" />');
				$('.hidecreppy').show();
				if (storage){
				localStorage.setItem('creppy', 'creppy');}
				} else {
				$("#creppyid").prop('disabled', true);
				$("#creppyid").remove();
				$('.hidecreppy').hide();
				if (storage){
				localStorage.setItem('creppy', '');}
			}
		}).change();
		
	if (storage){	
		if (localStorage.dfall == 'downfall'){
			$('input[name="toggledownfall"]').prop('checked',true);
			}

	$('body').addClass(localStorage.dfall);
	}
		
	$('input[name="toggledownfall"]').change(function() {
			if($(this).is(':checked')) {
				$('body').addClass('downfall');
				if (storage){
				localStorage.setItem('dfall', 'downfall');}
				} else {
				$('body').removeClass('downfall');
				if (storage){
				localStorage.setItem('dfall', '');}
			}
		}).change();
		
	if (storage){
		if (localStorage.wopt == 'wrapopt'){
			$('input[name="wrapbutton"]').prop('checked',true);
			}
	
		$('.optionswrap').addClass(localStorage.wopt);
	}
	
	$('input[name="wrapbutton"]').change(function() {
			if($(this).is(':checked')) {
				$('.optionswrap').addClass('wrapopt');
				if (storage){
				localStorage.setItem('wopt', 'wrapopt');}
				} else {
				$('.optionswrap').removeClass('wrapopt');
				if (storage){
				localStorage.setItem('wopt', '');}
				}
		}).change();
		
		
		
	function disablePicky(pickyid) {
		var pickyInputs = $(pickyid + ' input');
		for (i=0; i<pickyInputs.length; i++) {
				$(pickyInputs[i]).prop('disabled', true);
		}
	}
	
	function enablePicky(pickyid) {
		var pickyInputs = $(pickyid + ' input');
		for (i=0; i<pickyInputs.length; i++) {
				$(pickyInputs[i]).prop('disabled', false);
		}
	}
	
	$('#picky-matches input').change(function() {
		var pickySync = $('input[name="'+ $(this).attr('name') +'"]')
		if($(this).is(':checked')) {
			for (i=0; i<pickySync.length; i++) {
				$(pickySync[i]).prop('checked', true);}
		} else {
			for (i=0; i<pickySync.length; i++) {
				$(pickySync[i]).prop('checked', false);}
				}
	}).change();
	
	$('input[name="picky"]').change(function() {
		if($(this).is(':checked')) {
			$('#picky-matches').show();
			if (storage){
				if (localStorage.pstyle == 'text'){
					$('input[name="astext"]').prop('checked',true);
					}
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

	$('.menubutton').click(function() {
	$('#nav').toggleClass('is-open');
	});
	
	$('label.picky-header input').click(function() {
		var checks = $(this.parentNode.parentNode).next('div.picky-group').find('input');
		if (this.checked) {
			for (i=0; i<checks.length; i++) {
			var pickySync = $('input[name="'+ $(checks[i]).attr('name') +'"]')
			pickySync.attr('checked','checked');
			}
		}
		 else {
			for (i=0; i<checks.length; i++) {
			var pickySync = $('input[name="'+ $(checks[i]).attr('name') +'"]')
			pickySync.val([]);
			}
		}
	});

	if (storage){
		$('#container').addClass(localStorage.hdpi);
	}
	
	$('.hdpidisable').click(function() {
		$('#container').addClass('hdpi-disabled');
		if (storage){
		localStorage.setItem('hdpi', 'hdpi-disabled');
		}
	});
	
	$('.hdpienable').click(function() {
		$('#container').removeClass('hdpi-disabled');
		if (storage){
		localStorage.setItem('hdpi', '');
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

