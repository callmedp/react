import * as Actions from '../actions/actionTypes';

const initState = {
    name : '',
    heading : '',
    slug : '',
    description : '',
    subheading : '',
    breadcrumbs : [],
    skillGainList : [],
    faqList : [],
    whoShouldLearn : '',
    otherSkills : [],
    testimonialCategory : [],
    featuresList : [],
}



export const SkillPageBannerReducer = (state=initState, action) => {
    switch(action.type){
        case Actions.SKILL_PAGE_BANNER_FETCHED : return { ...initState,...action.item}
        
        default: return state;
    }
}