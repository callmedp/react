const STUDY_MODE = {
    'OL': 'Online',
    'OF': 'Offline',
    'IL': 'Instructor Led',
    'BL': 'Blended',
    'CA': 'Classroom',
    'CF': 'Certifications',
    'DL': 'Distance Learning',
    '': 'Other'
}

const getStudyMode = (type) => {
    return STUDY_MODE[type]
}

export {
    getStudyMode
}