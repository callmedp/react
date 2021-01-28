function GALayer() {
    var that = this;
    var trackingId = 'UA-3537905-41';
    that.fireGaEvent = function(options) {
        var event = options.event || '';
        var product = options.product || [];

        window.dataLayer = window.dataLayer || [];
        
        try{
            console.log('I am being logged');
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
    fn = arguments[0];
    product = [
        {
            'name': 'Programming in HTML5 with JavaScript and CSS3 70-480 Practice Test',
            'id': '12345',
            'price': '999',
            'brand': 'testprep',
            'category': 'IT Language',
            'variant': 'Product',
            'list': 'Search Results',
            'position': 1,
            'dimension15': 'Search page',//Page type (e.g Category page,Product Pages, Homepage, Checkout Pages)
            'dimension16': 'rating',
            'dimension17': 'people bought',
        },
        {
            'name': 'Programming in HTML5 with JavaScript and CSS3 70-480 Practice Test',
            'id': '12345',
            'price': '999',
            'brand': 'testprep',
            'category': 'IT Language',
            'variant': 'Product',
            'list': 'Search Results',
            'position': 1,
            'dimension15': 'Search page',//Page type (e.g Category page,Product Pages, Homepage, Checkout Pages)
            'dimension16': 'rating',
            'dimension17': 'people bought',
        },
        {
            'name': 'Programming in HTML5 with JavaScript and CSS3 70-480 Practice Test',
            'id': '12345',
            'price': '999',
            'brand': 'testprep',
            'category': 'IT Language',
            'variant': 'Product',
            'list': 'Search Results',
            'position': 1,
            'dimension15': 'Search page',//Page type (e.g Category page,Product Pages, Homepage, Checkout Pages)
            'dimension16': 'rating',
            'dimension17': 'people bought',
        },
    ]
    
    that.fireGaEvent({
        'event': 'productImpression',
        'product': product

    })
};

// window.dataLayer = window.dataLayer || [];
// function gtag() { window.dataLayer.push(arguments); }
// gtag('js', new Date());
// gtag('config', 'UA-3537905-41');
// Product impressions are sent by pushing an impressions object
// containing one or more impressionFieldObjects.

var GALayer = new GALayer();