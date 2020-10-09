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
window.Parsley.addValidator('imagedimension', {
  requirementType: 'string',
  validateString: function(value, requirement, parsleyInstance) {
    let [width, height] = requirement.split('x');
    var _URL = window.URL || window.webkitURL;
	var file, img;
	file = parsleyInstance.$element[0].files[0];
    if (file) {
        img = new Image();
        let deferred = $.Deferred();
        img.onload = function () {
            console.log("height: " + height + "img height: " + img.height )
            console.log("width: " + width + "img width: " + img.width)
            console.log(img.width >= width && img.height >= height)
            if (img.width >= width && img.height >= height) {
                deferred.resolve();
            }
            else {
                deferred.reject();
            }
        };
        img.src = _URL.createObjectURL(file);
        return deferred.promise();
    }
  },
  messages: {
    en: 'Image dimensions have to be at least  %s px',
  }
});

