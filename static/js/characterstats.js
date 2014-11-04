
// shuffle for character bar

// function shuffle(o){ 
//     for(var j, x, i = o.length; i; j = parseInt(Math.random() * i), x = o[--i], o[i] = o[j], o[j] = x);
//     return o;
// };
//charbarkeys = shuffle(charbarkeys);

// calculate totals for percentages, then set up charbar
// check whether character is set up in characters, else don't add

$(document).ready(function() {

	var charstotal = 0;
	var colorspans = "";
	var isonlinespans = '<h1> > Clients connected <span class="iofiltered">(filtered)</span></h1><br>';

	$.get("/charinfo.json", function(chars) {
		for (var i = 0; i < charbarkeys.length; ++i) {
			try {
				var name = charbarkeys[i];
				var exists = characters[name].color;
				charstotal = charstotal + chars[charbarkeys[i]];
			} catch(e) {}
		}
		for (var i = 0; i < charbarkeys.length; ++i) {
			var current = chars[charbarkeys[i]];
			var name = charbarkeys[i];
			var percent = (current / charstotal) * 100;
			try {
				uppername = name.replace(/^(\w)/, function(a,x){ return a.replace(x,x.toUpperCase()); });
				uppername = uppername.replace(/\s(\w)/, function(a,x){ return a.replace(x,x.toUpperCase()); });
				escapedname = name.replace(/[\(\)\/\s]/, '');
				colorspans = colorspans + '<span class="slidein" id="character' + escapedname + '" style="width:' + percent + '%; opacity:0.8;background-color:#' + characters[name].color +  '" title="' + uppername + '"></span>';
				isonlinespans = isonlinespans + '<span class="isonlinechar" data-char="picky-' + name + '"><span class="charbut char' + escapedname + '" title="' + uppername+ '"></span> x '+ current + '</span>'
				} catch(e)
			{}
		}

		$('#charbar').html(colorspans);
		$('#isonlineblock').html(isonlinespans);
			$(function(){
			   function slide_in(){
				  $('#charbar span').removeClass("slidein");
			   };
			   window.setTimeout( slide_in, 100 ); 
			});
	});
});