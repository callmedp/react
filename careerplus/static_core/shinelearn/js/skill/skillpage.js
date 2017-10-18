var cartScroller = function() {
      var item = $('.price-box'),
      height = item.height();
      $(window).scroll(function(){
          if(item.offset().top + height > $('.recomend-product-bg').offset().top - 50) {
            item.css({'visibility':'hidden'})
          } else {
            item.css({'visibility':'visible'});
          }
      });
    }
$(function() {
    $.validator.addMethod("indiaMobile", function(value, element) {
        var country_code = $("input[name=country_code]").val(); //$('#call_back_country_code-id').val();
        if(country_code == '91'){
            return value.length == 10;
        }
        return true;
    });
    $('#queryform').validate({
        rules:{
                name:{
                	required: true,
                    maxlength: 80,
                },
                mobile:{
                    required: true,
                    number: true,
                    indiaMobile: true,
                    minlength: 4,
                    maxlength: 15
                },
                message:{
                	required: true,
                	maxlength: 500,
                },
            },
        messages:{
            name:{
            	required: "Name is Mandatory.",
                maxlength: "Maximum 80 characters.",
            },
            mobile:{
                required: "Mobile Number is Mandatory",
                number: "Enter only number",
                indiaMobile: "Please enter 10 digits only",
                maxlength: "Please enter less than 16 digits",
                minlength: "Please enter atleast 4 digits"
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
	            url : "/shop/crm/lead/",
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
        $(".loadmore").remove();
        $.ajax({
            url: "/ajax/product/load-more/",
            data : {"page": page, "slug": $("#slug_id").val()},
            success: function(data, textStatus, jqXHR)
            {
                document.getElementById("page_id").value = Number(page)+1;
                // $('html,body').animate({scrollTop: $(".abc").offset().top},500);
                $("#product_list").append(data);       
                
            },
            error: function (jqXHR, textStatus, errorThrown)
            {
                // $("#prod_load_more").remove();
                alert("Can't load more comments.");
            }
        }); 
  
    });
    $(document).on('click', '#review_load_more', function(event) {
        var page = parseInt($("#page_id1").val());
        $(".loadreview").remove();
        $.ajax({
            url: "/ajax/review/load-more/",
            data : {"page": page, "slug": $("#slug_id1").val()},
            success: function(data, textStatus, jqXHR)
            {
                document.getElementById("page_id1").value = Number(page)+1;
                // $('html,body').animate({scrollTop: $("#review_load_more").offset().top},500);
                $("#review_list").append(data);       
                
            },
            error: function (jqXHR, textStatus, errorThrown)
            {
                // $("#revi_load_more").remove();
                alert("Can't load more comments.");
            }
        }); 
  
    });
    $('.about-course-links a').click(function(){
        $('.about-course-links a').removeClass('active');
        $(this).addClass('active');
      });
    cartScroller();

});
