import * as Actions from '../actions/actionTypes';

const initState = {
    name : '',
    heading : '',
    slug : '',
    description : '',
    subheading : '',
    career_outcomes : '',
    breadcrumbs : [],
    skillGainList : [],
    faqList : [{
        heading : "Question",
        content : "<strong>This is answer</strong>"
    }],
    storiesList : [[{
        userName : "Divyanshu",
        review : "Lorem Ipsum is simply dummy text of the printing \
        and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled.",
        company : "shine, gurugram"},
        {
            userName : "Divyanshu",
            review : "Lorem Ipsum is simply dummy text of the printing \
            and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled.",
            company : "shine, gurugram"},
            {
                userName : "Divyanshu",
                review : "Lorem Ipsum is simply dummy text of the printing \
                and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled.",
                company : "shine, gurugram"}]]
}



export const SkillPageBannerReducer = (state=initState, action) => {
    switch(action.type){
        case Actions.SKILL_PAGE_BANNER_FETCHED : return {...state, ...action.item}
        
        default: return state;
    }
}