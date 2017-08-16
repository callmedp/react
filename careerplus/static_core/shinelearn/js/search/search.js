function filterquery(type) {
    if (type != undefined) {
        $('#form_facets').find('input[name='+type+']').removeAttr('checked');
    }
    $('#form_facets').find('input').removeAttr('disabled', 'disabled');
    $('#id_page').val(1);
    $('#id_rstart').val(1);
    if($('.cls_paginate').length) {
    	$('.cls_paginate').first().click();
	} else {
		$('#form_facets').submit();
	}
}

function paginate() {
    $('.cls_paginate').click(function(e){
        var jObj={};
        jObj.element = $(this);
        jObj.val = (e.originalEvent == undefined ? 1 : (jObj.element.data('type') == 'next' ? parseInt($('#id_rstart').val()) + 1 : parseInt($('#id_rstart').val()) - 1));
        if(jObj.val < 2) {
            $('#id_page').val(1);
            jObj.val = '/';
        } else {
            $('#id_page').val(jObj.val)
            jObj.val = '/'+ jObj.val + '/';
        }

        jObj.action = top.window.location.pathname;
        switch ($('#id_search_type').val()) {
            case 'similar':
                jObj.newaction = jObj.action.replace((sc.LOGGEDIN == true ? '/myshine/job-search/similar/' : '/job-search/similar/'),'');
                jObj.url = jObj.newaction.split('/');
                jObj.newaction = (sc.LOGGEDIN == true ? '/myshine/job-search/similar' : '/job-search/similar');
                jObj.newaction +=  jObj.val + top.window.location.search;
                break;
            default:
                    /* For single keyword urls */
                    jObj.urlArray = top.window.location.pathname.split('-');
                    if(!isNaN(jObj.urlArray[jObj.urlArray.length-1])) {
                        jObj.urlArray.splice(jObj.urlArray.length-1,1);
                    }

                    jObj.newaction =  jObj.urlArray.join('-') + (jObj.val == '/' ? '' : '-' + jObj.val.replace(/\//g,"")) + top.window.location.search;

            break;
        }

        $('#form_facets').attr('action',jObj.newaction );
        if(sc.isFromMsite) {
            $.mobile_binder.showHideLoader('show');
        } else {
            $app.overLay(true);
        }

        $('#form_facets').submit();

    });

}

function SearchFilter() {
    $(document).on('change','.cls_filter', function(){
        var $formFacets = $('#form_facets');
        $formFacets.find('input#' + $(this).attr('hdn')).val($(this).val());
        $formFacets.find('input').removeAttr('disabled', 'disabled');
        $('#id_page').val(1);
        $('#id_rstart').val(1);
        if($('.cls_paginate').length){
            $('.cls_paginate').first().click();
        } else {
            $app.overLay(true);
            $('#form_facets').submit();
        }
    });
}

$(document).ready(function () {
    paginate();
    SearchFilter();
});