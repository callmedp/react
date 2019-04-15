$(document).on("click","a[href^='tel']",function(){
    MyGA.SendEvent('CallbackRequested', 'Call Interactions', 'General Enquiry', 'success');
});

/* 
1) .cls_search is the search form class 
2) q is the element where user writes
3) this function is binding typeahead for every form it finds with class .cls_search
4) it also binding jquery validate for form validation */
$(document).ready(function($) {
  
    var categorySkillSource = new Bloodhound({
        datumTokenizer: Bloodhound.tokenizers.whitespace,
        queryTokenizer: Bloodhound.tokenizers.whitespace,
        local:Object.keys(categoryUrlSet)
      });
      var productSource = new Bloodhound({
        datumTokenizer: Bloodhound.tokenizers.whitespace,
        queryTokenizer: Bloodhound.tokenizers.whitespace,
        local: Object.keys(productUrlSet)
      });

      $(".search").find("input").typeahead({
        highlight: false
      },
      {
        name: 'category_skill',
        source: categorySkillSource,
        limit: 3,
        templates: {
          header: '<h3>Skills</h3>'
        }
      },
      {
        name: 'products',
        source: productSource,
        limit: 3,
        templates: {
          header: '<h3>Products</h3>'
        }
      }).bind('typeahead:select', function(ev, suggestion) {
        if (categoryUrlSet[suggestion]) 
          window.location.href = `${categoryUrlSet[suggestion]}`;
        else 
          window.location.href = `${productUrlSet[suggestion]}`;
      });
      $("#id_q").typeahead({
        highlight: false
      },
      {
        name: 'category_skill',
        source: categorySkillSource,
        limit: 3,
        templates: {
          header: '<h3>Skills</h3>'
        }
      },
      {
        name: 'products',
        source: productSource,
        limit: 3,
        templates: {
          header: '<h3>Products</h3>'
        }
      }).bind('typeahead:select', function(ev, suggestion) {
        if (categoryUrlSet[suggestion]) 
          window.location.href = `${categoryUrlSet[suggestion]}`;
        else 
          window.location.href = `${productUrlSet[suggestion]}`;
      });
      
    $('.cls_search').each(function(index,item){
        $(item).validate({
            rules : {
                'q':'required'
            },
            messages:{
                'q':'Please enter a query'
            },
            submitHandler:function(form){
                var qVal = encodeURI($(form).find('input[name=q]').val());
                location.href = '/search/results/?q='+qVal;
            },
            errorPlacement:function(error,element){
                
                $(element).closest('div').find('.error-txt').html(error);  
            },
            highlight:function(el){
                $(el).closest('div').addClass('error-search');
            },
            unhighlight:function(el){
                $(el).closest('div').removeClass('error-search');
            }
        });
    
    });
    $('#search-form').on( "click",()=>{
      if($('.icon-logo').length){
        if($('.searchbox').hasClass('searchbox-open')){
          $('.icon-logo').css("width","0px")
          $('#search-form').parent().css("width","90%")
        }
        else{
          $('#search-form').parent().css({"width":"30%","transition":"all 0.3s"})
          setTimeout(()=>{
            $('.icon-logo').css({"width":"162px","transition":"all 0.3s"})
          }, 100);
          
        }
      }
      
    });

    
});



 $(window).on('scroll', function() {
          var scroll = $(window).scrollTop();

          if (scroll >= 50) {
              $('.navbar').addClass('navbar-color');
          } else {
              $('.navbar').removeClass('navbar-color');
          }
      });


$('.cls_showPanel').on('click',function(e){
    var that = $(this),
    divToToggle = $('#'+that.data('controls')),
    childDiv = $('.cls_showPanelChild'),
    alreadyOpenDiv = null;
    for(var i=0;i<childDiv.length;i++){
        if(!$(childDiv[i]).hasClass('collapse')){
            alreadyOpenDiv = childDiv[i];
        }
    }
    if(alreadyOpenDiv != null){
        var alreadyOpenDivId = $(alreadyOpenDiv).attr('id');
        if(that.data('controls') != alreadyOpenDivId){
            $('#'+alreadyOpenDivId).addClass('collapse');
            $('#'+alreadyOpenDivId).closest('.panel-pr').find('.panel').removeClass('panel-mg');
        }
    }

    if(divToToggle.css('display')=='none'){
        divToToggle.removeClass('collapse');  
        divToToggle.closest('.panel-pr').find('.panel').addClass('panel-mg');  
    } else {
        divToToggle.addClass('collapse');  
        divToToggle.closest('.panel-pr').find('.panel').removeClass('panel-mg');  
    }
    
        
    
    
    
});


$.validator.addMethod("lettersonly", function (value, element){
    return this.optional(element) || /^[a-z\s]*$/i.test(value);
}, "Letters only please");

$("#overlay_lead").validate({
    submitHandler:function (form) {
        var action = $(form).attr('action');
        $('#overlay-submit-btn').attr('disabled', 'true')
        $.post(action, $(form).serialize(), function (data) {
            if (data && data['status']){
                $.each($("#overlay_lead"), function (i, e) {
                    e.reset();
                });
                $("#overlay_lead label").remove();
                var conversion_id = 991709191;
                var conversion_label = "ciw9CIetw1gQh5Dx2AM";
                var ga_code = document.createElement('div');
                ga_code.innerHTML = '<img height="1" width="1" style="border-style:none;" alt="" src="http://www.googleadservices.com/pagead/conversion/' + conversion_id + '/?label=' + conversion_label + '&amp;guid=ON&amp;script=0"/>';
               document.body.appendChild(ga_code);
                $('#overlay_lead').css('display', 'none');
                $('.thankyou-popup').css('display','inherit');
                if($('.modal').modal){
                    setTimeout(function() {
                        $('.modal').modal('hide');
                    }, 4000);
                }
                else{
                    setTimeout(function() {
                        $('.modal').fadeOut(300);
                    }, 4000);
                }
                return false;
            }
        }, 'json');
    },
    rules:{
        number:{
            required:true,
            number:true,
            minlength:10,
            maxlength:10,
        },
        email:{
            email:true,
            required:true,

        },
        name:{
            required:true,
            lettersonly:true,

        },
    },
    messages:{
        number:{
           required:"Field is required",
           number: "Please enter valid number only"
        },
        email:{
            required:"Field is required"
        },
        name:{
            required:"Field is required"
        },
    },
    highlight:function(element, errorClass) {
      $(element).closest('.form-group').addClass('error');
    },
    unhighlight:function(element, errorClass) {
      $(element).closest('.form-group').removeClass('error');
      $(element).siblings('.js-error').html("");
    },
    errorPlacement: function(error, element){
      $(element).siblings('.js-error').html(error.text());
    } 
});

function closeOverlayModal() {
    $('.modal').fadeOut(300);
}