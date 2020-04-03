import { UPLOAD_FILE, UPDATE_SCORE } from "../actions/actionTypes";

const initState = {
    score : 67,
    section_score : [
                {section_name : 'Format /Style', section_score : 50, total_section_score : 100, section_description :"Lorem Ipsum", section_status : 1},
                {section_name : 'Summary & Objective', section_score : 60, total_section_score : 100, section_description :"Lorem Ipsum", section_status : 1},
                {section_name : 'Accomplishments', section_score : 65, total_section_score : 100, section_description :"Lorem Ipsum", section_status : 2},
                {section_name : 'Education Details', section_score : 55, total_section_score : 100, section_description :"Lorem Ipsum", section_status : 1},
                {section_name : 'Work Experience', section_score : 38, total_section_score : 100, section_description :"Lorem Ipsum", section_status : 3},
                {section_name : 'Skills', section_score : 80, total_section_score : 100, section_description :"Lorem Ipsum", section_status : 3},
                {section_name : 'Contact Details', section_score : 80, total_section_score : 100, section_description :"Lorem Ipsum", section_status : 1}
            ]
};

export const uploadFileReducer = (state = initState, action) => {
    switch( action.type ){
        case UPDATE_SCORE :{
            return {
                ...state,
                ...{
                    score : action.score,
                    section_score : action.section_score
                }
            }
        }

        case UPLOAD_FILE :{
            return state
        }
        default : return state;
    }
}