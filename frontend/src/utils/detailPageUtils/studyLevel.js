const STUDY_LEVEL = {
    'BG': 'Beginner',
    'IM': 'Intermediate',
    'AD': 'Advanced',
    '': 'Other'
}

const getStudyLevel = (type) => {
    return STUDY_LEVEL[type]
}

export {
    getStudyLevel
}