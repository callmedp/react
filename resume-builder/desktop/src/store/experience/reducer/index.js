import {SAVE_USER_EXPERIENCE, REMOVE_EXPERIENCE} from "../actions/actionTypes";

const initialState = {
    list: [{
        job_profile: '',
        company_name: '',
        start_date: '',
        end_date: '',
        is_working: '',
        job_location: '',
        work_description: '',
    }]
};


export const experienceReducer = (state = initialState, action) => {
    switch (action.type) {

        case SAVE_USER_EXPERIENCE: {
            return {
                ...state,
                ...action.data
            };
        }
        case REMOVE_EXPERIENCE: {
            return {
                ...state,
                ...{
                    list: state['list'].filter(item => item.id !== action.id)
                }
            }
        }
        default: {
            return state;
        }
    }
};

