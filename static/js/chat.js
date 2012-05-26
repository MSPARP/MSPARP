var PING_PERIOD=10;

function addAcronym(acronym,text) {
	if (acronym.length>0) {
		return acronym+": "+text;
	} else {
		return text;
	}
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
	var unconfirmed = [], ping_interval;

	function addLine(color, text){
		$('<div />').css('color', color).text(text).appendTo('#chat-log-inner');
		var chatlog = $('#chat-log');
		chatlog.scrollTop(chatlog[0].scrollHeight);
	}

	function updateChatPreview(){
		var preview = $('#chat-line').val();
		if (preview.substr(0,1)=='/') {
			preview = jQuery.trim(preview.substr(1));
		} else {
			preview = jQuery.trim(applyQuirks(preview));
		}
		$('#preview-text').text(preview);
		if (preview.length==0) {
			$('#hide-preview').hide();
		} else {
			$('#hide-preview').show();
		}
		$('#chat-log').css('bottom',$('#chat-hover').height()+'px');
		return preview.length!=0;
	}
	
	$('#chat-line').change(updateChatPreview).keyup(updateChatPreview).change();
	$('#preview-text').css('color', user_color);

	var previewHidden = false;
	$('#hide-preview').click(function() {
		if (previewHidden) {
			$('#preview-text').show();
			$(this).text("[hide]");
		} else {
			$('#preview-text').hide();
			$(this).text("[show]");
		}
		$('#chat-log').css('bottom',$('#chat-hover').height()+'px');
		previewHidden = !previewHidden;
		return false;
	});

	$('#chat-form').submit(function() {
		if (updateChatPreview()) {
			text = $('#preview-text').text();
			if (ping_interval) {
				window.clearTimeout(ping_interval);
			}
			$.post(post_url,{'line': text}); // todo: check for for error
			ping_interval = window.setTimeout(pingServer, PING_PERIOD*1000);
			$('#chat-line').val('');
		}
		return false;
	});

	function pingServer() {
		$.post(ping_url, {});
		ping_interval = window.setTimeout(pingServer, PING_PERIOD*1000);
	}

	function getMessages() {
		$.post(get_messages_url, {'after': latestNum}, function(data) {
			var messages = data.messages;
			for (var i=0; i<messages.length; i++) {
				var msg = messages[i];
				addLine('#'+msg['color'], msg['line']);
				latestNum = Math.max(latestNum, msg['id']);
			}
			if (typeof hidden!=="undefined" && document[hidden]==true) {
				// You can't change document.title here in Webkit. #googlehatesyou
				window.setTimeout(function() {
					document.title = "New message - "+ORIGINAL_TITLE;
				}, 50);
			}
		}, "json").complete(function() {
			window.setTimeout(getMessages, 50);
		});
	}

	if (typeof document.addEventListener!=="undefined" && typeof hidden!=="undefined") {
		document.addEventListener(visibilityChange, function() {
			if (document[hidden]==false) {
				document.title = ORIGINAL_TITLE;
			}
		}, false);
	}

	window.setTimeout(getMessages, 500);
	ping_interval=window.setTimeout(pingServer, PING_PERIOD*1000);

	$(window).unload(function() {
		$.ajax(quitURL, {'type': 'POST', 'async': false});
	});

});

