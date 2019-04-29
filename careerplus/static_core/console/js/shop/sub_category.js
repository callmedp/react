function slugify(string) {
  return string
    .toString()
    .trim()
    .toLowerCase()
    .replace(/\s+/g, "-")
    .replace(/[^\w\-]+/g, "")
    .replace(/\-\-+/g, "-")
    .replace(/^-+/, "-")
    .replace(/-+$/, "-")
    .replace(' ','-')
    .replace('-','-');
}



    function changeSlug(){
	let category_selected = $('#id_category option:selected').text().trim();
	let location = $('#id_location option:selected').text().trim();
	if (category_selected != "" && location != "" && category_selected != undefined && location !=undefined)
	{
	    let new_slug = category_selected.toLowerCase() + "-"+ location.toLowerCase();
	    new_slug = slugify(new_slug)
	    $('#id_slug').val(new_slug);
	}
	}

	function updateHeading(){
	let category_selected = $('#id_category option:selected').text().trim();
	let location = $('#id_location option:selected').text().trim();
	if (category_selected != "" && location != "" && category_selected != undefined && location !=undefined)
	{
	    let new_heading = category_selected + " courses in "+ location;
	    $('#id_heading').val(new_heading);
	}
	}

	function createTitle()
    {
    let category_selected = $('#id_category option:selected').text().trim();
	let location = $('#id_location option:selected').text().trim();
	if (category_selected != "" && location != "" && category_selected != undefined && location !=undefined)
	{
	    let new_heading = category_selected +" Courses in " + location +" - Fee structure, Practical Training - Shine Learning";
	    $('#id_title').val(new_heading);
	}
    }

    function createDescription(){

     let category_selected = $('#id_category option:selected').text().trim();
	let location = $('#id_location option:selected').text().trim();
	if (category_selected != "" && location != "" && category_selected != undefined && location !=undefined)
	{
	 let new_description= category_selected +' courses in '+ location+' - Are you looking for a '+ category_selected +" courses in " + location +" - Check complete fee structure, training programme from top institutes.";
	    $('#id_meta_desc').val(new_description);
	}
    }

    function funCalls()
    {
    changeSlug();
    updateHeading();
    createTitle();
    createDescription();

    }

    $('#id_category').change(funCalls);
	$('#id_location').change(funCalls);

$(document).ready(function(){
$('#id_products_mapped').select2();
$('#id_products_mapped').removeAttr('required');

});
