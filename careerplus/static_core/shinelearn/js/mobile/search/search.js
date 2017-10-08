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

$(document).ready(function () {
    var win = $(window);
    var EOP = false,
        inProgress = false;
	// Each time the user scrolls
    var $loading = $('#loading'),
                $pageNo = $('#id_page'),
                $formFacets = $('#form_facets');
    if (totalProducts > $('.js_prod_card').length) {
        win.scroll(function () {
            // End of the document reached?
            if (($(document).height() - win.height() == win.scrollTop()) && !EOP && !inProgress) {

                $loading.show();
                $pageNo.val(parseInt($pageNo.val()) + 1);
                var formData = $formFacets.serialize();

                $loading.text("Loading ...");
                inProgress = true;
                $.ajax({
                    async: true,
                    type: "GET",
                    url: $formFacets.attr('action'),
                    data: formData,
                    error: function () {
                        alert("There was a problem loading more products. Try again later");
                        inProgress = false;
                    },
                    success: function (data) { // check if there is an additional page
                        // , disable load button if not
                        if (!data['has_next']) {
                            EOP = true;
                        }
                        $loading.hide();
                        $('.js_listing').append(data["response"]);
                        inProgress = false;
                    }
                });
            }
        });
    }

    $('.js_sidebar_advanced').simplerSidebar({
        opener: '.js_advanced_trigger',
        animation: {
            easing: "easeOutQuint"
        },
        sidebar: {
            align: 'right'
        }
    });

    $('.js_sidebar_search').simplerSidebar({
        opener: '.js_search_trigger',
        animation: {
            easing: "easeOutQuint"
        },
        sidebar: {
            align: 'right'
        }
    });

    $(document).on('click', '.js_apply_filter', function () {
        filterquery();
    });

    $(document).on('click', '.js_clear_filters', function () {
       $('.js_filter_container').find("input[type='checkbox']:checked:not(:disabled)").attr('checked', false);
    });

    $('.js_query_input').keypress(function (e) {
        if (e.which == 13) {
            $('form#search_form').submit();
            return false;    
        }
    });
    
    // $('#tags11').typeahead({
    //         local: funcAreaSet
    //     });
    //     $('#tags21').typeahead({
    //         local: skillsSet
    //     });
});