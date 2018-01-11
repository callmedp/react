$(document).on("click","a[href^='tel']",function(){
    MyGA.SendEvent('CallbackRequested', 'Call Interactions', 'General Enquiry', 'success');
});


$('.cls_search').each(function(index,item){
        $(item).find('input[name=q]').typeahead({
            local: qSearch
        });

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
        })

    });