
const isMobileDevice = (userAgents) => {
    return /Android|Phone|Mobile|Opera\sM(in|ob)i|iP[ao]d|BlackBerry|SymbianOS|Safari\.SearchHelper|SAMSUNG-(GT|C)|WAP|CFNetwork|Puffin|PlayBook|Nokia|LAVA|SonyEricsson|Karbonn|UCBrowser|ucweb|Micromax|Silk|LG(MW|-MMS)|PalmOS/i.test(userAgents)
}

const getDefaultEvents = (data) => {
    const newArr = data.map(v => ({
        ...v,
        source : localStorage.getItem('source') || 'learning',
        device_type : isMobileDevice(navigator.userAgent) ? 'mobile' : 'desktop',
        userID : uId || localStorage.getItem('userId') || '',
        user_type : !!(uId || localStorage.getItem('userId')) ? 'logged_in' : 'non_logged_in',
        timestamp : new Date(),
        learning_session_id : '', 
        shine_t_id : trackingId || '',
        email: localStorage.getItem('userEmail') || email_id
    }))
    return newArr;
}

const addDefaultPayload = (payload) => {
    return getDefaultEvents(payload);
}

const sendLearningTracking = async function (payload) {
    console.log("tracking function fired")
    var superChargedPayload = addDefaultPayload(payload);
    console.log(superChargedPayload)
    console.log("payload is", superChargedPayload)
    const url = `http://34.93.108.100:80/api/v1/core/track`;
    const response = await fetch( url, {
        method: 'POST',
        cache: 'no-cache',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(superChargedPayload)
    })
    console.log("tracking response is", await response.json());
}

