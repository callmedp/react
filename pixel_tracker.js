function createCookie(name,value,days){
    var date = new Date();
    date.setTime(date.getTime()+(days*24*60*60*1000));
    var expires = "; expires="+date.toGMTString();
    document.cookie = name+"="+value+expires+"; path=/";
}

function readCookie(name) {
	var nameEQ = name + "=";
	var ca = document.cookie.split(';');
	for(var i=0;i < ca.length;i++) {
		var c = ca[i];
		while (c.charAt(0)==' ') c = c.substring(1,c.length);
		if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
	}
	return null;
}
var createCookieUrls = [createcookiurls];
var readCookieUrls = [readcookieurls];
var url_to_hit=pixel_url;
current_url = window.location.origin + window.location.pathname
if(createCookieUrls.includes(current_url)){
    const urlParams = new URLSearchParams(window.location.search);
    udata = urlParams.get('udata');
    if(udata){
	    createCookie('udata',udata, no_of_days)
    }
}
if(readCookieUrls.includes(current_url)){
	var udata = readCookie('udata')
    if(udata){
    	var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function() {
    	   console.log('pixel hit')
        };
        
        url_to_hit += '?udata=' + udata
        xhttp.open("GET", url_to_hit, true);
        xhttp.send();
    }
}
