import {FETCH_HOME_DATA, SAVE_USER_DETAILS} from "../actions/actionTypes";

const initialState = {
    firstName: '',
    lastName: '',
    email: '',
    number: ''
};


const homeReducer = (state = initialState, action) => {
    switch (action.type) {
        case FETCH_HOME_DATA: {
            return {
                ...state
            };
        }

        case SAVE_USER_DETAILS: {
            return {
                ...state,
                ...action.data
            };
        }
        default : {
            return state;
        }
    }
};

export default homeReducer;