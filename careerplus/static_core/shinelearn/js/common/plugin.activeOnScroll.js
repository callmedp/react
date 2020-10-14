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
				var navBarHeight = $('#id_nav').outerHeight() || 0;
				var stickyBarHeight = $(".cls_sticky_scroller").outerHeight() || 0;
			    child.each(function () {
			        var currLink = $(this);
			        var refElement = $(currLink.attr("href"));
			        if (refElement.offset().top - stickyBarHeight - navBarHeight <= scrollPos + height && refElement.offset().top + refElement.outerHeight()  > scrollPos + height ) {
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