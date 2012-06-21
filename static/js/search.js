$(document).ready(function() {

	if (document.cookie=="") {

		$('#progress').text("It seems you have cookies disabled. Unfortunately cookies are essential for MSPARP to work, so you'll need to either enable them or add an exception in order to use MSPARP.");

	} else {

		function checkForMatch() {
			$.post(foundYetURL, {} ,function(data) {
				window.location.replace(chatURL.replace('-CHATID-', data['target']));
			}).complete(function() {
				window.setTimeout(checkForMatch, 1000);
			});
		}

		window.setTimeout(checkForMatch, 500);
		$(window).unload(function(){
			$.ajax(quitURL, {'type': 'POST', 'async': false});
		});

	}

});

