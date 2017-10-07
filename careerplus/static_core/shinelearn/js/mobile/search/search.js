$(document).ready(function () {
    var win = $(window);
    var EOP = false;
	// Each time the user scrolls
	win.scroll(function() {
		// End of the document reached?
		if ($(document).height() - win.height() == win.scrollTop()) {


			$.ajax({
				url: 'get-post.php',
				dataType: 'html',
				success: function(html) {
					$('#posts').append(html);
					$('#loading').hide();
				}
			});

            var $loading = $('#loading'),
                $pageNo = $('#id_page'),
                $formFacets = $('#form_facets');
            $loading.show();
            $pageNo.val(parseInt($pageNo.val()) + 1);
            var formData = $formFacets.serialize();

            $loading.text("Loading ...");

            $.ajax({
                async: true,
                type: "GET",
                url: $formFacets.attr('action'),
                data: formData,
                error: function() {
                    alert("There was a problem loading more products. Try again later");
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
		}
	});
});