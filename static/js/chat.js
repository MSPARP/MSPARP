var PING_PERIOD=10;

function addAcronym(acronym,text) {
	if (acronym.length>0) {
		return acronym+": "+text;
	} else {
		return text;
	}
}

var postURL = "/post";
var pingURL = "/ping";
var messagesURL = "/messages";
var saveURL = "/save";
var quitURL = "/bye";

var currentSidebar;

function setSidebar(sidebar) {
	if (currentSidebar) {
		$('#'+currentSidebar).hide();
	} else {
		$(document.body).addClass('withSidebar');
	}
	// Null to remove sidebar.
	if (sidebar) {
		$('#'+sidebar).show();
	} else {
		$(document.body).removeClass('withSidebar');
	}
	currentSidebar = sidebar;
}

/* Browser compatibility for visibilityChange */
var hidden, visibilityChange;
if (typeof document.hidden !== "undefined") {
	hidden = "hidden";
	visibilityChange = "visibilitychange";
} else if (typeof document.mozHidden !== "undefined") {
	hidden = "mozHidden";
	visibilityChange = "mozvisibilitychange";
} else if (typeof document.msHidden !== "undefined") {
	hidden = "msHidden";
	visibilityChange = "msvisibilitychange";
} else if (typeof document.webkitHidden !== "undefined") {
	hidden = "webkitHidden";
	visibilityChange = "webkitvisibilitychange";
}

$(document).ready(function() {

	var ORIGINAL_TITLE = document.title;
	var unconfirmed = [], pingInterval;
	var conversation = $('#conversation');

	function addLine(color, text){
		$('<p />').css('color', color).text(text).appendTo('#conversation');
		conversation.scrollTop(conversation[0].scrollHeight);
	}

	if (document.cookie=="") {

		addLine("#FF0000", "It seems you have cookies disabled. Unfortunately cookies are essential for MSPARP to work, so you'll need to either enable them or add an exception in order to use MSPARP.");

		$('#controls').submit(function() {
			return false;
		});

	} else {

		function updateChatPreview(){
			var preview = $('#textInput').val();
			if (preview.substr(0,1)=='/') {
				preview = jQuery.trim(preview.substr(1));
			} else {
				preview = applyQuirks(jQuery.trim(preview));
			}
			if (preview.length>0) {
				$('#preview').text(preview);
			} else {
				$('#preview').html('&nbsp;');
			}
			$('#conversation').css('bottom',($('#controls').height()+10)+'px');
			return preview.length!=0;
		}
	
		$('#textInput').change(updateChatPreview).keyup(updateChatPreview).change();
		$('#preview').css('color', '#'+user.color);

		var previewHidden = false;
		$('#hidePreview').click(function() {
			if (previewHidden) {
				$('#preview').show();
				$(this).text("[hide]");
			} else {
				$('#preview').hide();
				$(this).text("[show]");
			}
			$('#conversation').css('bottom',($('#controls').height()+10)+'px');
			previewHidden = !previewHidden;
			return false;
		});

		$('#controls').submit(function() {
			if (updateChatPreview()) {
				if ($('#textInput').val()!='') {
					if (pingInterval) {
						window.clearTimeout(pingInterval);
					}
					$.post(postURL,{'chat': chat, 'line': $('#preview').text()}); // todo: check for for error
					pingInterval = window.setTimeout(pingServer, PING_PERIOD*1000);
					$('#textInput').val('');
				}
			}
			return false;
		});

		function pingServer() {
			$.post(pingURL, {'chat': chat});
			pingInterval = window.setTimeout(pingServer, PING_PERIOD*1000);
		}

		function getMessages() {
			$.post(messagesURL, {'chat': chat, 'after': latestNum}, function(data) {
				var messages = data.messages;
				for (var i=0; i<messages.length; i++) {
					var msg = messages[i];
					addLine('#'+msg['color'], msg['line']);
					latestNum = Math.max(latestNum, msg['id']);
				}
				if (typeof data.online!=="undefined") {
					// Reload user lists.
					$("#online, #away").empty();
					for (var i=0; i<data.online.length; i++) {
						var currentUser = data.online[i];
						var listItem = $('<li />').css('color', '#'+currentUser.color).text(currentUser.name);
						listItem.appendTo('#'+currentUser.state);
					}
				}
				if (typeof hidden!=="undefined" && document[hidden]==true) {
					document.title = "New message - "+ORIGINAL_TITLE;
				}
			}, "json").complete(function() {
				window.setTimeout(getMessages, 50);
			});
		}

		if (typeof document.addEventListener!=="undefined" && typeof hidden!=="undefined") {
			document.addEventListener(visibilityChange, function() {
				if (document[hidden]==false) {
					// You can't change document.title here in Webkit. #googlehatesyou
					window.setTimeout(function() {
						document.title = ORIGINAL_TITLE;
					}, 50);
				}
			}, false);
		}

		window.setTimeout(getMessages, 500);
		pingInterval=window.setTimeout(pingServer, PING_PERIOD*1000);

		$('#settingsButton').click(function() {
			setSidebar('settings');
		});

		var userState = 'online';
		var newState;
		$('#awayButton').click(function() {
			if (userState=='away') {
				newState = 'online';
			} else {
				newState = 'away';
			}
			$.post(postURL, {'chat': chat, 'state': newState}, function(data) {
				userState = newState;
			});
		});

		$('#settings').submit(function() {
			// Trim everything first
			formInputs = $('#settings').find('input, select');
			for (i=0; i<formInputs.length; i++) {
				formInputs[i].value = jQuery.trim(formInputs[i].value)
			}
			if ($('input[name="name"]').val()=="") {
				alert("You can't chat with a blank name!");
			} else if ($('input[name="color"]').val().match(/^[0-9a-fA-F]{6}$/)==null) {
				alert("You entered an invalid hex code. Try using the color picker.");
			} else {
				var formData = $(this).serializeArray();
				formData.push({ name: 'chat', value: chat })
				$.post(saveURL, formData, function(data) {
					$('#preview').css('color', '#'+$('input[name="color"]').val());
					var formInputs = $('#settings').find('input, select');
					for (i=0; i<formInputs.length; i++) {
						if (formInputs[i].name!="quirk_from" && formInputs[i].name!="quirk_to") {
							user[formInputs[i].name] = formInputs[i].value;
						}
					}
					user.replacements = [];
					var replacementsFrom = $('#settings').find('input[name="quirk_from"]');
					var replacementsTo = $('#settings').find('input[name="quirk_to"]');
					for (i=0; i<replacementsFrom.length; i++) {
						if (replacementsFrom[i].value!="" && replacementsFrom[i].value!=replacementsTo[i].value) {
							user.replacements.push([replacementsFrom[i].value, replacementsTo[i].value])
						}
					}
					closeSettings();
				});
			}
			return false;
		});

		$('#settingsCancelButton').click(function() {
			closeSettings();
		});

		function closeSettings() {
			if ($(document.body).hasClass('mobile')) {
				setSidebar(null);
			} else {
				setSidebar('userList');
			}
		}

		// Activate mobile mode on small screens
		if (window.innerWidth<500) {
			$(document.body).addClass('mobile');
			$('.sidebar .close').click(function() {
				setSidebar(null);
			}).show();
			$('#userListButton').click(function() {
				setSidebar('userList');
			}).show();
		} else {
			setSidebar('userList');
		}

		window.onbeforeunload = function (e) { e.preventDefault(); return ""; }

		$(window).unload(function() {
			$.ajax(quitURL, {'type': 'POST', data: {'chat': chat}, 'async': false});
		});

	}

});

