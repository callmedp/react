
$(document).ready(function() {
	var win = $(window),
		prev_page = 0;

	// Each time the user scrolls
	win.scroll(function() {
		// End of the document reached?
		if ( win.scrollTop() >= ($(document).height() - win.height()) * 0.8) {
			page = $("#pg_id").val();
			if (page != undefined & page != prev_page){
				prev_page = page;
				data = "?page="+ page;
				$.ajax({
					url: "/article/category-wise-loading/" + data,
					dataType: "html",
					success: function(html) {
						$("#load_more").remove();
						$('#category_container').append(html);
						ga('send', 'pageview');
=					},
					failure: function(response){
	                    alert("Something went wrong.")
	                }
				});
			}
			
		}
	});
  	$('#myCarousel').carousel({
        interval: 10000
  	});
});