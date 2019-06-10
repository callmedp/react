
$.validator.addMethod("numbercheck", function (value, element) {
    if( $('#id_country_code').val() == "91" && $('#id_cell_phone').val().length != 10){
         $('#enquire_form').removeAttr("disabled");
        return false;
    }
    else if($('#id_cell_phone').val().length >= 8 && $('#id_cell_phone').val().length <= 15){
        return true
    }
}, 'please enter valid mobile number');



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
            minlength: "please enter atleast 8 digit number",
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
              ga('create', 'UA-3537905-41', 'auto', {'name': 'a'});
              ga('a.send', 'pageview');
              ga('create', 'UA-3537905-41', 'auto');
              ga('send', 'pageview');

function gaEvent(event_cat,event_lab,event_action){
  ga('send', 'event', event_cat, event_action, event_lab);
 }

 function gaEventFunc(typeOfProduct,status){
    var event_cat='Form Interactions';

    var type = "" ;
    if(typeOfProduct == "1"){
        type= 'Skill Course Enquiry';
    }
    else{
        type= 'Skill Service Enquiry';
    }
    gaEvent(event_cat,status,type);
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
                number:{
                    required: true,
                    number: true,
                    indiaMobile: true,
                    minlength: 4,
                    maxlength: 15
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
                required: "Mobile Number is Mandatory",
                number: "Enter only number",
                indiaMobile: "Please enter 10 digits only",
                maxlength: "Please enter less than 16 digits",
                minlength: "Please enter atleast 4 digits"
            },
            msg:{
                required: "Message is Mandatory",
            }
        },
        highlight:function(element, errorClass) {
            $(element).parents('.form-group').addClass('error');
            $(element).siblings('.error-txt').removeClass('hide_error'); 
        },
        unhighlight:function(element, errorClass) {
            $(element).parents('.form-group').removeClass('error');
            $(element).siblings('.error-txt').addClass('hide_error');    
        },
        errorPlacement: function(error, element){
            $(element).siblings('.error-txt').html(error.text());
        } 
	});

	
	$('#id_query').click(function(){
	    var typeOfProduct = document.getElementsByName("lsource")[0].value;
		if ( $("#queryform").valid()) {
			var formData = $("#queryform").serialize();
			$.ajax({
	            url : "/lead/lead-management/",
	            type: "POST",
	            data : formData,
	            success: function(data, textStatus, jqXHR)
	            {
	             gaEventFunc(typeOfProduct,'success');
	            	alert('Your Query Submitted Successfully.');


                    window.location.reload();
	            },
	            error: function (jqXHR, textStatus, errorThrown)
	            {
	             gaEventFunc(typeOfProduct,'failure');
	                window.location.reload(); 
	            }
	        }); 
		}  
    });

	$('#enquire_form').click(function(){
	    var typeOfProduct = document.getElementsByName("lsource")[0].value;
		if ( $("#enquireform").valid()) {
			var formData = $("#enquireform").serialize();
			$.ajax({
	            url : "/lead/lead-management/",
	            type: "POST",
	            data : formData,
	            success: function(data, textStatus, jqXHR)
	            {
	             gaEventFunc(typeOfProduct,'success');
	            	alert('Your Query Submitted Successfully.');
                    window.location.reload();
	            },
	            error: function (jqXHR, textStatus, errorThrown)
	            {
	             gaEventFunc(typeOfProduct,'failure');
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

    $('.cls_scroll_tab').click(function(e){
        e.preventDefault();
        e.stopPropagation();
        var target = $(e.target);
        var navBarHeight = $('#id_nav').outerHeight() || 0;
        var stickyBarHeight = $(".cls_scroll_tab").outerHeight() || 0;
        if(target.hasClass('cls_tab_child')){
          $('html,body').animate({scrollTop : $(''+target.attr('href')).offset().top - navBarHeight - stickyBarHeight},1000);
        }
      });

});

