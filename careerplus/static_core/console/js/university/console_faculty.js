function init_faculty_add() {
	if($('#add-faculty-form').length > 0){
		var parsleyConfig = {
	        errorsContainer: function(parsleyField) {
	            var $errfield = parsleyField.$element.parent().siblings('.alert');
	            return $errfield;
	        },
	    };
	
	  	$('#add-faculty-form').parsley(parsleyConfig).on('field:validated', function() {
			if (this.validationResult === true) {
		      this.$element.closest('.item').removeClass('bad');

		    } else {
		      this.$element.closest('.item').addClass('bad');
		    }
		});
	};	
};

function init_faculty_change() {

	if($('#change-faculty-form').length > 0){
		var parsleyConfig = {
	        errorsContainer: function(parsleyField) {
	            var $errfield = parsleyField.$element.parent().siblings('.alert');
	            return $errfield;
	        },
	    };
	
		$('#change-faculty-form').parsley(parsleyConfig).on('field:validated', function() {
			if (this.validationResult === true) {
		      this.$element.closest('.item').removeClass('bad');

		    } else {
		      this.$element.closest('.item').addClass('bad');
		    }
		});
	};
};


$(document).ready(function() {
	init_faculty_add();
	init_faculty_change();
});

