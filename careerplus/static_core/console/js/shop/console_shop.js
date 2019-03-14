// /**
//  * Resize function without multiple trigger
//  * 
//  * Usage:
//  * $(window).smartresize(function(){  
//  *     // code here
//  * });
//  */
// (function($,sr){
//     // debouncing function from John Hann
//     // http://unscriptable.com/index.php/2009/03/20/debouncing-javascript-methods/
//     var debounce = function (func, threshold, execAsap) {
//       var timeout;

//         return function debounced () {
//             var obj = this, args = arguments;
//             function delayed () {
//                 if (!execAsap)
//                     func.apply(obj, args); 
//                 timeout = null; 
//             }

//             if (timeout)
//                 clearTimeout(timeout);
//             else if (execAsap)
//                 func.apply(obj, args);

//             timeout = setTimeout(delayed, threshold || 100); 
//         };
//     };

//     // smartresize 
//     jQuery.fn[sr] = function(fn){  return fn ? this.bind('resize', debounce(fn)) : this.trigger(sr); };

// })(jQuery,'smartresize');
// /**
//  * To change this license header, choose License Headers in Project Properties.
//  * To change this template file, choose Tools | Templates
//  * and open the template in the editor.
//  */

// var CURRENT_URL = window.location.href.split('#')[0].split('?')[0],
//     $BODY = $('body'),
//     $MENU_TOGGLE = $('#menu_toggle'),
//     $SIDEBAR_MENU = $('#sidebar-menu'),
//     $SIDEBAR_FOOTER = $('.sidebar-footer'),
//     $LEFT_COL = $('.left_col'),
//     $RIGHT_COL = $('.right_col'),
//     $NAV_MENU = $('.nav_menu'),
//     $FOOTER = $('footer');

	
	
// // Sidebar
// function init_sidebar() {
// // TODO: This is some kind of easy fix, maybe we can improve this
// var setContentHeight = function () {
// 	// reset height
// 	$RIGHT_COL.css('min-height', $(window).height());

// 	var bodyHeight = $BODY.outerHeight(),
// 		footerHeight = $BODY.hasClass('footer_fixed') ? -10 : $FOOTER.height(),
// 		leftColHeight = $LEFT_COL.eq(1).height() + $SIDEBAR_FOOTER.height(),
// 		contentHeight = bodyHeight < leftColHeight ? leftColHeight : bodyHeight;

// 	// normalize content
// 	contentHeight -= $NAV_MENU.height() + footerHeight;

// 	$RIGHT_COL.css('min-height', contentHeight);
// };

//   $SIDEBAR_MENU.find('a').on('click', function(ev) {
// 	  console.log('clicked - sidebar_menu');
//         var $li = $(this).parent();

//         if ($li.is('.active')) {
//             $li.removeClass('active active-sm');
//             $('ul:first', $li).slideUp(function() {
//                 setContentHeight();
//             });
//         } else {
//             // prevent closing menu if we are on child menu
//             if (!$li.parent().is('.child_menu')) {
//                 $SIDEBAR_MENU.find('li').removeClass('active active-sm');
//                 $SIDEBAR_MENU.find('li ul').slideUp();
//             }else
//             {
// 				if ( $BODY.is( ".nav-sm" ) )
// 				{
// 					$SIDEBAR_MENU.find( "li" ).removeClass( "active active-sm" );
// 					$SIDEBAR_MENU.find( "li ul" ).slideUp();
// 				}
// 			}
//             $li.addClass('active');

//             $('ul:first', $li).slideDown(function() {
//                 setContentHeight();
//             });
//         }
//     });

// // toggle small or large menu 
// $MENU_TOGGLE.on('click', function() {
// 		console.log('clicked - menu toggle');
		
