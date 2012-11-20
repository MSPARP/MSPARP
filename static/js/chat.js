$(document).ready(function() {

	var SEARCH_PERIOD = 1;
	var PING_PERIOD = 10;

	var SEARCH_URL = "/search";
	var SEARCH_QUIT_URL = "/stop_search";
	var POST_URL = "/chat_ajax/post";
	var PING_URL = "/chat_ajax/ping";
	var MESSAGES_URL = "/chat_ajax/messages";
	var SAVE_URL = "/chat_ajax/save";
	var QUIT_URL = "/chat_ajax/quit";

	var pingInterval;
	var chatState;
	var userState;
	var newState;
	var currentSidebar;
	var previewHidden = false;

	var actionListUser = null;
	var highlightUser = null;

	var ORIGINAL_TITLE = document.title;
	var conversation = $('#conversation');

	$('input, select, button').attr('disabled', 'disabled');

	if (document.cookie=="") {

		$('<p>').css('color', '#FF0000').text('It seems you have cookies disabled. Unfortunately cookies are essential for MSPARP to work, so you\'ll need to either enable them or add an exception in order to use MSPARP.').appendTo(conversation);

		$('#controls').submit(function() {
			return false;
		});

	} else {

		// Search

		function runSearch() {
			$.post(SEARCH_URL, {}, function(data) {
				chat = data['target'];
				chaturl = '/chat/'+chat;
				if (typeof window.history.replaceState!="undefined") {
					window.history.replaceState('', '', chaturl);
					startChat();
				} else {
					window.location.replace(chaturl);
				}
			}).complete(function() {
				if (chatState=='search') {
					window.setTimeout(runSearch, 1000);
				}
			});
		}

		// Chatting

		function addLine(msg){
			if (msg.counter==-1) {
				msgClass = 'system';
			} else {
				msgClass = 'user'+msg.counter;
			}
			var mp = $('<p>').addClass(msgClass).css('color', '#'+msg.color).text(msg.line).appendTo('#conversation');
			if (highlightUser==msg.counter) {
				mp.addClass('highlight');
			}
			conversation.scrollTop(conversation[0].scrollHeight);
		}

		function startChat() {
			chatState = 'chat';
			userState = 'online';
			document.title = 'Chat - '+ORIGINAL_TITLE;
			conversation.removeClass('search');
			$('input, select, button').removeAttr('disabled');
			$('#preview').css('color', '#'+user.character.color);
			$('#logLink').attr('href', '/chat/'+chat+'/log');
			closeSettings();
			getMessages();
			pingInterval = window.setTimeout(pingServer, PING_PERIOD*1000);
		}

		function getMessages() {
			var messageData = {'chat': chat, 'after': latestNum};
			$.post(MESSAGES_URL, messageData, function(data) {
				var messages = data.messages;
				for (var i=0; i<messages.length; i++) {
					addLine(messages[i]);
					latestNum = Math.max(latestNum, messages[i]['id']);
				}
				if (typeof data.online!=="undefined") {
					// Reload user lists.
					actionListUser = null;
					$("#online > li, #idle > li").appendTo(holdingList);
					generateUserlist(data.online, $('#online')[0]);
					generateUserlist(data.idle, $('#idle')[0]);
				}
				if (typeof hidden!=="undefined" && document[hidden]==true) {
					document.title = "New message - "+ORIGINAL_TITLE;
				}
			}, "json").complete(function() {
				if (chatState=='chat') {
					window.setTimeout(getMessages, 50);
				} else if (chatType=='match') {
					$('#save').appendTo(conversation);
					$('#save input').removeAttr('disabled');
				}
			});
		}

		function pingServer() {
			$.post(PING_URL, {'chat': chat});
			pingInterval = window.setTimeout(pingServer, PING_PERIOD*1000);
		}

		function disconnect() {
			if (confirm('Are you sure you want to disconnect?')) {
				chatState = 'inactive';
				if (pingInterval) {
					window.clearTimeout(pingInterval);
				}
				$.ajax(QUIT_URL, {'type': 'POST', data: {'chat': chat}});
				$('input[name="chat"]').val(chat);
				chat = null;
				$('input, select, button').attr('disabled', 'disabled');
				$('#userList > ul').empty();
				setSidebar(null);
				document.title = ORIGINAL_TITLE;
			}
		}

		// Sidebars

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

		function closeSettings() {
			if ($(document.body).hasClass('mobile')) {
				setSidebar(null);
			} else {
				setSidebar('userList');
			}
		}

		// User list
		var holdingList = $("<ul />");

		function generateUserlist(users, listElement) {
			for (var i=0; i<users.length; i++) {
				var currentUser = users[i];
				if (currentUser.meta.counter==user.meta.counter) {
					// Set self-related things here.
					user.meta.group = currentUser.meta.group;
				}
				// Get or create a list item.
				var listItem = $(holdingList).find('#user'+currentUser.meta.counter);
				if (listItem.length==0) {
					var listItem = $('<li />').attr('id', 'user'+currentUser.meta.counter);
					listItem.click(showActionList);
				}
				// Name is a reserved word; this may or may not break stuff but whatever.
				listItem.css('color', '#'+currentUser.character.color).text(currentUser.character['name']);
				listItem.removeClass('mod').removeClass('silent');
				if (currentUser.meta.group=='mod') {
					listItem.addClass('mod').attr('title', 'Moderator');
				} else if (currentUser.meta.group=='silent') {
					listItem.addClass('silent').attr('title', 'Silent');
				}
				if (currentUser.meta.counter==user.meta.counter) {
					listItem.addClass('self').append(' (you)');
				}
				listItem.removeData().data(currentUser).appendTo(listElement);
			}
		}

		function showActionList() {
			$('#actionList').remove();
			// Hide if already shown.
			if (this!=actionListUser) {
				var actionList = $('<ul />').attr('id', 'actionList');
				var userData = $(this).data();
				if (userData.meta.counter==highlightUser) {
					$('<li />').text('Clear highlight').appendTo(actionList).click(function() { highlightPosts(null); });
				} else {
					$('<li />').text('Highlight posts').appendTo(actionList).click(function() { highlightPosts(userData.meta.counter); });
				}
				if (user.meta.group=='mod') {
					if (userData.meta.group=='mod') {
						$('<li />').text('Unmod').appendTo(actionList).click(function() { setUserGroup('user', userData.meta.counter); });
					} else {
						$('<li />').text('Mod').appendTo(actionList).click(function() { setUserGroup('mod', userData.meta.counter); });
					}
					if (userData.meta.group=='silent') {
						$('<li />').text('Unsilence').appendTo(actionList).click(function() { setUserGroup('user', userData.meta.counter); });
					} else {
						$('<li />').text('Silence').appendTo(actionList).click(function() { setUserGroup('silent', userData.meta.counter); });
					}
				}
				$(actionList).appendTo(this);
				actionListUser = this;
			} else {
				actionListUser = null;
			}
		}

		function setUserGroup(group, counter) {
			if (counter!=user.meta.counter || confirm('You are about to unmod yourself. Are you sure you want to do this?')) {
				$.post(POST_URL,{'chat': chat, 'set_group': group, 'counter': counter});
			}
		}

		function highlightPosts(counter) {
			$('.highlight').removeClass('highlight');
			if (counter!=null) {
				$('.user'+counter).addClass('highlight');
			}
			highlightUser = counter;
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

		// Event listeners

		function updateChatPreview(){
			var textPreview = $('#textInput').val();
			if (textPreview.substr(0,1)=='/') {
				textPreview = jQuery.trim(textPreview.substr(1));
			} else {
				textPreview = applyQuirks(jQuery.trim(textPreview));
			}
			if (textPreview.length>0) {
				$('#preview').text(textPreview);
			} else {
				$('#preview').html('&nbsp;');
			}
			$('#conversation').css('bottom',($('#controls').height()+10)+'px');
			return textPreview.length!=0;
		}
		$('#textInput').change(updateChatPreview).keyup(updateChatPreview).change();

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

		if (typeof document.addEventListener!=="undefined" && typeof hidden!=="undefined") {
			document.addEventListener(visibilityChange, function() {
				if (chatState=='chat' && document[hidden]==false) {
					if (navigator.userAgent.indexOf('Chrome')!=-1) {
						// You can't change document.title here in Chrome. #googlehatesyou
						window.setTimeout(function() {
							document.title = 'Chat - '+ORIGINAL_TITLE;
						}, 200);
					} else {
						document.title = 'Chat - '+ORIGINAL_TITLE;
					}
				}
			}, false);
		}

		$('#controls').submit(function() {
			if (updateChatPreview()) {
				if ($('#textInput').val()!='') {
					if (pingInterval) {
						window.clearTimeout(pingInterval);

					}
					$.post(POST_URL,{'chat': chat, 'line': $('#preview').text()}); // todo: check for for error
					pingInterval = window.setTimeout(pingServer, PING_PERIOD*1000);
					$('#textInput').val('');
					updateChatPreview();
				}
			}
			return false;
		});

		$('#disconnectButton').click(disconnect);

		$('#idleButton').click(function() {
			if (userState=='idle') {
				newState = 'online';
			} else {
				newState = 'idle';
			}
			$.post(POST_URL, {'chat': chat, 'state': newState}, function(data) {
				userState = newState;
			});
		});

		$('#settingsButton').click(function() {
			setSidebar('settings');
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
				$.post(SAVE_URL, formData, function(data) {
					$('#preview').css('color', '#'+$('input[name="color"]').val());
					var formInputs = $('#settings').find('input, select');
					for (i=0; i<formInputs.length; i++) {
						if (formInputs[i].name!="quirk_from" && formInputs[i].name!="quirk_to") {
							user.character[formInputs[i].name] = formInputs[i].value;
						}
					}
					user.character.replacements = [];
					var replacementsFrom = $('#settings').find('input[name="quirk_from"]');
					var replacementsTo = $('#settings').find('input[name="quirk_to"]');
					for (i=0; i<replacementsFrom.length; i++) {
						if (replacementsFrom[i].value!="" && replacementsFrom[i].value!=replacementsTo[i].value) {
							user.character.replacements.push([replacementsFrom[i].value, replacementsTo[i].value])
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

		// Activate mobile mode on small screens
		if (navigator.userAgent.indexOf('Android')!=-1 || navigator.userAgent.indexOf('iPhone')!=-1 || window.innerWidth<=500) {
			$(document.body).addClass('mobile');
			$('.sidebar .close').click(function() {
				setSidebar(null);
			}).show();
			$('#userListButton').click(function() {
				setSidebar('userList');
			}).show();
		}

		window.onbeforeunload = function (e) {
			if (chatState=='chat') {
				if (typeof e!="undefined") {
					e.preventDefault();
				}
				return "";
			}
		}

		$(window).unload(function() {
			if (chatState=='chat') {
				$.ajax(QUIT_URL, {'type': 'POST', data: {'chat': chat}, 'async': false});
			} else if (chatState=='search') {
				$.ajax(SEARCH_QUIT_URL, {'type': 'POST', 'async': false});
			}
		});

		// Initialisation

		if (chat==null) {
			chatState = 'search';
			document.title = 'Searching - '+ORIGINAL_TITLE;
			conversation.addClass('search');
			runSearch();
		} else {
			startChat();
		}

	}

});

