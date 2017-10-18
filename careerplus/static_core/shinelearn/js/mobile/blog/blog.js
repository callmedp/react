$(document).ready(function() {

	$(document).on('click', '#recent-loadmore', function(event) {
		this.disabled = true;
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
		this.disabled = true;
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

	$(document).on('click', '#recent-loadmore-tag', function(event) {
		this.disabled = true;
		var formData = $('#loadmore-recent-form').serialize();
		$.ajax({
			url: "/article/lodemore-articlebytag/",
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

	$(document).on('click', '#popular-loadmore-tag', function(event) {
		this.disabled = true;
		var formData = $('#loadmore-pop-form').serialize();
		$.ajax({
			url: "/article/lodemore-articlebytag/",
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


