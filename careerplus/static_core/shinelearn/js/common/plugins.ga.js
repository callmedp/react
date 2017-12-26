function GA(){
    var that = this;
    var trackingId = 'UA-3537905-41';
    that.fireGaEvent = function(options){
        // category,action,label,value,noninteraction,switchcase,metrics
        var path = self.window.location.pathname,
        type = 'event',
        category = options.category || '',
        action = options.action || '',
        label= options.label || '',
        value = options.value || 0,
        noninteraction = options.noninteraction || false,
        switchcase = options.switchcase || false,
        metrics = options.metrics || {},
        name = options.name || '';

        try{
            gtag('event', name, {
              'send_to': ['UA-3537905-41'],
              'event_category': category,
              'event_label': label,
              'event_action':action
            });
        }catch(e)
        {
            try{
                console.log(e);
            }catch(e) {
            }
        }

    };
    that.SetMetrics = function(metricName, metricValue) {
        try{
            gtag('set',metricName,metricValue);
        }catch(e){
            try{
                console.log(e);
            }catch(e) {

            }

        }
    };

    that.PassEvents = function() {
        that.fireGaEvent( $(this).data('category'), $(this).data('action'), $(this).data('label'), 0, true);
    };
    
    that.sendVirtualPage = function(obj){
        var event_id = obj.event || trackingId,
        pageTitle = obj.pageTitle || document.title;
        gtag('event', 'page_view',{'send_to': event_id,'page_title':pageTitle,'page_location':top.window.location.href,'page_path':top.window.location.pathname});
    };

    that.customDimension = function(name, value) {
        gtag('config', trackingId, {
          'custom_map': {name: value}
        });
    };
};
/***Function called for GA Profile***/
GA.prototype.callFromGaParent = function(){
    var that=this;
    $('.cls_gaProfileList').click(function(e) {
        if(e.target.className == 'cls_gaProfileChild') {
            that.SendEvent($(this).data('case'),$(this).data('category'),e.target.dataset.action,$(this).data('label'),0,true)
        }
    });

}

GA.prototype.SendEvent = function() {
    var that = this,
    fn = arguments[0],
    value = "",
    noninteraction = false;
    if(typeof arguments[4] != "undefined") {
        value = arguments[4];
    }
    if(typeof arguments[5] != "undefined") {
        noninteraction = arguments[5];
    }
    name = fn;
    //vars = Array.prototype.slice.call(arguments, 1);
    //return fn.apply(this, vars);
    switch(fn) {
        case 'QueryForm' :  /* Fire event before making ajax from Course Page, Service Page (Have a query?) form */
        case 'CallbackRequested' : /* when user click on call */   
        case 'talenteconomy' : /* talenteconomy navigation click (header->desktop, menu->mobile) */    
        case 'InboxJobs' :/*When user click on get these jobs jsrp*/
        case 'itm' : /* when ever url contains itm parameters */

            
            that.fireGaEvent({
                'category': arguments[1],
                'action': arguments[2],
                'label': arguments[3],
                'value': value,
                'noninteraction': noninteraction,
                'name': fn 
            });
            break;
        
    }


};

var MyGA = new GA();