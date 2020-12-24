const getWhatsAppNo = (pageType, whatsappDict) =>{
    var whatsappNo = ''
    if(pageType === 'skill'){
        whatsappNo = whatsappDict?.course_skill_visibility ? whatsappDict?.course_skill_number : ''
    }

    return whatsappNo
}

export {
    getWhatsAppNo
}