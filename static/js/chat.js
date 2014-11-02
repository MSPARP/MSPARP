function linkify(inputText) {
    var replacedText, replacePattern1, replacePattern2;
    if (inputText.indexOf("[img]") !=-1) {
	return inputText;
    }
    //URLs starting with http://, https://, or ftp://
    replacePattern1 = /]?=?https?:\/\/[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)/gim;
    replacedText = inputText.replace(replacePattern1,
    function(m) {
        if (m.substr(0,1) == "=" || m.substr(0,1) == "]") {
            return m;
        } else {
            return "[url]"+m+"[/url]";
        }
    });

    //Change email addresses to mailto:: links.
    replacePattern2 = /(\w+@[a-zA-Z_]+?\.[a-zA-Z]{2,6})/gim;
    replacedText = replacedText.replace(replacePattern2, '[email]$1[/email]');

    return replacedText;
}

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

	var CHAT_FLAGS = ['autosilence'];

	var MOD_GROUPS = ['globalmod', 'mod', 'mod2', 'mod3']
	var GROUP_RANKS = { 'globalmod': 6, 'mod': 5, 'mod2': 4, 'mod3': 3, 'user': 2, 'silent': 1 }
	var GROUP_DESCRIPTIONS = {
		'globalmod': { title: 'God tier moderator', description: 'MSPARP staff.' },
		'mod': { title: 'Professional Wet Blanket', description: 'can silence, kick and ban other users.' },
		'mod2': { title: 'Bum\'s Rusher', description: 'can silence and kick other users.' },
		'mod3': { title: 'Amateur Gavel-Slinger', description: 'can silence other users.' },
		'user': { title: '', description: '' },
		'silent': { title: 'Silenced', description: '' },
	};

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

	var globals = [];
	var bbset = 1;

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
	
	if (storage){
		$('body').addClass(localStorage.hdpi);
	}
	
	$("meta[name=viewport]").attr('content', 'width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=0');
	
	if (storage){
		if (localStorage.creppy == 'creppy'){
				$('head').append('<link rel="stylesheet" id="creppyid" href="/static/css/mscreppy_chat.css?41031" type="text/css" />');
				$('.hidecreppy').show();
			}
			else {
				$('.hidecreppy').hide();
			}
		
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
	
    $('#conversation p').each(function() {
        if (bbset == 1) {
            line = bbEncode(linkify($(this).html()));
            $(this).html(line);
        } else {
            if ($(this).attr('class') == 'eMessages') {
                line = bbEncode(linkify($(this).html()));
            } else {
                line = bbEncode(linkify(bbRemove($(this).html())));
            }
            $(this).html(line);
        }
    });

    if ($('#topic').length != 0) {
        if (bbset == 1) {
            text = bbEncode(htmlEncode(linkify($('#topic').html())));
            $('#topic').html(text);
        } else {
            text = bbEncode(htmlEncode(linkify(bbRemove($('#topic').html()))));
            $('#topic').html(text);
        }
    }

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
            var von = conversation.scrollTop()+conversation.height()+24;
            var don = conversation[0].scrollHeight;
            var lon = don-von;
            if (lon <= 30){
                flip = 1;
            } else {
                flip = 0;
            }
			if (msg.counter==-1) {
				msgClass = 'system';
			} else {
				msgClass = 'user'+msg.counter;
			}

			if ($.inArray(msg.counter, globals) !== -1 || msg.counter == -123){
				message = bbEncode(htmlEncode(linkify(msg.line)), true);
			} else {
				message = bbEncode(htmlEncode(linkify(msg.line)), false);
			}

			var mp = $('<p>').addClass(msgClass).attr('title',msgClass).css('color', '#'+msg.color).html(message).appendTo('#conversation');

			if (highlightUser==msg.counter) {
				mp.addClass('highlight');
			}
			
			if ($('#userList #user'+msg.counter).hasClass('globalmod')) {
				mp.addClass('staffmessage').prepend('<span class="spiroicon"></span>');
			}
			
			if (flip == 1) {
				conversation.scrollTop(conversation[0].scrollHeight);
				flip = 0;
			}
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
				if (typeof data.exit!=='undefined') {
					if (data.exit=='kick') {
						clearChat();
						addLine({ counter: -1, color: '000000', line: 'You have been kicked from this chat. Please think long and hard about your behaviour before rejoining.' });
					} else if (data.exit=='ban') {
						latestNum = -1;
						chat = 'theoubliette'
						$('#userList h1')[0].innerHTML = 'theoubliette';
						$('#conversation').empty();
					}
					return true;
				}
				var messages = data.messages;
				for (var i=0; i<messages.length; i++) {
					addLine(messages[i]);
					latestNum = Math.max(latestNum, messages[i]['id']);
				}
				if (typeof data.counter!=="undefined") {
					user.meta.counter = data.counter;
				}
				if (typeof data.online!=="undefined") {
					// Reload user lists.
					actionListUser = null;
					$("#online > li").appendTo(holdingList);
					generateUserlist(data.online, $('#online')[0]);
				}
				if (typeof data.meta!=='undefined') {
					// Reload chat metadata.
					var chat_meta = data.meta;
					for (i=0; i<CHAT_FLAGS.length; i++) {
						if (typeof data.meta[CHAT_FLAGS[i]]!=='undefined') {
							$('#'+CHAT_FLAGS[i]).attr('checked', 'checked');
							$('#'+CHAT_FLAGS[i]+'Result').show();
						} else {
							$('#'+CHAT_FLAGS[i]).removeAttr('checked');
							$('#'+CHAT_FLAGS[i]+'Result').hide();
						}
					}
					if (typeof data.meta.topic!=='undefined') {
						$('#topic').html(bbEncode(htmlEncode(linkify(data.meta.topic))));
					} else {
						$('#topic').text('');
					}
				}
				if (messages.length>0 && typeof hidden!=="undefined" && document[hidden]==true) {
					document.title = "New message - "+ORIGINAL_TITLE;
				}
			}, "json").complete(function() {
				if (chatState=='chat') {
					window.setTimeout(getMessages, 1000);
				} else if (chat_meta.type=='unsaved' || chat_meta.type=='saved') {
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
				$.ajax(QUIT_URL, {'type': 'POST', data: {'chat': chat}});
				clearChat();
				if (chat_meta.type=='unsaved' || chat_meta.type=='saved') {
					$("#disconnectButton").unbind( "click" );
					$("#disconnectButton").removeAttr("disabled");
					$("#disconnectButton").text("New chat" );
					$('#disconnectButton').click(reconnect);
				}
			}
		}

		function reconnect() {
			window.location.replace(document.location.origin + "/chat");
		}

		function clearChat() {
			chatState = 'inactive';
			if (pingInterval) {
				window.clearTimeout(pingInterval);
			}
			$('input[name="chat"]').val(chat);
			chat = null;
			$('input, select, button').attr('disabled', 'disabled');
			$('#userList > ul').empty();
			setSidebar(null);
			document.title = ORIGINAL_TITLE;
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
				// Get or create a list item.
				var listItem = $(holdingList).find('#user'+currentUser.meta.counter);
				if (listItem.length==0) {
					var listItem = $('<li />').attr('id', 'user'+currentUser.meta.counter);
					listItem.click(showActionList);
				}
				// Name is a reserved word; this may or may not break stuff but whatever.
				listItem.css('color', '#'+currentUser.character.color).text(currentUser.character['name']);
				listItem.removeClass().addClass(currentUser.meta.group);
				if (currentUser.meta.group == 'globalmod'){
					globals.push(currentUser.meta.counter);
				}
				var currentGroup = GROUP_DESCRIPTIONS[currentUser.meta.group]
				var userTitle = currentGroup.title
				if (currentGroup.description!='') {
					userTitle += ' - '+GROUP_DESCRIPTIONS[currentUser.meta.group].description
				}
				listItem.attr('title', userTitle);
				if (currentUser.meta.counter==user.meta.counter) {
					// Set self-related things here.
					if (currentUser.meta.group=='silent') {
						// Just been made silent.
						$('#textInput, #controls button[type="submit"]').attr('disabled', 'disabled');
					} else if (user.meta.group=='silent' && currentUser.meta.group!='silent') {
						// No longer silent.
						$('input, select, button').removeAttr('disabled');
					}
					user.meta.group = currentUser.meta.group;
					if ($.inArray(user.meta.group, MOD_GROUPS)==-1) {
						$(document.body).removeClass('modPowers');
					} else {
						$(document.body).addClass('modPowers');
					}
					listItem.addClass('self').append(' (you)');
				}

				// Character icons + Globalmod icons
				if (currentUser.meta.group == 'globalmod') {
					listItem.prepend($("<span/>").addClass('globalicon'));
				} else {
					filteredchar = currentUser.character['character'].replace(/[()/\s]/g, '').toLowerCase();
					listItem.prepend($("<span/>").addClass("charbut").addClass('char'+filteredchar));
				}

				// Extra info for globalmods
				if (user.meta.group=="globalmod") {
					listItem.append("<span class=\"userID\">user"+currentUser.meta.counter+"</span>"); 
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
				// Mod actions. You can only do these if you're (a) a mod, and (b) higher than the person you're doing it to.
				if ($.inArray(user.meta.group, MOD_GROUPS)!=-1 && GROUP_RANKS[user.meta.group]>=GROUP_RANKS[userData.meta.group]) {
					for (var i=1; i<MOD_GROUPS.length; i++) {
						if (userData.meta.group!=MOD_GROUPS[i] && GROUP_RANKS[user.meta.group]>=GROUP_RANKS[MOD_GROUPS[i]]) {
							var command = $('<li />').text('Make '+GROUP_DESCRIPTIONS[MOD_GROUPS[i]].title);
							command.appendTo(actionList);
							command.data({ group: MOD_GROUPS[i] });
							command.click(setUserGroup);
						}
					}
					if ($.inArray(userData.meta.group, MOD_GROUPS)!=-1) {
						$('<li />').text('Unmod').appendTo(actionList).data({ group: 'user' }).click(setUserGroup);
					}
					if (userData.meta.group=='silent') {
						$('<li />').text('Unsilence').appendTo(actionList).data({ group: 'user' }).click(setUserGroup);
					} else {
						$('<li />').text('Silence').appendTo(actionList).data({ group: 'silent' }).click(setUserGroup);
					}
					$('<li />').text('Kick').appendTo(actionList).data({ action: 'kick' }).click(userAction);
					$('<li />').text('IP Ban').appendTo(actionList).data({ action: 'ip_ban' }).click(userAction);
				}
				// Global mod actions. You can only do these if you're a global mod.
                if (user.meta.group=="globalmod") {
                    $('<li />').text('Look up IP').appendTo(actionList).click(ipLookup);
                }
				$(actionList).appendTo(this);
				actionListUser = this;
			} else {
				actionListUser = null;
			}
		}

		function setUserGroup() {
			var counter = $(this).parent().parent().data().meta.counter;
			var group = $(this).data().group;
			if (counter!=user.meta.counter || confirm('You are about to unmod yourself. Are you sure you want to do this?')) {
				$.post(POST_URL,{'chat': chat, 'set_group': group, 'counter': counter});
			}
		}

		function userAction() {
			var counter = $(this).parent().parent().data().meta.counter;
			var action = $(this).data().action;
			var actionData = {'chat': chat, 'user_action': action, 'counter': counter};
			if (action=='ip_ban') {
				var reason = prompt('Please enter a reason for this ban (spamming, not following rules, etc.):');
				if (reason==null) {
					return;
				} else if (reason!="") {
					actionData['reason'] = reason;
				}
			}
			if (counter!=user.meta.counter || confirm('You are about to kick and/or ban yourself. Are you sure you want to do this?')) {
				$.post(POST_URL, actionData);
			}
		}

        function ipLookup() {
            var counter = $(this).parent().parent().data().meta.counter;
            $.post("/chat_ajax/ip_lookup", { 'chat': chat, 'counter': counter, }, function(ip) {
                var msg = {counter: "-1", color: "000000", line: "[SYSTEM] user" +counter+ "'s IP: " + ip}
                addLine(msg);
            });
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
					 if (user.character['case']=='alt-lines') {
						lastAlternatingLine = !lastAlternatingLine;
					}
					$('#textInput').val('');
					updateChatPreview();
				}
			}
			return false;
		});

		$('#disconnectButton').click(disconnect);

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

		$('#metaOptions input').click(function() {
			var data = {'chat': chat, 'meta_change': ''}
			// Convert to integer then string.
			data[this.id] = +this.checked+'';
			$.post(POST_URL, data);
		});

		$('#topicButton').click(function() {
			if ($.inArray(user.meta.group, MOD_GROUPS)!=-1) {
				var new_topic = prompt('Please enter a new topic for the chat:');
				if (new_topic!=null) {
					$.post(POST_URL,{'chat': chat, 'topic': new_topic.substr(0, 1500)});
				}
			}
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

	$('#conversation').scrollTop($('#conversation')[0].scrollHeight);
	$("#textInput").focus();

    $('.spoiler').live('click', function() {
        if ($(this).css('opacity') == '0') {
            $(this).css('opacity','1');
        } else {
            $(this).css('opacity','0');
        }
    });

});

