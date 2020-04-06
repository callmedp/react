import {UPDATE_SCORE} from "../actions/actionTypes";

const initialState = {
    score : 70,
    section_score : [
            {section_name : 'Format/Style', section_score : 70, total_section_score: 100, section_description:'Lorem Ipsum hash hash',section_status:1},
            {section_name : 'Objectives', section_score : 60, total_section_score: 100, section_description:'Objective is undefined',section_status:2},
            {section_name : 'Eduction', section_score : 50, total_section_score: 100, section_description:'Education Exists',section_status:3}
    ]
};


export const landingPageReducer = (state = initialState, action) => {
    switch (action.type) {
        case UPDATE_SCORE : {
            return state;
        }
        default: {
            return state;
        }
    }
};
