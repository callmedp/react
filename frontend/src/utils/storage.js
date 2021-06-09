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
    if (!!localStorage.getItem('candidate_id')) return localStorage.getItem('candidate_id');
    if (!!sessionStorage.getItem('candidateId')) return sessionStorage.getItem('candidateId');
    if (!!sessionStorage.getItem('candidate_id')) return sessionStorage.getItem('candidate_id');

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
        localStorage.setItem("recommendation_by", !!query["recommendation_by"] ? query["recommendation_by"] : "")
        localStorage.setItem("cart_addition", !!query["cart_addition"] ? query["cart_addition"] : "")
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
    localStorage.removeItem("recommendation_by");
    localStorage.removeItem("cart_addition");
}

export const getTrackingUrl = () => {
    if (localStorage.getItem("trackingId", "")){
        var t_id = localStorage.getItem("trackingId");
        var prod_id = localStorage.getItem("productId");
        var product_tracking_mapping_id = localStorage.getItem("productTrackingMappingId");
        var position =!!localStorage.getItem("position") ? parseInt(localStorage.getItem("position")) : '';
        var u_id = localStorage.getItem("uId");
        var trigger_point = localStorage.getItem("triggerPoint");
        var utm_campaign = localStorage.getItem("utmCampaign");
        var popup_based_product =  localStorage.getItem("popup_based_product");
        var referal_product =  !! localStorage.getItem("referal_product") ? localStorage.getItem("referal_product") : '';
        var referal_subproduct = !! localStorage.getItem("referal_subproduct") ? localStorage.getItem("referal_subproduct") : '';
        var recommendation_by = !! localStorage.getItem("recommendation_by") ? localStorage.getItem("recommendation_by") : '';
        var cart_addition = !! localStorage.getItem("cart_addition") ? localStorage.getItem("cart_addition") : '';

        var tracking_url = `?t_id=${t_id}`;
        if(prod_id) tracking_url += `&t_prod_id=${prod_id}`;
        if(product_tracking_mapping_id) tracking_url += `&prod_t_m_id=${product_tracking_mapping_id}`;
        if(u_id) tracking_url += `&u_id=${u_id}`;
        if(position) tracking_url += `&position=${position}`;
        if(trigger_point) tracking_url += `&trigger_point=${trigger_point}`;
        if(utm_campaign) tracking_url += `&utm_campaign=${utm_campaign}`;
        if(popup_based_product) tracking_url += `&popup_based_product=${popup_based_product}`;
        if(recommendation_by) tracking_url += `&recommendation_by=${recommendation_by}`;
        if(cart_addition) tracking_url += `&cart_addition=${cart_addition}`;
        if(referal_product) tracking_url += `&referal_product=${referal_product}`;
        if(referal_subproduct) tracking_url += `&referal_subproduct=${referal_subproduct}`;

        return tracking_url;
    }
    return ""
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
            "recommendation_by": localStorage.getItem("recommendation_by"),
            "cart_addition": localStorage.getItem("cart_addition"),
            "referal_product": !! localStorage.getItem("referal_product") ? localStorage.getItem("referal_product") : '',
            "referal_subproduct": !! localStorage.getItem("referal_subproduct") ? localStorage.getItem("referal_subproduct") : ''
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


export const getCandidateInformation = () => {
    return {
        candidateId: getCandidateId() || '',
        name: localStorage.getItem('userName') || '',
        lastname: localStorage.getItem('lastName') || '',
        email: localStorage.getItem('userEmail') || '',
        mobile:  localStorage.getItem('mobile') || '',
    }
}

export const CountryCode2 = () => {
    if (localStorage.getItem('code2')) return localStorage.getItem('code2');
    if (sessionStorage.getItem('code2')) return sessionStorage.getItem('code2');
    return false;
}