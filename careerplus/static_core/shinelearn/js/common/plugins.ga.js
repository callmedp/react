function GA(){
    var that = this;
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
        /*if(switchcase){

            if(path.indexOf('job-search/')>-1){
                action = 'JSRP';
            }else if(path.indexOf('/jobs/')>-1){
                action = 'JD';
            }else if(path.indexOf('/myshine/login')>-1 || path.indexOf('/myshine/home')>-1){
                action = 'HOME';
            }else if(path.indexOf('/jobs/apply/')>-1 || path.indexOf('/ajax/bulk/save/')>-1){
                action = 'JAP';
            }else{
                action = 'Others';
            }

        }*/

        try{

            /*ga('send',type,category,action,label,value,noninteraction,metrics);*/
            //ga('send',type,category,action,label,noninteraction);
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
            ga('set',metricName,metricValue);
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

    that.PageView = function() {
        ga('send', 'pageview');
    };
    that.sendVirtualPage = function(page){
        ga('send', 'pageview',page);
    }


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
    //vars = Array.prototype.slice.call(arguments, 1);
    //return fn.apply(this, vars);
    switch(fn) {
        case 'QueryForm' :  /* Fire event before making ajax from Course Page, Service Page (Have a query?) form */
        case 'CallbackRequested' : /* when user click on call */        
        case 'InboxJobs' :/*When user click on get these jobs jsrp*/

            
            that.fireGaEvent({
                'category': arguments[1],
                'action': arguments[2],
                'label': arguments[3],
                'value': value,
                'noninteraction': noninteraction,
                'name': 'leadform' 
            });
            break;
        
    }


};

var MyGA = new GA();