function applyQuirks(text) {

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

	// Prefix
	if (user.quirk_prefix!='') {
		text = user.quirk_prefix+' '+text;
	}

	return text

}

function replaceLetter(txt, from, to) {
	return txt.replace(new RegExp(from, 'g'), to);
}

function twoQuirk(txt) {
	return txt.replace(/too/g, 'two');
}

function l33t(txt) {
	return txt.replace(/[Aa]/g,'4').replace(/[iI]/g,'1').replace(/[eE]/g,'3');
}

function depunct(txt) {
	return txt.replace(/[.,?!']/g, '');
}

function hornedEmoticons(txt) {
	return txt.replace(/[;:]-?[()DO]/, function(arg) { return '}'+arg; });
}

