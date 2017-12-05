$('.cls_eventtrack').on('click', function (e) {
	var element = $(this).closest('a');
	if(e.which) {
		MyGA.SendEvent('talenteconomy', element.data('category'), element.data('action'), element.data('label'));
	}
	return true;
});