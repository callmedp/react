function GALayer() {
    var that = this;
    var trackingId = 'UA-3537905-41';
    that.fireGaEvent = function(options) {
        var event = options.event || '';
        var product = options.product || [];
        currencyCode = options.currencyCode || 'INR';

        window.dataLayer = window.dataLayer || [];
        
        try{
            console.log(product);
            window.dataLayer.push({
                "event": event,
                'ecommerce': {
                    'currencyCode': 'INR',
                    'impressions': product
                }
            });


        }
        catch(e) {
            console.log(e)
        }
    }
    that.customDimension = function(name, value) {
        gtag('config', trackingId, {
          'custom_map': {name: value}
        });
    };
};

GALayer.prototype.SendImpression = function() {
    var that = this;
    eventName = arguments[0];
    ecommerce = arguments[1];
    currencyCode = arguments[2];
    
    that.fireGaEvent({
        'event': eventName,
        'product': ecommerce,
        'currencyCode': currencyCode
    })
};

// window.dataLayer = window.dataLayer || [];
// function gtag() { window.dataLayer.push(arguments); }
// gtag('js', new Date());
// gtag('config', 'UA-3537905-41');
// Product impressions are sent by pushing an impressions object
// containing one or more impressionFieldObjects.

var GALayer = new GALayer();