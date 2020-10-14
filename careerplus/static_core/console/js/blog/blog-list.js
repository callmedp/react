$(function(){
	$('#id_filter').click(function(){
	    $('#filter-article-form').submit();
	});
});


function sortByDate(){
	let form = $('#filter-article-form')[0] ;
	if (sorting == '1'){
		$('#sortAngle').removeClass();
		$('#sortAngle').addClass('fa fa-angle-up ');
	}
	else{
		$('#sortAngle').removeClass();
		$('#sortAngle').addClass('fa fa-angle-down');
	}

	$('<input>').attr({
		type: 'hidden',
		id: 'sortdate',
		name: 'sortdate',
		value: sorting
	}).appendTo(form);
	$('#filter-article-form').submit();
}

function sortByLastModified(){
	let form = $('#filter-article-form')[0] ;
	if (sorting_lm == '3'){
		$('#sortAngle_lm').removeClass();
		$('#sortAngle_lm').addClass('fa fa-angle-up ');
	}
	else{
		$('#sortAngle_lm').removeClass();
		$('#sortAngle_lm').addClass('fa fa-angle-down');
	}

	$('<input>').attr({
		type: 'hidden',
		id: 'sortdate',
		name: 'sortdate',
		value: '-1'
	}).appendTo(form);
	$('<input>').attr({
		type: 'hidden',
		id: 'sortdate_lm',
		name: 'sortdate_lm',
		value: sorting_lm
	}).appendTo(form);
	$('#filter-article-form').submit();
}