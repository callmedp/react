function filterquery(type) {
    var $formFacets = $('#form_facets');
    if (type != undefined) {
        $formFacets.find('input[name='+type+']').removeAttr('checked');
    }
    $formFacets.find('input').removeAttr('disabled', 'disabled');
    //TODO: uncomment below code when non existing attribute handling is done in solr.
    // $formFacets.find('.js_filter_sxn').each(function () {
    //     var totalInputs = $(this).find('input').length;
    //     var checkedInputs = $(this).find('input:checked').length;
    //     if (checkedInputs == totalInputs) {
    //         $(this).find('input').each(function() {
    //            $(this).attr('name', 'ign_'+ $(this).attr('name'));
    //         });
    //     }
    // });
    $('#id_page').val(1);
    $('#id_rstart').val(1);
    $formFacets.submit();
}

function paginate() {
    $('.cls_load_more').click(function(e){
        e.preventDefault();
        var $this = $(this),
            $pageNo = $('#id_page'),
            $formFacets = $('#form_facets');
        $pageNo.val(parseInt($pageNo.val()) + 1);
        var formData = $formFacets.serialize();
        
        $(this).prop("disabled", true);
        $(this).text("Loading ...");
        
        $.ajax({
            async: true,
            type: "GET",
            url: $formFacets.attr('action'),
            data: formData,
            error: function() {
                $this.replaceWith("<p>There was a problem loading more products. Try again later/</p>");
            },
            success: function(data){ // check if there is an additional page
                                    // , disable load button if not
                if (!data['has_next']) {
                    $this.hide();
                }
                else {
                    $this.text("Load more");
                    $this.prop("disabled", false);
                }
                $('.js_listing').append(data["response"]);
            }
        });
    });

}

function SearchFilter() {
    $(document).on('change','.cls_filter', function(){
        var $formFacets = $('#form_facets');
        $formFacets.find('input#' + $(this).attr('hdn')).val($(this).val());
        $formFacets.find('input').removeAttr('disabled', 'disabled');
        $('#id_page').val(1);
        $('#id_rstart').val(1);
        $formFacets.submit();
    });
    $(document).on('click', '.js_apply_filter', function () {
        filterquery();
    });
}

$(document).ready(function () {
    paginate();
    SearchFilter();
    
    $('#id_area').inputTags({
        placeholder: prefetchedFuncArea ? '': "Select Functional Area",
        autocomplete: {
            values: funcAreaSet,
            actualValues: funcAreaSet,
            only: true
        },
        max: 1,
        maxLength: 100,
        create: function(e) {
            var $field = e.$input[0];
            $field.placeholder = '';
        },
        destroy: function(e) {
            var $field = e.$input[0];
            if (e.tags.length == 0)
            $field.placeholder = 'Select Functional Area';
        },
        errors: {
            empty: "Be careful, you can't add an empty tag.",
            minLength: 'Your tag must have at least %s characters.',
            maxLength: 'Your tag must not exceed %s characters.',
            max: 'Please note that the number of tags must not exceed %s.',
            email: 'The email address you entered is not valid',
            exists: 'This tag already exists',
            autocomplete_only: 'You must select a value from the list.',
            timeout: 8000
        }
    });

    $('#id_skills').inputTags({
        placeholder: prefetchedSkills ? '': "Choose upto 2 Skills",
        autocomplete: {
            values: skillsSet,
            actualValues: skillsSet,
            only: true
        },
        max: 3,
        create: function(e) {
            var $field = e.$input[0];
            $field.placeholder = '';
        },
        destroy: function(e) {
            var $field = e.$input[0];
            if (e.tags.length == 0)
            $field.placeholder = 'Choose upto 2 Skills';
        },
        errors: {
            empty: "Be careful, you can't add an empty tag.",
            minLength: 'Your tag must have at least %s characters.',
            maxLength: 'Your tag must not exceed %s characters.',
            max: 'Please note that the number of tags must not exceed %s.',
            email: 'The email address you entered is not valid',
            exists: 'This tag already exists',
            autocomplete_only: 'You must select a value from the list.',
            timeout: 8000
        }
    });
    $("#ex2").slider({});
    $('.tt-query').css('background-color','#fff');
    // $('.js_advance_search').on('click', function () {
    //     var flag = true;
    //         if (!$('#id_area').val()){
    //             flag = false;
    //             $('#id_area').siblings('.error-txt').html('Please choose a functional area.');
    //         }
    //         if (!$('#id_skills').val()){
    //             flag = false;
    //             $('#id_skills').siblings('.error-txt').html('Please choose a skill.');
    //         }
    //         if (flag) {
    //             $(".js_advance_search_form").submit();
    //         }    
    // });
});