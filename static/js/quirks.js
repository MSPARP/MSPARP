var lastAlternatingLine = false;

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
			text = text.toLowerCase().replace(/(^|[^\w-'])\w/g, function(t) { return t.toUpperCase(); });
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
        case "alt-lines":
            if (lastAlternatingLine) {
                text = text.toUpperCase();
            } else {
                text = text.toLowerCase();
            }
	}

	// Replacements
	for (i=0; i<user.character.replacements.length; i++) {
		var replacement = user.character.replacements[i];
		// We're doing it like this because regular expressions pick up slashes
		// and stuff as control characters, and string replacement only picks up
		// the first occurence in Chrome.
		text = text.split(replacement[0]).join(replacement[1])
	}

	// Regexes
	var i=0;
	var rlen = user.character.regexes.length;
	while(i < rlen) {
		var regex = user.character.regexes[i++];
		text = text.replace(parse_regex(regex[0]), regex[1]);
		i++;
	}

	// Prefix
	if (user.character.quirk_prefix!='') {
		text = user.character.quirk_prefix+text;
	}

	// Suffix
	if (user.character.quirk_suffix!='') {
		text = text+user.character.quirk_suffix;
	}

	return text

}
	
function parse_regex(str) {
	var flags = 'g';
    if(str.charAt(0) == '/') {
	    var pattern = str.substr(1, str.lastIndexOf('/')-1);
	    flags = str.substr(str.lastIndexOf('/')+1);
	    return RegExp(pattern, flags);
	} else {
		return RegExp(str, flags);
	}
}

function depunct(txt) {
	return txt.replace(/[.,?!']/g, '');
}

