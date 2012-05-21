var PING_PERIOD=10;
function addAcronym(acronym,text){
	if(acronym.length>0){
		return acronym+": "+text;
	}else{
		return text;
	}
}
$(document).ready(function(){
	var unconfirmed=[],ping_interval;
	function addLine(color,text){
		$('<div />').css('color',color).text(text).appendTo('#chat-log-inner');
		var chatlog=$('#chat-log');
		chatlog.scrollTop(chatlog[0].scrollHeight);
	}
	function updateChatPreview(){
		var preview=$('#chat-line').val();
		if(preview.substr(0,1)=='/'){
			preview=jQuery.trim(preview.substr(1));
		}else{
			preview=jQuery.trim(applyQuirks(preview));
		}

		$('#preview-text').text(preview);
		if(preview.length==0){
			$('#hide-preview').hide();
		}else{
			$('#hide-preview').show();
		}
		$('#chat-log').css('bottom',$('#chat-hover').height()+'px');
		return preview.length!=0;
	}
	
	$('#chat-line').change(updateChatPreview).keyup(updateChatPreview).change();
	$('#preview-text').css('color',user_color);

	$('#hide-preview').click(function(){
		$('#chat-preview').hide();
		return false;
	});
	$('#chat-form').submit(function(){
		if(updateChatPreview()){
			text=$('#preview-text').text();
			if(ping_interval){
				window.clearTimeout(ping_interval);
			}
			$.post(post_url,{'line':text}); // todo: check for for error
			ping_interval=window.setTimeout(pingServer,PING_PERIOD*1000);
			$('#chat-line').val('');
		}
		return false;
	});
	function pingServer(){
		$.post(ping_url,{});
		ping_interval=window.setTimeout(pingServer,PING_PERIOD*1000);
	}
	function getMessages(){
		$.getJSON(get_messages_url+'?after='+latestNum,function(data){
			var messages=data.messages;
			for(var i=0;i<messages.length;i++){
				var msg=messages[i];
				addLine('#'+msg['color'],msg['line']);	
				latestNum=Math.max(latestNum,msg['id']);
			}
		}).complete(function(){
			window.setTimeout(getMessages,50);
		});
	}
	window.setTimeout(getMessages,500);
	ping_interval=window.setTimeout(pingServer,PING_PERIOD*1000);
	$(window).unload(function(){
		$.ajax(quitURL,{'async':false});
	});
});
