var lastAlternatingLine = false;

function applyQuirks(text) {

	// Global quirking tags
		
		text = text.replace(/\[[cC](?:[aA][pP][sS])?\](.*?)\[\/[cC](?:[aA][pP][sS])?\]/g, '¦¤¤¤¤¦ $1 ¦¤¤¤¦¦');
		text = text.replace(/\[[wW](?:[hH][iI][sS][pP][eE][rR])?\](.*?)\[\/[wW](?:[hH][iI][sS][pP][eE][rR])?\]/g, '¦¤¤¤¦ $1 ¦¤¤¦¦');


	// Case
	switch (user.character['case']) {
		case "lower":
			text = text.replace(/([A-Z][a-z]+\b)/g, function(a,x){ return a.replace(x,x.toLowerCase()); });
			text = text.replace(/(\b)([A-Z]'?[A-Z]+)(\b)/g, '¥$2¥');
			text = text.toLowerCase();
			text = text.replace(/¥([\w|']+)¥/g, function(a,x){ return a.replace(x,x.toUpperCase()); });
			text = text.replace(/¥/g, '');
			text = text.replace(/([A-Z]\W[a-z]\W[A-Z])/g, function(a,x){ return a.replace(x,x.toUpperCase()); });
			text = text.replace(/^([a-z]\W[A-Z][A-Z]+)/g, function(a,x){ return a.replace(x,x.toUpperCase()); });
			text = text.replace(/[\.|!|\?]\W([a-z]\W[A-Z][A-Z]+)/g, function(a,x){ return a.replace(x,x.toUpperCase()); });
			text = text.replace(/([A-Z]'[a-z])/g, function(a,x){ return a.replace(x,x.toUpperCase()); });
			break;
		case "upper":
			text = text.toUpperCase();
			text = text.replace(/¦¤¤¤¦(.*?)¦¤¤¦¦/g, function(a,x){ return a.replace(x,x.toLowerCase()); });
			break;
		case "title":
			text = text.replace(/(^[a-z])/g, function(a,x){ return a.replace(x,x.toUpperCase()); });
			text = text.replace(/([\s|-][a-z])/g, function(a,x){ return a.replace(x,x.toUpperCase()); });
			break;
		case "inverted":
	        text = text.replace(/(?:^|¦¤¤¦¦)(.*?)(?:$|¦¤¤¤¦)/g, function(a,x){ return a.replace(x,x.toUpperCase()); });
			text = text.replace(/^(\w)/, function(a,x){ return a.replace(x,x.toLowerCase()); });
			text = text.replace(/([iI])\b/g, function(a,x){ return a.replace(x,x.toLowerCase()); });
			text = text.replace(/([,\.]\s?\w)/g, function(a,x){ return a.replace(x,x.toLowerCase()); });
			break;
		case "alternating":
	        text = text.toLowerCase();
			text = text.replace(/([\w\s]|[\w'\w])([\w'\w]|[\w\s])?/g, function(a,x){ return a.replace(x,x.toUpperCase()); });
			break;
		case "alt-lines":
			if (lastAlternatingLine) {
				text = text.toUpperCase();
			} else {
				text = text.toLowerCase();
			}
			break;
		case "proper":
			text = text.replace(/^(\w)/, function(a,x){ return a.replace(x,x.toUpperCase()); });
			text = text.replace(/(?:[^\.]|^[^\.])[!|\?|\.](\s\w)/g, function(a,x){ return a.replace(x,x.toUpperCase()); });
			text = text.replace(/[\s|^](i)['|\W|$]/g, function(a,x){ return a.replace(x,x.toUpperCase()); });
			break;
		case "first-caps":
			text = text.replace(/([A-Z][a-z]+\b)/g, function(a,x){ return a.replace(x,x.toLowerCase()); });
			text = text.replace(/(\b)([A-Z]'?[A-Z]+)(\b)/g, '¥$2¥');
			text = text.toLowerCase();
			text = text.replace(/¥([\w|']+)¥/g, function(a,x){ return a.replace(x,x.toUpperCase()); });
			text = text.replace(/¥/g, '');
			text = text.replace(/([A-Z]\W[a-z]\W[A-Z])/g, function(a,x){ return a.replace(x,x.toUpperCase()); });
			text = text.replace(/^([a-z]\W[A-Z][A-Z]+)/g, function(a,x){ return a.replace(x,x.toUpperCase()); });
			text = text.replace(/[\.|!|\?]\W([a-z]\W[A-Z][A-Z]+)/g, function(a,x){ return a.replace(x,x.toUpperCase()); });
			text = text.replace(/(?:^|\*)(\w)/, function(a,x){ return a.replace(x,x.toUpperCase()); });
			text = text.replace(/(?:[^\.]|^[^\.])[!|\?|\.](\s\w)/g, function(a,x){ return a.replace(x,x.toUpperCase()); });
			break;
		
	}
	
	// Replacements

	for (var i=0; i < user.character.replacements.length; i++) {
		var replacement = user.character.replacements[i];
		if (replacement[1] == " ") {
		replacement[1] = ""
		}
		if (replacement[0].match(/\/.*?\//)) {
		str1 = replacement[0]
		str1 = str1.replace(/^\/(.*?)\//g, '$1');
		str2 = replacement[1]
		try {
		   var re = new RegExp(str1, "g"); 
		}
		catch (e) {console.log("A young person stands in their bedroom. They don't know Regexp.")}
		if (str2 == "$L")
				{
					try {
					text = text.replace(re, function(a,x){ return a.replace(x,x.toLowerCase()); });
					}
					catch (e) {
					text = text.replace(re, function(a){ return a.replace(a,a.toLowerCase()); });
					}
				}
		else if (str2 == "$U")
				{
					try {
					text = text.replace(re, function(a,x){ return a.replace(x,x.toUpperCase()); });
					}
					catch (e) {
					text = text.replace(re, function(a){ return a.replace(a,a.toUpperCase()); });
					}
				}
		else {
			  text = text.replace(re, str2);
		}}
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

	// Cleanup global quirking tags
	
	text = text.replace(/¦¤¤¤¤¦(.*?)¦¤¤¤¦¦/g, function(a,x){ return a.replace(x,x.toUpperCase()); });
	text = text.replace(/(¦¤¤¤¤?¦\s)/g, '');
	text = text.replace(/(\s¦¤¤¤?¦¦)/g, '');

	// Prefix
	if (user.character.quirk_prefix!='' || user.character.quirk_suffix!='') {
		text = user.character.quirk_prefix+' '+text+' '+user.character.quirk_suffix;
	}

	return text

}

function depunct(txt) {
	return txt.replace(/[.,?!']/g, '');
}

