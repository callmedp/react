import {FETCH_HOME_DATA, STORE_USER_INFO} from "../actions/actionTypes";

const initialState = {
    first_name: '',
    last_name: '',
    email: '',
    number: ''
};


const userInfoReducer = (state = initialState, action) => {
    switch (action.type) {
        case FETCH_HOME_DATA: {
            return {
                ...state
            };
        }

        case STORE_USER_INFO: {
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

export default userInfoReducer;