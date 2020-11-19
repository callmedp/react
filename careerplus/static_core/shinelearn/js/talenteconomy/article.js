(function($, Article){
	function init() {
	  	$(document).on('click', '#article_share', function(event) {
	        $.ajax({
	            url: "/ajax/article-share/",
	            type: 'GET',
	            data: {
	              article_slug: $(this).attr('article-slug'),
	            },
	            success: function(data) {
	                console.log('success');
	            }
	        });
    	});

    	$(document).on('click', '#load-more-te-tag', function(event) {
	        this.disabled = true;
	        var formData = $("#load-te-tag-form").serialize();
	        $.ajax({
	            url : "/talenteconomy/tags/loadmore-article/",
	            type: "GET",
	            data : formData,
	            dataType: 'html',
	            success: function(html, textStatus, jqXHR)
	            {
	                $("#talent_tag_load_more_id").remove();
	                $("#te-tag-article-container-id").append(html);
	            },
	            error: function (jqXHR, textStatus, errorThrown)
	            {
	                alert("Can't load more");
	            }
	         });   
        });


        $(document).on('click', '#load-more-art', function(event) {
	        this.disabled = true;
	        var formData = $("#load-te-art-form").serialize();
	        $.ajax({
	            url : "/talenteconomy/load-more-article/",
	            type: "GET",
	            data : formData,
	            dataType: 'json',
	            success: function(data, textStatus, jqXHR)
	            {

	                $("#talent_art_load_more").remove();
	                $("#list-container-id").append(data.article_list);
	            },
	            error: function (jqXHR, textStatus, errorThrown)
	            {
	                alert("Can't load more");
	            }
	         });
        });
	}

	Article.init = init;

}($, (window.Article = window.Article || {} )))


$.validator.addMethod("numbercheck", function (value, element) {
    if( $('#id_country_code').val() == "91" && $('#id_cell_phone').val().length != 10){
         $('#enquire_form').removeAttr("disabled");
        return false;
    }
    else if($('#id_cell_phone').val().length >= 8 && $('#id_cell_phone').val().length <= 15){
        return true
    }
}, 'Please enter valid mobile number');



$(function() {
  // Initialize form validation on the registration form.
  // It has the name attribute "registration"
  $("form[name='enq']").validate({
    // Specify validation rules
    rules: {
        number: {
            numbercheck : true,
        },
        msg: {
            maxlength:250,
        }
    },
    // Specify validation error messages
    messages: {
        number: {
                required: "Please enter your number",
                minlength: "Please enter atleast 8 digit number",
        },

        msg: {
            maxlength: "Message should be within 250 characters",
        },
    },
    // Make sure the form is submitted to the destination defined
    // in the "action" attribute of the form when valid
  });
});

    (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
              (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
              m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
              })(window,document,'script','https://www.google-analytics.com/analytics.js','ga');


function gaEvent(event_cat,event_lab,event_action){
  ga('send', 'event', event_cat, event_action, event_lab);
 }

function gaEventFunc(typeOfProduct,status){
    var event_cat='Form Interactions';
    gaEvent(event_cat,status,"Talent Enquiry");
 }


$('#enquire_form').click(function(event) {
    event.preventDefault();
    $('#enquire_form').attr("disabled", true);

    var $enquireform = $("#enquireform");
    var typeOfProduct = 'Talent Enquiry';
    var flag = $enquireform.valid();
    if (flag) {
        var formData = $enquireform.serialize();
        $.ajax({
            url: "/lead/lead-management/",
            type: "POST",
            data: formData,
            success: function(data, textStatus, jqXHR) {
                gaEventFunc(typeOfProduct,'success');
                pop('Your Query Submitted Successfully.');
                $('#enquireform')[0].reset();
                $('#enquire_form').removeAttr("disabled");
                $('#popup_subscribe').modal('toggle');
            },
            error: function(jqXHR, textStatus, errorThrown) {
                gaEventFunc(typeOfProduct,'failure');
                $('#enquire_form').removeAttr("disabled");
                pop('Something went wrong. Try again later.');
            }
        });
    }
});


function pop(param) {
    // Get the snackbar DIV
    var x = document.getElementById("snackbar");
    x.innerHTML=param;

    // Add the "show" class to DIV
    x.className = "show";

    // After 3 seconds, remove the show class from DIV
    setTimeout(function(){ x.className = x.className.replace("show", ""); }, 3500);
}

