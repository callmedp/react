
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
        var page = parseInt($("#prod_page_id").val());
        var pCtg = parseInt($("#slug_id").val());
        var prod_detail = '';
        $('#product_load_more').remove();
        $('#prod_loader').show();
        $.ajax({
            url: 'api/v1/Certification-load-more/', //change the name
            type: "GET",
            data : {"page": page, "page_size": 1, "pCtg" : pCtg, "pTF" : 16 ,"pTF_include" : false,  "fl" : "name,pCert,pURL,pImg,pNm,pNJ,pHd,pStar,pARx,pPin,pPfin,pPvn"},
            dataType: 'json',
            success: function(data){
                for(d in data.results){
                    prod_detail += `<li class="box-panel" itemprop="itemListElement" itemscope itemtype="http://schema.org/ListItem"><a title="${data.results[d].name}" href="${data.results[d].pURL}"><div class="media"><div class="media-left"><img aria-label="${data.results[d].name}" class="media-object" src="${data.results[d].pImg}" alt="${data.results[d].pNm}" height="130px" width="130px"></div><div class="media-body"><div class="certification-jobs-box">`;
                    if("true" in data.results[d].pCert){
                        prod_detail += `<span class="certification-jobs"><figure class="certification-icon"></figure> Certification</span>`;
                    }
                    if(data.results[d].pNJ){
                        prod_detail +=  `<span class="certification-jobs"><figure class="jobs-icon"></figure> <span class="jobs-number">${data.results[d].pNJ}</span> jobs available</span>`;
                    }
                    prod_detail += `</div>
                    <h3 class="listing-heading">${ data.results[d].pHd != "" ? data.results[d].pHd : data.results[d].pNm }</h3>
                  <div class="rating-review-box">`;
                    for(star in data.results[d].pStar){
                        if(star == '*'){ prod_detail += `<figure class="full-star"></figure>`}
                        else if(star == '+'){ prod_detail += `<figure class="half-star"></figure>`}
                        else { prod_detail += `<figure class="blank-star"></figure>`}
                    }
                    var pARx = parseInt(data.results[d].pARx).toFixed(1);
                    var pPin = parseInt(data.results[d].pPin).toFixed(0);
                    var pPfin = parseInt(data.results[d].pPfin).toFixed(0);
                    prod_detail += `<strong>${pARx}/5</strong> 
                    </div>
                    <div class="providers">
                       Providers
                       <span>${data.results[d].pPvn}</span>
                    </div>
                  <div class="pricing-box">
                    Starting at <strong>Rs. ${pPin}/-</strong>`;
                    if(pPfin){
                        prod_detail += `<strike>Rs. ${pPfin}/-</strike> <span class="discount">${data.results[d].discount}% OFF</span>`
                    }
                    prod_detail += `
                  </div>
                </div>
                </div>
                </a>
                </li> `   
                }
                page = page + 1; 
                var img = document.getElementById('prod_loader').innerHTML;
                if(data.next != null){
                    prod_detail += `
                    <div id = "prod_loader" style ="display:none">${img}
                            </div>
                    <div id="product_load_more">
                    <a href="javascript:void(0)" 
                                 class="load-more loadmore">
                                Load more</a> 
                                <div id="prod_load_more">
                                    <input type="hidden" name="page" 
                                    value="${page}" id="prod_page_id">
                                    <input type="hidden" name="pCtg" value="${pCtg}" 
                                    id="slug_id">
                                </div></div>`
                }
                $('#prod_loader').remove();

                var prod_list = document.getElementById('product_list');
                prod_list.innerHTML += prod_detail;
       
                
            },
            error: function (jqXHR, textStatus, errorThrown)
            {
                alert("Can't load more comments.");
            }
        }); 

  
    });

    $(document).on('click', '#certification_load_more', function(event) {
        var page = parseInt($("#cert_page_id").val());
        var pCtg = parseInt($("#Ctg_id").val());
        var cert_detail = '';
        $('#certification_load_more').remove();
        $('#cert_loader').show();
        $.ajax({
            url: '/api/v1/Certification-load-more/',
            type: "GET",
            data : {"page": page, "page_size": 5, "pCtg" : pCtg, "pTF" : 16, "pTF_include" : true, "fl" : "name,pCert,pURL,pImg,pNm,pNJ,pHd,pStar,pARx,pPin,pPfin,pPvn,pAsft,pPOP"},
            dataType: 'json',
            success: function(data){
                for(d in data.results){
                    cert_detail =  cert_detail + `<li class="box-panel"><a title="${data.results[d].name}" href="${data.results[d].pURL}"><div class="media"><div class="media-left"><img aria-label="${data.results[d].name}" class="media-object" src="${data.results[d].pImg}" alt="${data.results[d].pNm}" height="130px" width="130px"></div><div class="media-body"><div class="certification-jobs-box">`;
                    var cert_list = data.results[d].pCert; 
                    for(var i=0; i<cert_list.length ; i++){
                        if(cert_list[i] == 'true'){
                            cert_detail += `<span class="certification-jobs"><figure class="certification-icon"></figure>Certification</span>`; break;
                        }
                    }
                    if(Number(data.results[d].pNJ) > 0){
                        cert_detail +=  `<span class="certification-jobs"><figure class="jobs-icon"></figure> <span class="jobs-number">${data.results[d].pNJ}</span> jobs available</span>`;
                    }
                    cert_detail += `</div>
                                        <h3 class="listing-heading">${ data.results[d].pHd != "" ? data.results[d].pHd : data.results[d].pNm }</h3>
                                        <div class="rating-review-box">`;
                                            for(star in data.results[d].pStar){
                                                if(data.results[d].pStar[star] == '*'){ cert_detail += `<figure class="full-star"></figure>`}
                                                else if(data.results[d].pStar[star] == '+'){ cert_detail += `<figure class="half-star"></figure>`}
                                                else { cert_detail += `<figure class="blank-star"></figure>`}
                                            }
                                            var pARx = Number(Number(data.results[d].pARx).toFixed(1));
                                            var pPin = Number(Number(data.results[d].pPin).toFixed(0));
                                            var pPfin = Number(Number(data.results[d].pPfin).toFixed(0));
                                            cert_detail += `<strong>${pARx}/5</strong> 
                                        </div>
                                            <div class="providers">
                                               Providers
                                               <span>${data.results[d].pPvn}</span>
                                            </div>
                                          <div class="pricing-box">
                                          <div class="pull-left">
                                            Starting at <strong>Rs. ${pPin}/-</strong>`;
                                            if(pPfin){
                                                cert_detail += `<strike>Rs. ${pPfin}/-</strike> <span class="discount">${data.results[d].discount}% OFF</span>`;
                                            }
                                            cert_detail += `</div>
                                            <ul class="pull-right pricing-box__lists">`;
                                            var pAsft = JSON.parse(data.results[d].pAsft[0]);
                                            if(pAsft["number_of_questions"]){
                                                cert_detail +=`<li>No. of questions : <span>${pAsft["number_of_questions"]}</span></li>`
                                            }
                                            if(pAsft["test_duration"]){
                                                cert_detail += `<li>Duration: <span>${pAsft["test_duration"]}mins</span></li>`
                                            }
                                            cert_detail+=`</ul>
                                          </div>
                                        </div>
                                        </div>
                                        </a>
                                        </li> `
                }
                var img = document.getElementById('cert_loader').innerHTML;
                // 
                page = page + 1;
                if(data.next != null){
                    cert_detail += `
                     <div id = "cert_loader" style ="display:none">${img}</div>
                    <div id="certification_load_more">
                        <a href="javascript:void(0)" id="certification_load_more" class="load-more loadmore">Load more</a> 
                        <div id="cert_load_more">
                            <input type="hidden" name="page" 
                            value="${page}" id="cert_page_id">
                            <input type="hidden" name="pCtg" value="${pCtg}" 
                            id="Ctg_id">
                        </div>
                    </div>`
                }

                $('#cert_loader').remove();

                var cert_list = document.getElementById('certification_list');
                cert_list.innerHTML += cert_detail;
      
                
            },
            error: function (jqXHR, textStatus, errorThrown)
            {

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