// 		if ($BODY.hasClass('nav-md')) {
// 			$SIDEBAR_MENU.find('li.active ul').hide();
// 			$SIDEBAR_MENU.find('li.active').addClass('active-sm').removeClass('active');
// 		} else {
// 			$SIDEBAR_MENU.find('li.active-sm ul').show();
// 			$SIDEBAR_MENU.find('li.active-sm').addClass('active').removeClass('active-sm');
// 		}

// 	$BODY.toggleClass('nav-md nav-sm');

// 	setContentHeight();
// });

// 	// check active menu
// 	$SIDEBAR_MENU.find('a[href="' + CURRENT_URL + '"]').parent('li').addClass('current-page');

// 	$SIDEBAR_MENU.find('a').filter(function () {
// 		return this.href == CURRENT_URL;
// 	}).parent('li').addClass('current-page').parents('ul').slideDown(function() {
// 		setContentHeight();
// 	}).parent().addClass('active');

// 	// recompute content when resizing
// 	$(window).smartresize(function(){  
// 		setContentHeight();
// 	});

// 	setContentHeight();

// 	// fixed sidebar
// 	if ($.fn.mCustomScrollbar) {
// 		$('.menu_fixed').mCustomScrollbar({
// 			autoHideScrollbar: true,
// 			theme: 'minimal',
// 			mouseWheel:{ preventDefault: true }
// 		});
// 	}
// };
// // /Sidebar

// 	var randNum = function() {
// 	  return (Math.floor(Math.random() * (1 + 40 - 20))) + 20;
// 	};


// // Panel toolbox
// $(document).ready(function() {
//     $('.collapse-link').on('click', function() {
//         var $BOX_PANEL = $(this).closest('.x_panel'),
//             $ICON = $(this).find('i'),
//             $BOX_CONTENT = $BOX_PANEL.find('.x_content');
        
//         // fix for some div with hardcoded fix class
//         if ($BOX_PANEL.attr('style')) {
//             $BOX_CONTENT.slideToggle(200, function(){
//                 $BOX_PANEL.removeAttr('style');
//             });
//         } else {
//             $BOX_CONTENT.slideToggle(200); 
//             $BOX_PANEL.css('height', 'auto');  
//         }

//         $ICON.toggleClass('fa-chevron-up fa-chevron-down');
//     });

//     $('.close-link').click(function () {
//         var $BOX_PANEL = $(this).closest('.x_panel');

//         $BOX_PANEL.remove();
//     });
// });
// // /Panel toolbox

// // Tooltip
// $(document).ready(function() {
//     $('[data-toggle="tooltip"]').tooltip({
//         container: 'body'
//     });
// });
// // /Tooltip

// // Progressbar
// if ($(".progress .progress-bar")[0]) {
//     $('.progress .progress-bar').progressbar();
// }
// // /Progressbar

// // Switchery
// $(document).ready(function() {
//     if ($(".js-switch")[0]) {
//         var elems = Array.prototype.slice.call(document.querySelectorAll('.js-switch'));
//         elems.forEach(function (html) {
//             var switchery = new Switchery(html, {
//                 color: '#26B99A'
//             });
//         });
//     }
// });
// // /Switchery


// // iCheck
// $(document).ready(function() {
//     if ($("input.flat")[0]) {
//         $(document).ready(function () {
//             $('input.flat').iCheck({
//                 checkboxClass: 'icheckbox_flat-green',
//                 radioClass: 'iradio_flat-green'
//             });
//         });
//     }
// });
// // /iCheck

// // Table
// $('table input').on('ifChecked', function () {
//     checkState = '';
//     $(this).parent().parent().parent().addClass('selected');
//     countChecked();
// });
// $('table input').on('ifUnchecked', function () {
//     checkState = '';
//     $(this).parent().parent().parent().removeClass('selected');
//     countChecked();
// });

// var checkState = '';

