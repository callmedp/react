$(document).on("click","a[href^='tel']",function(){
    MyGA.SendEvent('CallbackRequested', 'Call Interactions', 'General Enquiry', 'success');
});

/* 
1) .cls_search is the search form class 
2) q is the element where user writes
3) this function is binding typeahead for every form it finds with class .cls_search
4) it also binding jquery validate for form validation */
 
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
    });

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
