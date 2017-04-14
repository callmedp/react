$(function() {

    $(document).on('click', '#id_download_button', function(event) {
        event.preventDefault();
        var pop_up = $(this).attr('pop-up');
        var href = $(this).attr('href');
        console.log(pop_up);
        console.log(href);
        if (pop_up == "no") {
            $("#id_action").val(2);   // action for login -user
            $("#downloadpdf_form").submit();
            window.open(href, '_blank');
        }
        else {
            $('#id_download_model').modal("show");
        }
    });

    
    $(document).on('click', '#id_download', function(event) {
        event.preventDefault();
        $("#id_action").val(1);  //action on download button

        $("#downloadpdf_form").validate({

            rules:{
                name:{
                    required: true,
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
                    required: "Name is mandatory",
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
            },

        });
        if ($("#downloadpdf_form").valid()) {
            $("#downloadpdf_form").submit();
            $("#downloadpdf_form")[0].reset();
            $('#id_download_model').modal('toggle');
            var href = $('#id_download_button').attr('href');
            window.open(href, '_blank'); 
        }
    });

    $("#id_skip").click(function(){
        $("#id_action").val(0);   // action on skip button
        $("#downloadpdf_form").submit();
        $("#downloadpdf_form")[0].reset();
        var href = $('#id_download_button').attr('href');
        window.open(href, '_blank'); 
    });

	$("#cms_comment_form").validate({
		rules: {
		    message: "required",
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


    $(document).on('click', '#cms_share', function(event) {
        // console.log('click');
        // console.log($(this).attr('page-id'));
        $.ajax({
            url: "/ajax/page/cms-share/",
            type: 'GET',
            data: {
              page_id: $(this).attr('page-id'),
            },
            success: function(data) {
                console.log('success');
            }
        });
        
    });

});