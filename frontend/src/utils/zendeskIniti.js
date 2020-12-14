const initZendesk = (candidateDetails) => {
    if (candidateDetails) {
        const full_name = candidateDetails?.full_name;
        const  email = candidateDetails?.email;
        const mobile_no = candidateDetails?.mobile_no;
    
        window && window.$zopim &&  window.$zopim(function () {
            window.$zopim.livechat.set({
                language: 'en',
                name: full_name ? full_name.charAt(0).toUpperCase() + full_name.slice(1): '',
                email: email ? email : '',
                phone: mobile_no ? mobile_no : ''
            });                
        });
    }
}

export default initZendesk;