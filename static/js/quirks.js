function upper(txt) {
	return txt.toUpperCase();
}

function lower(txt) {
	return txt.toLowerCase();
}

function prefix(txt, what) {
	return what+txt;
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

function titleCase(txt) {
	return txt.toLowerCase().replace(/\b\w/g, upper);
}

function depunct(txt) {
	return txt.replace(/[.,?!']/g, '');
}

function alternatingCaps(txt) {
	var buffer = txt.toLowerCase().split('');
	for(var i=0; i<buffer.length; i+=2){
		buffer[i] = buffer[i].toUpperCase();
	}
	return buffer.join('');
}

function inverseCaps(txt) {
	var buffer = txt.replace(/[a-zA-Z]/g, function(arg) {
		var out = arg.toUpperCase();
		if (out==arg) {
			return arg.toLowerCase();
		} else {
			return out;
		}
	}).replace(/\bI\b/g, 'i').replace(/,\s*[A-Z]/g, lower).replace(/\./g, ',');
	return buffer.charAt(0).toLowerCase()+buffer.substr(1);
}

function hornedEmoticons(txt) {
	return txt.replace(/[;:]-?[()DO]/, function(arg) { return '}'+arg; });
}