// $('.bulk_action input').on('ifChecked', function () {
//     checkState = '';
//     $(this).parent().parent().parent().addClass('selected');
//     countChecked();
// });
// $('.bulk_action input').on('ifUnchecked', function () {
//     checkState = '';
//     $(this).parent().parent().parent().removeClass('selected');
//     countChecked();
// });
// $('.bulk_action input#check-all').on('ifChecked', function () {
//     checkState = 'all';
//     countChecked();
// });
// $('.bulk_action input#check-all').on('ifUnchecked', function () {
//     checkState = 'none';
//     countChecked();
// });

// function countChecked() {
//     if (checkState === 'all') {
//         $(".bulk_action input[name='table_records']").iCheck('check');
//     }
//     if (checkState === 'none') {
//         $(".bulk_action input[name='table_records']").iCheck('uncheck');
//     }

//     var checkCount = $(".bulk_action input[name='table_records']:checked").length;

//     if (checkCount) {
//         $('.column-title').hide();
//         $('.bulk-actions').show();
//         $('.action-cnt').html(checkCount + ' Records Selected');
//     } else {
//         $('.column-title').show();
//         $('.bulk-actions').hide();
//     }
// }



// // Accordion
// $(document).ready(function() {
//     $(".expand").on("click", function () {
//         $(this).next().slideToggle(200);
//         $expand = $(this).find(">:first-child");

//         if ($expand.text() == "+") {
//             $expand.text("-");
//         } else {
//             $expand.text("+");
//         }
//     });
// });

// // NProgress
// if (typeof NProgress != 'undefined') {
//     $(document).ready(function () {
//         NProgress.start();
//     });

//     $(window).load(function () {
//         NProgress.done();
//     });
// }

	
// 	  //hover and retain popover when on popover content
//         var originalLeave = $.fn.popover.Constructor.prototype.leave;
//         $.fn.popover.Constructor.prototype.leave = function(obj) {
//           var self = obj instanceof this.constructor ?
//             obj : $(obj.currentTarget)[this.type](this.getDelegateOptions()).data('bs.' + this.type);
//           var container, timeout;

//           originalLeave.call(this, obj);

//           if (obj.currentTarget) {
//             container = $(obj.currentTarget).siblings('.popover');
//             timeout = self.timeout;
//             container.one('mouseenter', function() {
//               //We entered the actual popover – call off the dogs
//               clearTimeout(timeout);
//               //Let's monitor popover content instead
//               container.one('mouseleave', function() {
//                 $.fn.popover.Constructor.prototype.leave.call(self, self);
//               });
//             });
//           }
//         };

//         $('body').popover({
//           selector: '[data-popover]',
//           trigger: 'click hover',
//           delay: {
//             show: 50,
//             hide: 400
//           }
//         });


// 	function gd(year, month, day) {
// 		return new Date(year, month - 1, day).getTime();
// 	}
	  
	
	   	    
	   
		
// 	  /* INPUTS */
	  
// 		function onAddTag(tag) {
// 			alert("Added a tag: " + tag);
// 		  }

// 		  function onRemoveTag(tag) {
// 			alert("Removed a tag: " + tag);
// 		  }

// 		  function onChangeTag(input, tag) {
// 			alert("Changed a tag: " + tag);
// 		  }

// 		  //tags input
// 		function init_TagsInput() {
			  
// 			if(typeof $.fn.tagsInput !== 'undefined'){	
			 
// 			$('#id_career_outcomes').tagsInput({
// 			  width: 'auto'
// 			});
			
// 			}
			
// 	    };




// 	    /* SMART WIZARD */
		
// 		function init_SmartWizard() {
			
// 			if( typeof ($.fn.smartWizard) === 'undefined'){ return; }
// 			console.log('init_SmartWizard');
			
// 			$('#wizard').smartWizard();

// 			/*$('#wizard_verticle').smartWizard({
// 			  transitionEffect: 'slide'
// 			});*/

// 			$('.buttonNext').addClass('btn btn-success');
// 			$('.buttonPrevious').addClass('btn btn-primary');
// 			$('.buttonFinish').addClass('btn btn-default');
			
// 		};
	   
   
	
// 		/* INPUT MASK */
			
