
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

		var charbarkeys = Object.keys(chars);
		var charlistkeys = Object.keys(characters);


		for (var i = 0; i < charbarkeys.length; ++i) {
			try {
				var name = charbarkeys[i];
				var exists = characters[name].color;
				charstotal = charstotal + chars[charbarkeys[i]];
			} catch(e) {
				console.log("Error: " + e);
			}
		}
		for (var i = 0; i < charlistkeys.length; ++i) {
			var name = charlistkeys[i];
			if (chars[charlistkeys[i]] !== undefined) {
				var current = chars[charlistkeys[i]];
			} else {
				var current = 0;
			}
			var percent = (current / charstotal) * 100;
			try {
				uppername = name.replace(/^(\w)/g, function(a,x){ return a.replace(x,x.toUpperCase()); });
				uppername = uppername.replace(/\s(\w)/g, function(a,x){ return a.replace(x,x.toUpperCase()); });
				escapedname = name.replace(/[()/\s]/g, '');
				colorspans = colorspans + '<span class="slidein" id="character' + escapedname + '" style="width:' + percent + '%;background-color:#' + characters[name].color +  '" title="' + uppername + '"></span>';
				isonlinespans = isonlinespans + '<span class="isonlinechar" data-char="picky-' + name + '"><span class="charbut char' + escapedname + '" title="' + uppername+ '"></span> x '+ current + '</span>'
				$('.charbut.char' + escapedname).attr('title', uppername + ' (' + current + ' online)');
				$('.charbut.char' + escapedname + ' + .chartip').html(uppername + ' (' + current + ' online)');
			} catch(e) {
				console.log("Error: " + e);
			}
		}

		$('#charbar').html(colorspans);
		$('#isonlineblock').html(isonlinespans);
			$(function(){
			   function slide_in(){
				  $('#charbar span').removeClass("slidein");
			   };
			   window.setTimeout( slide_in, 100 ); 
			});

		if($('input[name="picky"]').is(':checked')) {
				$('#isonlineblock .isonlinechar').hide();
				$('#isonlineblock .iofiltered').show();
				var pickySync = $('#picky-icon input[class="butty"]')
				for (i=0; i<pickySync.length; i++) {
					if($(pickySync[i]).is(':checked')) {
						$('#isonlineblock span[data-char="' + $(pickySync[i]).attr('name') + '"]').show();
					}		
				}
			} else {
				$('#isonlineblock .isonlinechar').show();
				$('#isonlineblock .iofiltered').hide();
			}

	});
});