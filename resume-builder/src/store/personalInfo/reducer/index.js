import {SAVE_USER_INFO} from "../actions/actionTypes";

const initialState = {
    candidate_id: '',
    first_name: '',
    last_name: '',
    email: '',
    number: '',
    image: '',
    date_of_birth: '',
    location: '',
    gender: '',

};


export const personalInfoReducer = (state = initialState, action) => {
    switch (action.type) {

        case SAVE_USER_INFO: {
            localStorage.setItem('candidateId', action.data && action.data['candidate_id'] || '');
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

