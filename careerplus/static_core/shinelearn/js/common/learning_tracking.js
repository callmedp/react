
const isMobileDevice = (userAgents) => {
    return /Android|Phone|Mobile|Opera\sM(in|ob)i|iP[ao]d|BlackBerry|SymbianOS|Safari\.SearchHelper|SAMSUNG-(GT|C)|WAP|CFNetwork|Puffin|PlayBook|Nokia|LAVA|SonyEricsson|Karbonn|UCBrowser|ucweb|Micromax|Silk|LG(MW|-MMS)|PalmOS/i.test(userAgents)
}

const getDefaultEvents = () => {
    return {
        source : localStorage.getItem('source') || '',
        device_type : isMobileDevice(navigator.userAgent) ? 'mobile' : 'desktop',
        userID : uId || localStorage.getItem('userId') || '',
        user_type : !!(uId || localStorage.getItem('userId')) ? 'logged_in' : 'non_logged_in',
        timestamp : new Date(),
        learning_session_id : '', 
        shine_t_id : trackingId || '',
        email: localStorage.getItem('userEmail')
    }
}

const addDefaultPayload = (payload) => {
    return { ...getDefaultEvents(), ...payload };
}

const sendLearningTracking = function (payload) {
    console.log("tracking function fired")
    var superChargedPayload = addDefaultPayload(payload);
    console.log("payload is", superChargedPayload)
    const url = `${site_domain}/dummy-api/`;
    fetch( url, {
        method: 'POST',
        cache: 'no-cache',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(superChargedPayload)
    }).then(response => console.log("Tracking fired", response.json()))
}


console.log("learning tracking is initialized")