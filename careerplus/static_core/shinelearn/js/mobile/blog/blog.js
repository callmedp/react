$(document).ready(function() {

	$(document).on('click', '#recent-loadmore', function(event) {
		// $('#recent-loadmore').addClass('disabled');
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
		// $('#popular-loadmore').addClass('disabled');
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

	$(document).on('click', '.js_redirect', function(event) {
        window.location.href = window.MOBILE_LOGIN_URL + "?next="+window.location.pathname;
    });
	
});


