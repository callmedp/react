
export const storeTrackingInfo = (trackingId, productTrackingMappingId, productId,
    triggerPoint, uId, position, utmCampaign) => {
    localStorage.setItem("trackingId", trackingId);
    localStorage.setItem("productTrackingMappingId", productTrackingMappingId);
    localStorage.setItem("productId", productId);
    localStorage.setItem("triggerPoint", triggerPoint);
    localStorage.setItem("uId", uId);
    localStorage.setItem("position", position);
    localStorage.setItem("utmCampaign", utmCampaign);
}


export const isTrackingInfoAvailable = () => {
    return localStorage.getItem("trackingId")
        && localStorage.getItem("productTrackingMappingId")
}

export const storeProduct = (productId) => {
    localStorage.setItem("productId", productId);
}


export const getTrackingInfo = () => {
    return {
        "trackingId": localStorage.getItem("trackingId"),
        "productTrackingMappingId": localStorage.getItem("productTrackingMappingId"),
        "productId": localStorage.getItem("productId"),
        "triggerPoint": localStorage.getItem("triggerPoint"),
        "uId": localStorage.getItem("uId"),
        "position": !!localStorage.getItem("position") ? parseInt(localStorage.getItem("position")): '',
        "utmCampaign": localStorage.getItem("utmCampaign")
    }
}


