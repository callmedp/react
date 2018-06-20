;(function($, activeOnScroll) {
	
	var Scroll = {
		class: 'active',
		_load: function (container) {
			var child = $(container).children();
			child.removeClass(this.class);
			child.first().addClass(this.class);
		},
		_scroll: function (container) {
			
			$(document).on("scroll", onScroll);

			function onScroll(){
				var child = $(container).children();
				var scrollPos = $(document).scrollTop();
				var height = $(container).height();
			    child.each(function () {
			        var currLink = $(this);
			        var refElement = $(currLink.attr("href"));
			        if (refElement.offset().top - $('.cls_sticky_scroller').outerHeight() <= scrollPos + height && 
			        		refElement.offset().top + refElement.outerHeight()  > scrollPos + height ) {
			            child.removeClass("active");
			            currLink.addClass("active");
			        }
			    });
			}

		}
	}

	function init(argument) {
		this.className = argument.className || '.scroll-tab';

		Scroll._load(this.className);
		Scroll._scroll(this.className);

	}

	activeOnScroll.init = init;
}($, (window.activeOnScroll = window.activeOnScroll || {} )))