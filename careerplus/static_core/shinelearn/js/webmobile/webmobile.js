$('.cls_eventtrack').on('click', function () {
	MyGA.SendEvent('talenteconomy', $(this).data('category'), $(this).data('action'), $(this).data('label'));
	return true;
});