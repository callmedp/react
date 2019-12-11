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