function applyQuirks(text) {

	// Case
	switch (user.case) {
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
	for (i=0; i<user.replacements.length; i++) {
		var replacement = user.replacements[i];
		// Chrome doesn't do global string replacing so we need to loop this.
		while (text.indexOf(replacement[0])!=-1) {
			text = text.replace(replacement[0], replacement[1], 'g');
		}
	}

	// Prefix
	if (user.quirk_prefix!='') {
		text = user.quirk_prefix+' '+text;
	}

	return text

}

function depunct(txt) {
	return txt.replace(/[.,?!']/g, '');
}

