$('.cls_eventtrack').on('click', function (e) {
	var element = $(this).closest('a');
	if(e.which) {
		MyGA.SendEvent('talenteconomy', element.data('category'), element.data('action'), element.data('label'));
	}
	return true;
});



var cmn = function(){}

cmn.prototype = {
	constructor : cmn,

	getParameterByName : function(name){
        name = name.replace(/[\[]/, "\\\[").replace(/[\]]/, "\\\]");
        var regex = new RegExp("[\\?&]" + name + "=([^&#]*)"),
            results = regex.exec(location.search);
        return results == null ? "" : decodeURIComponent(results[1].replace(/\+/g, " "));
    }
}

var commonJs = new cmn();