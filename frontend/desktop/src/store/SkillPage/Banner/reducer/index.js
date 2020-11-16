import {    SKILL_PAGE_BANNER_FETCHED } from "../actions/actionTypes";
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
}

export const SkillPageBannerReducer = (state=initState, action) => {
    switch(action.type){
        case Actions.SKILL_PAGE_BANNER_FETCHED : return {...state, ...action.item}
        
        default: return state;
    }
}