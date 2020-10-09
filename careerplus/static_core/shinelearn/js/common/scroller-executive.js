var Scroller = function(itm,className) {
        this.item = itm;
        this.parentItem = this.item.parent();
        this.className = className || '.cls_scroller';
    };

    Scroller.prototype = {
      constructor : Scroller,
      scroll :  function() {
        var that = this;
        if(that.parentItem.length < 1 || that.item.length <1){
            return;
        }
        var parentDivTop = that.parentItem.offset().top,
        windowTop = $(window).scrollTop();

        if(windowTop >= parentDivTop && windowTop < (that.item.closest('.cls_scroller_parent').height() + parentDivTop)) {
            that.item.css({
                'top': (windowTop - parentDivTop) + 0
            })
            that.item.find('.cls_scroller_hiddenDiv').removeClass('hidden');
        }else {
            that.item.css({
                'top': 0
            })
            that.item.find('.cls_scroller_hiddenDiv').addClass('hidden');
        }
        
    } 
}


$.fn.scrollerdiv = function() {
    var that = this;
    that.each(function(index,item){
        var data  = $(item).data('scrollerdiv');
        if(!data) {
            data = new Scroller($(item));
            $(item).data('scrollerdiv',data);
        }
        $(window).scroll(function() { 
            data.scroll();
        });
    })
}

var stickyHeaderDetail = function(itm){
    this.item = itm;
    this.parentItem = this.item.closest('.cls_sticky_scroller_p');
}

stickyHeaderDetail.prototype = {
    constructor : stickyHeaderDetail,

    scroll: function(){
        var that = this;
        if(that.parentItem.length < 1 || that.item.length <1){
            return;
        }
        var parentDivTop = that.parentItem.offset().top,
        windowTop = $(window).scrollTop();
        if(windowTop >= parentDivTop){
            that.item.css({
                'top': (windowTop - parentDivTop) + $('#id_nav').outerHeight()
            });
            //$('#id_nav').hide();
            that.item.find('.cls_scroller_hiddenDiv').removeClass('hidden');
            $('.cls_enquiry_cart').hide();
            $('.cls_samples_enquiry').addClass('fixedSample');
        }else {
          that.item.css({
            'top': 0
          });
          $('#id_nav').show();
          that.item.find('.cls_scroller_hiddenDiv').addClass('hidden');
          $('.cls_enquiry_cart').show();
          $('.cls_samples_enquiry').removeClass('fixedSample')
        }
        if($('.cls_samples_enquiry').hasClass('fixedSample')){
            if($('.cls_hide_sticky_panel').length){
                if((windowTop + $('.cls_samples_enquiry').height() + 10) > $($('.cls_hide_sticky_panel')[0]).offset().top){
                    $('.cls_samples_enquiry').hide();       
                }else{
                    $('.cls_samples_enquiry').show(); 
                }
            }

        }
    }
}

$.fn.productdetailAnimations = function() {
    var that = this;
    that.each(function(index,item){
        var data  = $(item).data('stickyheader');
        if(!data) {
            data = new stickyHeaderDetail($(item));
            $(item).data('stickyheader',data);
        }
        $(window).scroll(function() { 
            data.scroll();
        });
    })
}

$(document).ready(function () {
    $('.cls_scroller').scrollerdiv();
    $('.cls_sticky_scroller').productdetailAnimations();

});





/*
var Scroller = function(itm,className) {
        this.item = itm;
        this.parentItem = this.item.parent();
        this.className = className || '.cls_scroller';
    };

    Scroller.prototype = {
      constructor : Scroller,
      scroll :  function() {
        var that = this,
        parentDivTop = that.parentItem.offset().top,
        windowTop = $(window).scrollTop();

        if(windowTop >= parentDivTop && windowTop < (that.item.closest('.cls_scroller_parent').height() + parentDivTop)) {
          that.item.css({
            'top': (windowTop - parentDivTop) + 53
          })
          that.item.find('.cls_scroller_hiddenDiv').removeClass('hidden');
        } else {
          that.item.css({
            'top': 0
          })
          that.item.find('.cls_scroller_hiddenDiv').addClass('hidden');
        }
      } 
    }


    $.fn.scrollerdiv = function() {
      var that = this;
      that.each(function(index,item){
        var data  = $(item).data('scrollerdiv');
        if(!data) {
          data = new Scroller($(item));
          $(item).data('scrollerdiv',data);
        }
        $(window).scroll(function() { 
          data.scroll();
        });
      })
    }
$(document).ready(function () {
    $('.cls_scroller').scrollerdiv();
});

*/