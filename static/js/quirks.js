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

	for (var i=0; i < user.character.replacements.length; i++) {
		var replacement = user.character.replacements[i];
		if (replacement[0].match(/\/.*?\//)) {
		 str1 = replacement[0]
		  str1 = str1.replace(/^\/(.*?)\//g, '$1');
		  str2 = replacement[1]
			  try {
		   var re = new RegExp(str1, "g"); 
		text = text.replace(re, str2);}
		catch (e) {console.log("A young person stands in their bedroom. They don't know Regexp.")}
		}
		else {
		 RegExp.quote = function(str) {
			 return str.replace(/([.?*+^$[\]\\(){}|-])/g, "\\$1");
		 };
		 str1 = replacement[0] 
		  str2 = replacement[1]
		var re = new RegExp(RegExp.quote(str1), "g"); 
		text = text.replace(re, str2);
		}
	}


	// Prefix
	if (user.character.quirk_prefix!='') {
		text = user.character.quirk_prefix+' '+text;
	}

	return text

}

function depunct(txt) {
	return txt.replace(/[.,?!']/g, '');
}

