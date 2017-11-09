function GA(){
    var that = this;
    that.fireGaEvent = function(category,action,label,value,noninteraction,switchcase,metrics){

        var path = self.window.location.pathname;
        type = 'event';
        category = category || '';
        action = action || '';
        label= label || '';
        value = value || 0;
        noninteraction = noninteraction || false;
        switchcase = switchcase || false;
        metrics = metrics || {};
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
            ga('send',type,category,action,label,noninteraction);
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
    var that = this;
    var fn = arguments[0];
    //vars = Array.prototype.slice.call(arguments, 1);
    //return fn.apply(this, vars);
    switch(fn) {
        case 'QueryForm' :  /* Fire event before making ajax from Course Page, Service Page (Have a query?) form */
            
        case 'InboxJobs' :/*When user click on get these jobs jsrp*/

            var value = "",
            noninteraction = false;
            if(typeof arguments[4] != "undefined") {
                value = arguments[4];
            }
            if(typeof arguments[5] != "undefined") {
                noninteraction = arguments[5];
            }

            that.fireGaEvent(arguments[1],arguments[2],arguments[3],value,noninteraction);
            break;
        
    }


};

var MyGA = new GA();