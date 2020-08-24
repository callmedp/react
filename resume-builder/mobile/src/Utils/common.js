
export const storeTrackingInfo = (trackingId, productTrackingMappingId, productId) => {
    localStorage.setItem("trackingId", trackingId);
    localStorage.setItem("productTrackingMappingId", productTrackingMappingId);
    localStorage.setItem("productId", productId);
}

export const removeTrackingInfo = () => {
    localStorage.removeItem("trackingId");
    localStorage.removeItem("productTrackingMappingId");
    localStorage.removeItem("productId");
    localStorage.removeItem("productPresentInCart");

}

export const isTrackingInfoAvailable = () => {
    return localStorage.getItem("trackingId")
        && localStorage.getItem("productTrackingMappingId")
        && localStorage.getItem("productId")
}


export const getTrackingInfo = () => {
    return {
        "trackingId": localStorage.getItem("trackingId"),
        "productTrackingMappingId": localStorage.getItem("productTrackingMappingId"),
        "productId": localStorage.getItem("productId")
    }
}


export const isProductInCart = () => {
    return !!localStorage.getItem("productPresentInCart");
}


export const updateProductAvailability = (productId) => {
    localStorage.setItem('productPresentInCart', productId)
}
