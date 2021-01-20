export const getLearningToken = () => {
    if (localStorage.getItem('learning_token')) return localStorage.getItem('learning_token');
    if (sessionStorage.getItem('learning_token')) return sessionStorage.getItem('learning_token');
    return '';
}


export const getAccessKey = () => {
    if (localStorage.getItem('access_key')) return localStorage.getItem('access_key');
    if (sessionStorage.getItem('access_key')) return sessionStorage.getItem('access_key');
    return '';
}

export const getCandidateId = () => {
    if (!!localStorage.getItem('candidateId')) return localStorage.getItem('candidateId');
    if (!!sessionStorage.getItem('candidateId')) return sessionStorage.getItem('candidateId');
    return false;
}

export const storageTrackingInfo = (query) => {
    let trackingId = !!query["t_id"] ? query["t_id"] : "";
    if (trackingId) {
        localStorage.setItem("trackingId", trackingId);
        localStorage.setItem("productTrackingMappingId", !!query['product_tracking_mapping_id'] ?  query['product_tracking_mapping_id'] : "");
        localStorage.setItem("productId", !!query['prod_id'] ? query['prod_id'] : "");
        localStorage.setItem("triggerPoint", !!query["trigger_point"] ? query["trigger_point"] : "");
        localStorage.setItem("position", !!query["position"] ? query["position"] : "");
        localStorage.setItem("uId", !!query["u_id"] ? query["u_id"] : getCandidateId() );
        localStorage.setItem("utmCampaign", !!query["utm_campaign"] ? query["utm_campaign"] : "" );
        localStorage.setItem("popup_based_product", !!query["popup_based_product"] ? query["popup_based_product"] : "" );
    }
}

export const removeTrackingInfo = () => {
    localStorage.removeItem("trackingId");
    localStorage.removeItem("productTrackingMappingId");
    localStorage.removeItem("productId");
    localStorage.removeItem("position");
    localStorage.removeItem("uId");
    localStorage.removeItem("triggerPoint");
    localStorage.removeItem("utmCampaign");
    localStorage.removeItem("popup_based_product");
}

export const getTrackingInfo = () => {
    if (localStorage.getItem("trackingId", "")){
        return {
            "t_id": localStorage.getItem("trackingId"),
            "product_tracking_mapping_id": localStorage.getItem("productTrackingMappingId"),
            "prod_id": localStorage.getItem("productId"),
            "position": !!localStorage.getItem("position") ? parseInt(localStorage.getItem("position")) : '',
            "u_id": localStorage.getItem("uId"),
            "trigger_point": localStorage.getItem("triggerPoint"),
            "utm_campaign": localStorage.getItem("utmCampaign"),
            "popup_based_product": localStorage.getItem("popup_based_product"),
            // "referal_product": !! localStorage.getItem("referal_product") ? localStorage.getItem("referal_product") : '',
            // "referal_subproduct": !! localStorage.getItem("referal_subproduct") ? localStorage.getItem("referal_subproduct") : ''
        }
    }
    return {}
}

export function getTrackingParameters(tracking_data){
    var url_parameter = ""
    let tracking_id = localStorage.getItem("trackingId","")
    if(tracking_id){
        url_parameter += "?"
        for(var key in tracking_data){
            if(tracking_data[key]){
                url_parameter += (key + "=" + tracking_data[key] + "&")
            }
        }
    }
    return url_parameter
}

export const getDataStorage = (key) => {
    return localStorage.getItem(key) ? localStorage.getItem(key) : getSession(key)
}

const getSession = (name) => {
   return  sessionStorage.getItem(name)
}