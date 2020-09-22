$(document).ready(function () {

    $('#myCarousel1').carousel({
        interval: 4000,
    });

    $('#carousel-example-generic1').carousel({
        interval: 100000
    })

    $('.nav-tabs > li > a').hover(function () {
        $(this).tab('show');
    })


    jQuery.ajaxPrefilter(function (s) {
        if (s.crossDomain) {
            s.contents.script = false;
        }
    });

})



const makeTrackingRequest = (loggingData) => {

    $.ajax({
        method: "POST",
        url: `${shineApiUrl}/learning-touchpoints-tracking/`,
        data: JSON.stringify(loggingData),
        contentType: "application/json",
    })
}

const homepageTracking = (action) => {
    let loggingData = { t_id: trackingId, products: [productTrackingMappingId], action: action, 
        'position': parseInt(position), domain: 2, sub_product: trackingProductId, trigger_point : triggerPoint, u_id : uId, utm_campaign : utmCampaign };
    if (trackingId) {
        if(referal_product){
            let loggingData = { t_id: trackingId, products: [productTrackingMappingId], action: action, 
        'position': parseInt(position), domain: 2, sub_product: trackingProductId, trigger_point : triggerPoint, u_id : uId, utm_campaign : utmCampaign, referral_product: parseInt(referal_product), referal_subproduct:referal_subproduct};
         makeTrackingRequest(loggingData);
        }else{
        makeTrackingRequest(loggingData);}
    }
}

const trackClickEvent = () => {
    let loggingData = { t_id: trackingId, products: [productTrackingMappingId], action: 'exit_home_page', 
    'position': parseInt(position), domain: 2, sub_product: trackingProductId, trigger_point : triggerPoint, u_id : uId, utm_campaign : utmCampaign };
    if (trackingId) {
        if(referal_product){
            let loggingData = { t_id: trackingId, products: [productTrackingMappingId], action: 'exit_home_page', 
        'position': parseInt(position), domain: 2, sub_product: trackingProductId, trigger_point : triggerPoint, u_id : uId, utm_campaign : utmCampaign, referral_product: parseInt(referal_product), referal_subproduct:referal_subproduct};
         makeTrackingRequest(loggingData);
        }else{
        makeTrackingRequest(loggingData);}
    }
}