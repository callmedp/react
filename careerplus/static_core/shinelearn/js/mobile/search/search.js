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

function filterSearch(e)
    {
    clicked = $(e.target);
    className = e.target.classList[0];
    clicked.toggleClass('selected');

    obj = $('#farea_filters .'+className)[0]
    obj.toggleAttribute('checked')
    filterquery();
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

    $('.js_advanced_trigger', '.js_search_trigger').on('click', function(){})

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
    
    
    $('.js_advance_search').on('click', function (e) {
        e.preventDefault();
        var flag1 = true,
            flag2 = true;
        var $tags1 = $('#tags11'),
            $tags2 = $('#tags21');
            if (!$tags1.val()){
                flag1 = false;
                $tags1.closest('div').addClass('error');
                // debugger;
                $('.js_area_error').html('Please choose a functional area.');
            }
            else {
                flag1 = true;
                $tags1.closest('div').removeClass('error');
                $('.js_area_error').html('');
            }
            if (!$tags2.val()){
                flag2 = false;
                $tags2.closest('div').addClass('error');
                $('.js_skill_error').html('Please choose a skill.');
            }
            else {
                flag2 = true;
                $tags2.closest('div').removeClass('error');
                $('.js_skill_error').html('');
            }
            if (flag2 && flag1) {
                $(".js_advance_search_form").submit();
            }
    });

});