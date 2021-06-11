

const isMobileDevice = (userAgents) => {
    return /Android|Phone|Mobile|Opera\sM(in|ob)i|iP[ao]d|BlackBerry|SymbianOS|Safari\.SearchHelper|SAMSUNG-(GT|C)|WAP|CFNetwork|Puffin|PlayBook|Nokia|LAVA|SonyEricsson|Karbonn|UCBrowser|ucweb|Micromax|Silk|LG(MW|-MMS)|PalmOS/i.test(userAgents)
  }
  

export const addDefaultPayload = (payload) => {
    return { ...getDefaultEvents(), ...payload };
}

export const getDefaultEvents = () => {
    return {
        source : localStorage.getItem('source') || '',
        device : isMobileDevice(navigator.userAgent) ? 'mobile' : 'desktop',
        userId : localStorage.getItem('userId') || '',
        userType : !!localStorage.getItem('userId') ? 'logged_in' : 'non_logged_in',
        timeStamp : new Date(),
        learning_session_id : '', 
        tracking_id : ''
    }
}