// 		function init_InputMask() {
			
// 			if( typeof ($.fn.inputmask) === 'undefined'){ return; }
// 			console.log('init_InputMask');
			
// 				$(":input").inputmask();
				
// 		};
	  
		
	   
	  /* VALIDATOR */

	  function init_category_parsley(){

	  		window.Parsley.addValidator('notdefault', {
			  validateString: function(value) {
			  	return "0" != value;
			  },
			  messages: {
			    en: 'This should not be default',
			  }
			});

		  	window.Parsley.addValidator('filemimetypes', {
	            requirementType: 'string',
	            validateString: function (value, requirement, parsleyInstance) {

	                var file = parsleyInstance.$element[0].files;

	                if (file.length == 0) {
	                    return true;
	                }

	                var allowedMimeTypes = requirement.replace(/\s/g, "").split(',');
	                return allowedMimeTypes.indexOf(file[0].type) !== -1;

	            },
	            messages: {
	                en: 'Only %s is allowed'
	            }
	        });

	        window.Parsley.addValidator('maxFileSize', {
			  validateString: function(_value, maxSize, parsleyInstance) {
			    var files = parsleyInstance.$element[0].files;
			    return files.length != 1  || files[0].size <= maxSize * 1024;
			  },
			  requirementType: 'integer',
			  messages: {
			    en: 'This file should not be larger than %s Kb',
			  }
			});
		
		  	
	  };


	   function init_skill_add() {
	  	if($('#add-skill-form').length > 0){
	  		var parsleyConfig = {
		        errorsContainer: function(parsleyField) {
		            var $errfield = parsleyField.$element.parent().siblings('.alert');
		            return $errfield;
		        },
		    };
			
		  	$('#add-skill-form').parsley(parsleyConfig).on('field:validated', function() {
				if (this.validationResult === true) {
			      this.$element.closest('.item').removeClass('bad');

			    } else {
			      this.$element.closest('.item').addClass('bad');
			    }
			});
		};	  
	  	
	  };

	  function init_skill_change() {

	  	if($('#change-skill-form').length > 0){
	  		var parsleyConfig = {
		        errorsContainer: function(parsleyField) {
		            var $errfield = parsleyField.$element.parent().siblings('.alert');
		            return $errfield;
		        },
		    };
			
	  		$('#change-skill-form').parsley(parsleyConfig).on('field:validated', function() {
				if (this.validationResult === true) {
			      this.$element.closest('.item').removeClass('bad');

			    } else {
			      this.$element.closest('.item').addClass('bad');
			    }
			});
		};	  
	  	
	  };

	  function init_category_add() {
	  	if($('#add-category-form').length > 0){
	  		var parsleyConfig = {
		        errorsContainer: function(parsleyField) {
		            var $errfield = parsleyField.$element.parent().siblings('.alert');
		            return $errfield;
		        },
		    };
			
		  	$('#add-category-form').parsley(parsleyConfig).on('field:validated', function() {
				if (this.validationResult === true) {
			      this.$element.closest('.item').removeClass('bad');

			    } else {
			      this.$element.closest('.item').addClass('bad');
			    }
			});
		};	  
	  	
	  };
	   
	  
	  function init_category_change() {

	  	if($('#change-category-form').length > 0){
	  		var parsleyConfig = {
		        errorsContainer: function(parsleyField) {
		            var $errfield = parsleyField.$element.parent().siblings('.alert');
		            return $errfield;
		        },
		    };
			
	  		$('#change-category-form').parsley(parsleyConfig).on('field:validated', function() {
				if (this.validationResult === true) {
			      this.$element.closest('.item').removeClass('bad');

			    } else {
			      this.$element.closest('.item').addClass('bad');
			    }
			});
		};	  
	  	
	  };
	  
	  function init_category_seo_change() {
	  	if($('#change-category-seo-form').length > 0){
	  		var parsleyConfig = {
		        errorsContainer: function(parsleyField) {
		            var $errfield = parsleyField.$element.parent().siblings('.alert');
		            return $errfield;
		        },
		    };
			
			$('#change-category-seo-form').parsley(parsleyConfig).on('field:validated', function() {
				if (this.validationResult === true) {
			      this.$element.closest('.item').removeClass('bad');

			    } else {
			      this.$element.closest('.item').addClass('bad');
			    }
			});/*.on('form:submit', function() {
			    console.log('error');
	  		    return false; // Don't submit form for this demo
			  });*/
		};	  
	  	
	  };

	  function init_category_relation_change() {
	  	if($('#change-category-relation-form').length > 0){
	  		var parsleyConfig = {
		        errorsContainer: function(parsleyField) {
		            var $errfield = parsleyField.$element.parent().siblings('.alert');
		            return $errfield;
		        },
		    };
			
			$('#change-category-relation-form').parsley(parsleyConfig).on('field:validated', function() {
				if (this.validationResult === true) {
			      this.$element.closest('.item').removeClass('bad');

			    } else {
			      this.$element.closest('.item').addClass('bad');
			    }
			});/*.on('form:submit', function() {
			    console.log('error');
	  		    return false; // Don't submit form for this demo
			  });*/
		};	  
	  	
	  };

	function init_category_skill_change() {
		  	if($('#change-category-skill-form').length > 0){
		  		var parsleyConfig = {
			        errorsContainer: function(parsleyField) {
			            var $errfield = parsleyField.$element.parent().siblings('.alert');
			            return $errfield;
			        },
			    };
				
				$('#change-category-skill-form').parsley(parsleyConfig).on('field:validated', function() {
					if (this.validationResult === true) {
				      this.$element.closest('.item').removeClass('bad');

				    } else {
				      this.$element.closest('.item').addClass('bad');
				    }
				});/*.on('form:submit', function() {
				    console.log('error');
		  		    return false; // Don't submit form for this demo
				  });*/
			};	  
		  	
		  };

		function init_tree_cat() {
	      $('.tree li:has(ul)').addClass('parent_li').find(' > span').attr('title', 'Collapse this branch');
		    $('.tree li.parent_li > span').on('click', function (e) {
		        var children = $(this).parent('li.parent_li').find(' > ul > li');
		        if (children.is(":visible")) {
		            children.hide('fast');
		            $(this).attr('title', 'Expand this branch').find(' > i').addClass('fa-plus-square').removeClass('fa-minus-square');
		        } else {
		            children.show('fast');
		            $(this).attr('title', 'Collapse this branch').find(' > i').addClass('fa-minus-square').removeClass('fa-plus-square');
		        }
		        e.stopPropagation();
		    });
		};	

	function init_faq_add() {
	  	if($('#add-faq-form').length > 0){
	  		var parsleyConfig = {
		        errorsContainer: function(parsleyField) {
		            var $errfield = parsleyField.$element.parent().siblings('.alert');
		            return $errfield;
		        },
		    };
			
		  	$('#add-faq-form').parsley(parsleyConfig).on('field:validated', function() {
				if (this.validationResult === true) {
			      this.$element.closest('.item').removeClass('bad');

			    } else {
			      this.$element.closest('.item').addClass('bad');
			    }
			});
		};	  
	  	
	  };

	  function init_chapter_add() {
	  	if($('#add-chapter-form').length > 0){
	  		var parsleyConfig = {
		        errorsContainer: function(parsleyField) {
		            var $errfield = parsleyField.$element.parent().siblings('.alert');
		            return $errfield;
		        },
		    };
			
		  	$('#add-chapter-form').parsley(parsleyConfig).on('field:validated', function() {
				if (this.validationResult === true) {
			      this.$element.closest('.item').removeClass('bad');

			    } else {
			      this.$element.closest('.item').addClass('bad');
			    }
			});
		};	  
	  	
	  };
	  
	  function init_keyword_add() {
	  	if($('#add-keyword-form').length > 0){
	  		var parsleyConfig = {
		        errorsContainer: function(parsleyField) {
		            var $errfield = parsleyField.$element.parent().siblings('.alert');
		            return $errfield;
		        },
		    };
			$('#add-keyword-form').parsley(parsleyConfig).on('field:validated', function() {
				if (this.validationResult === true) {
			      this.$element.closest('.item').removeClass('bad');

			    } else {
			      this.$element.closest('.item').addClass('bad');
			    }
			});
		};	  
	  	
	  };

	  function init_attribute_add() {
	  	if($('#add-attribute-form').length > 0){
	  		var parsleyConfig = {
		        errorsContainer: function(parsleyField) {
		            var $errfield = parsleyField.$element.parent().siblings('.alert');
		            return $errfield;
		        },
		    };
			
		  	$('#add-attribute-form').parsley(parsleyConfig).on('field:validated', function() {
				if (this.validationResult === true) {
			      this.$element.closest('.item').removeClass('bad');

			    } else {
			      this.$element.closest('.item').addClass('bad');
			    }
			});
		};	  
	  	
	  };

	function init_category_product_change() {
	  	if($('#change-category-product-form').length > 0){
	  		console.log('check');
	  		var parsleyConfig = {
		        errorsContainer: function(parsleyField) {
		            var $errfield = parsleyField.$element.parent().siblings('.alert');
		            return $errfield;
		        },
		    };
			
			$('#change-category-product-form').parsley(parsleyConfig).on('field:validated', function() {
				if (this.validationResult === true) {
			      this.$element.closest('.item').removeClass('bad');

			    } else {
			      this.$element.closest('.item').addClass('bad');
			    }
			});/*.on('form:submit', function() {
			    console.log('error');
	  		    return false; // Don't submit form for this demo
			  });*/
		};	  
	  	
	  };

	
	function init_product_add() {
	  	if($('#add-product-form').length > 0){
	  		var parsleyConfig = {
		        errorsContainer: function(parsleyField) {
		            var $errfield = parsleyField.$element.parent().siblings('.alert');
		            return $errfield;
		        },
		    };
			
		  	$('#add-product-form').parsley(parsleyConfig).on('field:validated', function() {
				if (this.validationResult === true) {
			      this.$element.closest('.item').removeClass('bad');

			    } else {
			      this.$element.closest('.item').addClass('bad');
			    }
			});
		};	  
	  	
	  };
	  function init_product_change() {
	  	if($('#change-product-form').length > 0){
	  		var parsleyConfig = {
		        errorsContainer: function(parsleyField) {
		            var $errfield = parsleyField.$element.parent().siblings('.alert');
		            return $errfield;
		        },
		    };
			
		  	$('#change-product-form').parsley(parsleyConfig).on('field:validated', function() {
				if (this.validationResult === true) {
			      this.$element.closest('.item').removeClass('bad');

			    } else {
			      this.$element.closest('.item').addClass('bad');
			    }
			});
		};

		if($('#change-product-price-form').length > 0){
	  		var parsleyConfig = {
		        errorsContainer: function(parsleyField) {
		            var $errfield = parsleyField.$element.parent().siblings('.alert');
		            return $errfield;
		        },
		    };
			
		  	$('#change-product-price-form').parsley(parsleyConfig).on('field:validated', function() {
				if (this.validationResult === true) {
			      this.$element.closest('.item').removeClass('bad');

			    } else {
			      this.$element.closest('.item').addClass('bad');
			    }
			});
		};

		if($('#change-product-attribute-form').length > 0){
	  		var parsleyConfig = {
		        errorsContainer: function(parsleyField) {
		            var $errfield = parsleyField.$element.parent().siblings('.alert');
		            return $errfield;
		        },
		    };
			
		  	$('#change-product-attribute-form').parsley(parsleyConfig).on('field:validated', function() {
				if (this.validationResult === true) {
			      this.$element.closest('.item').removeClass('bad');

			    } else {
			      this.$element.closest('.item').addClass('bad');
			    }
			});
		};	  
	  	
	  };
	  function init_product_seo_change() {
	  	if($('#change-product-seo-form').length > 0){
	  		var parsleyConfig = {
		        errorsContainer: function(parsleyField) {
		            var $errfield = parsleyField.$element.parent().siblings('.alert');
		            return $errfield;
		        },
		    };
			
		  	$('#change-product-seo-form').parsley(parsleyConfig).on('field:validated', function() {
				if (this.validationResult === true) {
			      this.$element.closest('.item').removeClass('bad');

			    } else {
			      this.$element.closest('.item').addClass('bad');
			    }
			});
		};	  
	  	
	  };
	  
	  function init_product_attr_change() {
	  	/*if($('#change-product-attribute-form').length > 0){
	  		var parsleyConfig = {
		        errorsContainer: function(parsleyField) {
		            var $errfield = parsleyField.$element.parent().siblings('.alert');
		            return $errfield;
		        },
		    };
			
		  	$('#change-product-attribute-form').parsley(parsleyConfig).on('field:validated', function() {
				if (this.validationResult === true) {
			      this.$element.closest('.item').removeClass('bad');

			    } else {
			      this.$element.closest('.item').addClass('bad');
			    }
			});
		};*/	  
	  	
	  };
	  	  
	  function init_ColorSelector() {
			
			if( typeof ($.fn.colorselector) === 'undefined'){ return; }
				console.log('init_colorselector');
			
				$('#id_image_bg').colorselector();

		}; 

	function init_product_structure_change() {
	  	if($('#change-product-structure-form').length > 0){
	  		var parsleyConfig = {
		        errorsContainer: function(parsleyField) {
		            var $errfield = parsleyField.$element.parent().siblings('.alert');
		            return $errfield;
		        },
		    };
			
		  	$('#change-product-structure-form').parsley(parsleyConfig).on('field:validated', function() {
				if (this.validationResult === true) {
			      this.$element.closest('.item').removeClass('bad');

			    } else {
			      this.$element.closest('.item').addClass('bad');
			    }
			});
		};	  
	  	
	  };
	  function init_product_faq_change() {
	  	if($('#change-product-faq-form').length > 0){
	  		var parsleyConfig = {
		        errorsContainer: function(parsleyField) {
		            var $errfield = parsleyField.$element.parent().siblings('.alert');
		            return $errfield;
		        },
		    };
			
		  	$('#change-product-faq-form').parsley(parsleyConfig).on('field:validated', function() {
				if (this.validationResult === true) {
			      this.$element.closest('.item').removeClass('bad');

			    } else {
			      this.$element.closest('.item').addClass('bad');
			    }
			});
		};	  
	  	
	  }; 

	 function scrollReload () {
          if (localStorage) {
              var posReader = localStorage["posStorage"];
              if (posReader) {
                  console.log(posReader);
                  $(window).scrollTop(posReader);
                  localStorage.removeItem("posStorage");
              }
              return true;
          }
          return false;
        }
	   
	   
	$(document).ready(function() {
				
		// init_sidebar();
		// init_InputMask();
		// init_SmartWizard();
		// init_TagsInput();
		
		init_ColorSelector();
		init_category_parsley();
		init_category_add();
		init_category_change();
		init_category_seo_change();
		init_category_relation_change();
		init_category_skill_change();

		init_skill_add();
		init_skill_change();
		
		init_tree_cat();
		init_faq_add();
		init_chapter_add();
		init_keyword_add();
		init_attribute_add();
		init_product_add();
		init_product_change();
		init_product_seo_change();
		init_product_attr_change();
		init_category_product_change();
		init_product_structure_change();
		init_product_faq_change();
		scrollReload();
		$( ".save_scroll" ).click(function() {
		  if (localStorage) {
              	  localStorage["posStorage"] = $(window).scrollTop();
          }
          return true;
		});
		
	});




