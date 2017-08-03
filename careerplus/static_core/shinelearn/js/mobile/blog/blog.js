$(document).ready(function() {

	$(document).on('click', '#recent-loadmore', function(event) {
		var formData = $('#loadmore-recent-form').serialize();
		$.ajax({
			url: "/article/lodemore-articlebycategory/",
			data: formData,
			dataType: "html",
			success: function(html) {
				$("#load_more_recent").remove();
				$('#tab-1').append(html);
			},
			failure: function(response){
	            alert("Something went wrong.")
	        }
		});
	});

	$(document).on('click', '#popular-loadmore', function(event) {
		var formData = $('#loadmore-pop-form').serialize();
		$.ajax({
			url: "/article/lodemore-articlebycategory/",
			data: formData,
			dataType: "html",
			success: function(html) {
				$("#load_more_pop").remove();
				$('#tab-2').append(html);
			},
			failure: function(response){
	            alert("Something went wrong.")
	        }
		});
	});
	
});