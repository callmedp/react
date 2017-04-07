$(function() {

    /*$("#downloadpdf_form").validate({
        rules:{
                name:{
                    maxlength: 100,
                },
                email:{
                    required:false,
                    maxlength: 100,
                },
                mobile_number:{
                    required:true,
                    number: true,
                    minlength: 5,
                    maxlength: 15,                    
                },
                term_condition:{
                    required: true,
                },

            },
        messages:{
                name:{
                    maxlength: "Maximum 100 characters."
                },
                email:{
                    maxlength: "At most 100 characters"
                },
                mobile_number:{
                    required:"Mobile Number is Mandatory",
                    number:"Enter only number",
                    maxlength: "Please enter below 15 digits",
                    minlength: "Please enter atleast 5 digits"
                },
                
            },
        highlight:function(element, errorClass) {
            $(element).siblings('.error').removeClass('hide_error');
        },
        unhighlight:function(element, errorClass) {
            $(element).siblings('.error').addClass('hide_error');    
        },
        errorPlacement: function(error, element){
        
            $(element).siblings('.error').html(error.text());
        } 
    });*/

    $("#id_download").click(function(){
        $("#id_action").val(1);
        $("#downloadpdf_form").submit();
        $('#id_download_model').modal('toggle');
    });

    $("#id_skip").click(function(){
        $("#id_action").val(0);
        $("#downloadpdf_form").submit();
    });

	$("#cms_comment_form").validate({
		rules: {
		    message: "required",
		},
		highlight:function(element, errorClass) {
		        $(element).siblings('.error').remove();
		},
		unhighlight:function(element, errorClass) {
		        $(element).siblings('.error').remove();    
		},
		errorPlacement: function(error, element){
		        $(element).siblings('.error').html(error.text());
		} 
    });

    $('#callback_form').validate({
        rules:{
                name:{
                	required: true,
                    maxlength: 80,
                },
                mobile_number:{
                    required: true,
                    number: true,
                    minlength: 5,
                    maxlength: 15,                        
                },
                message_box:{
                	required: true,
                	maxlength: 500,
                },
            },
        messages:{
            name:{
            	required: "Name is Mandatory.",
                maxlength: "Maximum 80 characters.",
            },
            mobile_number:{
                required:"Mobile Number is Mandatory",
                number:"Enter only number",
                maxlength: "Please enter below 15 digits",
                minlength: "Please enter atleast 5 digits",
            },
            
        },
        highlight:function(element, errorClass) {
            $(element).siblings('.error').removeClass('hide_error'); 
        },
        unhighlight:function(element, errorClass) {
            $(element).siblings('.error').addClass('hide_error');    
        },
        errorPlacement: function(error, element){
            $(element).siblings('.error').html(error.text());
        } 
	});

	
	$('#id_callback').click(function(){
		if ( $("#callback_form").valid()) {
			var formData = $("#callback_form").serialize();
			$.ajax({
	            url : "/cms/lead-management/",
	            type: "POST",
	            data : formData,
	            success: function(data, textStatus, jqXHR)
	            {
	            	alert('Your Query Submitted Successfully.');
                    window.location.reload();
	            },
	            error: function (jqXHR, textStatus, errorThrown)
	            {
	                window.location.reload(); 
	            }
	        }); 
		}  
    });

    $(document).on('click', '#comment_load_more', function(event) {
        var formData = $("#loadform").serialize();
        console.log(formData);
        $.ajax({
            url : "/ajax/page/load-more/",
            type: "POST",
            data : formData,
            success: function(data, textStatus, jqXHR)
            {
                data = JSON.parse(data);
                $("#total_comment").remove();
                $("#load_more").remove();
                $("#page_comment").append(data.comment_list);
            },
            error: function (jqXHR, textStatus, errorThrown)
            {
                alert("Can't load more comments.");
            }
        }); 
  
    });

});