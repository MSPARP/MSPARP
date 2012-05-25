$(document).ready(function() {

	function checkForMatch() {
		$.post(foundYetURL, {} ,function(data) {
			window.location.replace(chatURL.replace('-CHATID-', data['target']));
		}).complete(function() {
			window.setTimeout(checkForMatch, 500);
		});
	}

	window.setTimeout(checkForMatch, 500);
	$(window).unload(function(){
		$.ajax(quitURL, {'type': 'POST', 'async': false});
	});

});

