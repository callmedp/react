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