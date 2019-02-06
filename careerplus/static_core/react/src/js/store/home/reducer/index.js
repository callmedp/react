import {FETCH_HOME_DATA, SAVE_HOME_DATA} from "../actions/actionTypes";

const initialState = {
    "location": "Delhi",
    "pinCode": 110064,
    "state": "Delhi"
}


const homeReducer = (state = initialState, action) => {
    switch (action.type) {
        case FETCH_HOME_DATA: {
            return {
                ...state
            };
        }

        case SAVE_HOME_DATA: {
            return {
                ...state,
                ...action.data
            };
        }
        default : {
            return state;
        }
    }
}


export default homeReducer;