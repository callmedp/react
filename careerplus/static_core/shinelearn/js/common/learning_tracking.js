const _getDefaultEvents = () => {
    return {
        source : localStorage.getItem('source') || '',
        device : isMobileDevice(navigator.userAgent) ? 'mobile' : 'desktop',
        userId : localStorage.getItem('userId') || '',
        userType : !!localStorage.getItem('userId') ? 'logged_in' : '',
        timeStamp : new Date(),
        learning_session_id : '', 
        shine_t_id : ''
    }
}

const _addDefaultPayload = (payload) => {
    return { ..._getDefaultEvents(), ...payload };
}

const sendLearningTracking = function (payload) {
    superChargedPayload = _addDefaultPayload(payload);
    const url = 'https://learning.shine.com/dummy-api/';
    fetch( url, {
        method: 'POST',
        cache: 'no-cache',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(superChargedPayload)
    }).then(response => console.log("Tracking fired", response))
}