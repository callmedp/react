import {SAVE_USER_EDUCATION} from "../actions/actionTypes";

const initialState = {
    candidate_id: '',
    id: '',
    specialization: '',
    institution_name: '',
    course_type: '',
    start_date: '',
    percentage_cgpa: '',
    end_date: '',
    is_pursuing: false,
};


export const educationReducer = (state = initialState, action) => {
    switch (action.type) {

        case SAVE_USER_EDUCATION: {
            return {
                ...state,
                ...action.data
            };
        }
        default: {
            return state;
        }
    }
};

