function applyQuirks(text) {

	// Case
	switch (user.character['case']) {
		case "lower":
			text = text.toLowerCase();
			break;
		case "upper":
			text = text.toUpperCase();
			break;
		case "title":
			text = text.toLowerCase().replace(/\b\w/g, function(t) { return t.toUpperCase(); });
			break;
		case "inverted":
	        var buffer = text.replace(/[a-zA-Z]/g, function(t) {
		        var out = t.toUpperCase();
		        if (out==t) {
			        return t.toLowerCase();
		        } else {
			        return out;
		        }
	        }).replace(/\bI\b/g, 'i').replace(/,\s*[A-Z]/g, function(t) { return t.toLowerCase(); });
	        text = buffer.charAt(0).toLowerCase()+buffer.substr(1);
			break;
		case "alternating":
	        var buffer = text.toLowerCase().split('');
	        for(var i=0; i<buffer.length; i+=2){
		        buffer[i] = buffer[i].toUpperCase();
	        }
	        text = buffer.join('');
			break;
	}

	// Replacements
	for (i=0; i<user.character.replacements.length; i++) {
		var replacement = user.character.replacements[i];
		// We're doing it like this because regular expressions pick up slashes
		// and stuff as control characters, and string replacement only picks up
		// the first occurence in Chrome.
		text = text.split(replacement[0]).join(replacement[1])
	}

	// Prefix
	if (user.character.quirk_prefix!='') {
		text = user.character.quirk_prefix+' '+text+' '+user.character.quirk_suffix;
	}

	return text

}

function depunct(txt) {
	return txt.replace(/[.,?!']/g, '');
}

