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
});