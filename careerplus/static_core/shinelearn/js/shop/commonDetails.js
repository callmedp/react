
const makeTrackingRequest = (loggingData) => {

    $.ajax({
        method: "POST",
        url: `${shineApiUrl}/learning-touchpoints-tracking/`,
        data: JSON.stringify(loggingData),
        contentType: "application/json",
    })
}


function handleTracking(action) {
    let loggingData = { t_id: trackingId, products: [productTrackingMappingId], action: action, 'position': parseInt(position), domain: 2, sub_product: trackingProductId, trigger_point: triggerPoint, u_id: uId, utm_campaign: utmCampaign};
    if (trackingId && trackingProductId === productId){
        makeTrackingRequest(loggingData);
    }
}

function trackClickEvent() {
    // exit product page handling 
    let loggingData = { t_id: trackingId, products: [productTrackingMappingId], action: 'exit_product_page', 'position': 1, domain: 2, sub_product: trackingProductId, trigger_point: triggerPoint, u_id: uId, utm_campaign: utmCampaign};
    if (trackingId && trackingProductId === productId ){
        makeTrackingRequest(loggingData);
    }
}
