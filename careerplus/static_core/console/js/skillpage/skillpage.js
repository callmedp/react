$(function() {
    $('#queryform').validate({
        rules:{
                name:{
                	required: true,
                    maxlength: 80,
                },
                number:{
                    required: true,
                    number: true,
                    minlength: 5,
                    maxlength: 15,                        
                },
                msg:{
                	required: true,
                	maxlength: 500,
                },
            },
        messages:{
            name:{
            	required: "Name is Mandatory.",
                maxlength: "Maximum 80 characters.",
            },
            number:{
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

	
	$('#id_query').click(function(){
		if ( $("#queryform").valid()) {
			var formData = $("#queryform").serialize();
			$.ajax({
	            url : "/lead/lead-management/",
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

    $(document).on('click', '#product_load_more', function(event) {
        var page = parseInt($("#page_id").val());
        $.ajax({
            url: "/ajax/product/load-more/",
            data : {"page": page, "slug": $("#slug_id").val(), "pk":("#pk_id").val()},
            success: function(data, textStatus, jqXHR)
            {
                document.getElementById("page_id").value = Number(page)+1;
                $('html,body').animate({scrollTop: $("#product_load_more").offset().top},500);
                $("#product_list").append(data);       
                
            },
            error: function (jqXHR, textStatus, errorThrown)
            {
                $("#prod_load_more").remove();
                alert("Can't load more comments.");
            }
        }); 
  
    });
    $(document).on('click', '#review_load_more', function(event) {
        alert("sdsaddas");
        var page = parseInt($("#page_id").val());
        $.ajax({
            url: "/ajax/review/load-more/",
            data : {"page": page, "slug": $("#slug_id").val()},
            success: function(data, textStatus, jqXHR)
            {
                document.getElementById("page_id").value = Number(page)+1;
                $('html,body').animate({scrollTop: $("#review_load_more").offset().top},500);
                $("#product_list").append(data);       
                
            },
            error: function (jqXHR, textStatus, errorThrown)
            {
                $("#prod_load_more").remove();
                alert("Can't load more comments.");
            }
        }); 
  
    });
});
