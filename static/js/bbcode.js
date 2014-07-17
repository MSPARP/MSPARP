function htmlEncode(value){
  //create a in-memory div, set it's inner text(which jQuery automatically encodes)
  //then grab the encoded contents back out.  The div never exists on the page.
  return $('<div/>').text(value).html();
}

function bbEncode(S, isglobal) {

    if (S.indexOf('[') < 0 || S.indexOf(']') < 0) return S;

    if(typeof(isglobal)==='undefined') isglobal = false;
    
    S = S.replace(/\[(font|color|bgcolor|tshadow|bshadow)=([^\]]+)]/gi, function(one,two,three) {
        if (isglobal == true){
            three = three;
        } else {
            three = three.replace(/["';{}]/gi, "");
        }
        return "["+two+"="+three+"]";
    });
    

    var BR = true;
    while (BR == true) {
        BR = false;
        S = S.replace(/\[br]\s?\[br]/gi, function(w) {
            if (w) { BR = true; }
            return '[br]';
        });
    }

    function X(p, f) {return new RegExp(p, f)}
    function D(s) {return rD.exec(s)}
    function R(s) {return s.replace(rB, P);}
    function A(s, p) {for (var i in p) s = s.replace(X(i, 'g'), p[i]); return s;}

    function P($0, $1, $2, $3) {
        if ($3 && $3.indexOf('[') > -1) $3 = R($3);
        var linkint = ($2||$3).trim();
        linkint = linkint.replace(/javascript/gi, "");
        linkint = linkint.replace(/["';{}]/g, "");
        $2 = linkint;
        switch ($1) {
            case 'url':case 'email': return '<a target="_blank" '+ L[$1] + $2 +'">'+ $3 +'</a>';
            case 'pad': return '<span class="padded">'+ $3 +'</span>';
            case 'spoiler': return '<span class="spoil"><span class="spoiler">'+ $3 +'</span></span>';
            case 'b':case 'i':case 'u':case 's':case 'sup':case 'sub': return '<'+ $1 +'>'+ $3 +'</'+ $1 +'>';
        }
        return '['+ $1 + ']'+ $3 +'[/'+ $1 +']';
    }

    var C = {code: [{'\\[': '&#91;', ']': '&#93;'}, '', '']};
    var rB = X('\\[([a-z][a-z0-9]*)(?:=([^\\]]+))?]((?:.|[\r\n])*?)\\[/\\1]', 'g'), rD = X('^(\\d+)x(\\d+)$');
    var L = {url: 'href="', email: 'href="mailto: '};
    if (isglobal==true){
        var F = {font: 'font-family:$1', color: 'color:$1', bgcolor: 'background-color:$1', tshadow: 'line-height:20px;text-shadow:$1', bshadow: 'line-height:20px;box-shadow:$1'};
    } else {
        var F = {font: 'font-family:$1', color: 'color:$1', bgcolor: 'background-color:$1', tshadow: '', bshadow: ''};
    }
    var I = {}, B = {};

    for (var i in C) I['\\[('+ i +')]((?:.|[\r\n])*?)\\[/\\1]'] = function($0, $1, $2) {return C[$1][1] + A($2, C[$1][0]) + C[$1][2]};
    for (var i in F) {B['\\['+ i +'=([^\\]]+)]'] = '<span style="'+ F[i] +'">'; B['\\[/'+ i +']'] = '</span>';}
    B['\\[(br)]'] = '<$1 />';

    var result = R(A(A(S, I), B));
    return result;
}

function bbRemove(S) {
    if (S.indexOf('[') < 0 || S.indexOf(']') < 0) return S;

    function X(p, f) {return new RegExp(p, f)}
    function D(s) {return rD.exec(s)}
    function R(s) {return s.replace(rB, P)}
    function A(s, p) {for (var i in p) s = s.replace(X(i, 'g'), p[i]); return s;}

    function P($0, $1, $2, $3) {
        if ($3 && $3.indexOf('[') > -1) $3 = R($3);
        switch ($1) {
            case 'pad': return '$3';
        }
        return '['+ $1 + ']'+ $3 +'[/'+ $1 +']';
    }

    var rB = X('\\[([a-z][a-z0-9]*)(?:=([^\\]]+))?]((?:.|[\r\n])*?)\\[/\\1]', 'g'), rD = X('^(\\d+)x(\\d+)$');
    var F = {font: 'font-family:$1', color: 'color:$1', bgcolor: 'background-color:$1', tshadow: 'text-shadow:$1', bshadow: 'box-shadow:$1'};
    var I = {}, B = {};

    for (var i in F) {B['\\['+ i +'=([^\\]]+)]'] = ''; B['\\[/'+ i +']'] = '';}
    var result = R(A(A(S, I), B));
    return result;
}
