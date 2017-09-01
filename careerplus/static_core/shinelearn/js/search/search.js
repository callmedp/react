function filterquery(type) {
    if (type != undefined) {
        $('#form_facets').find('input[name='+type+']').removeAttr('checked');
    }
    $('#form_facets').find('input').removeAttr('disabled', 'disabled');
    $('#id_page').val(1);
    $('#id_rstart').val(1);
    $('#form_facets').submit();
}

$("#load-id").click(function(){
    load_page(
        "/myapp/mymodels/",
        "#pagination-id",
        "#load-id",
        "#pagediv-id"
      );
});

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
        const query = new URLSearchParams(window.location.search);
        query[$(this).attr('name')] = $(this).val();
        $('#id_page').val(1);
        $('#id_rstart').val(1);
        $('#form_facets').submit();
    });
    $(document).on('click', '.js_apply_filter', function () {
        filterquery();
    });
}

$(document).ready(function () {
    paginate();
    SearchFilter();
});