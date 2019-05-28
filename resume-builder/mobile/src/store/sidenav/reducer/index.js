import {UPDATE_SIDENAV_STATUS,UPDATE_LIST_LINK,UPDATE_CURRENT_LINK_POS} from "../actions/actionTypes";

const initialState = {
    sidenavStatus : false,
    listOfLinks : ['profile','education','skill'],
    currentLinkPos : 0
};


export const sidenavReducer = (state = initialState, action) => {
    switch (action.type) {

        case UPDATE_SIDENAV_STATUS: {
            return {
                ...state,
                ...{sidenavStatus:action.payload}
            };
        }
        case UPDATE_LIST_LINK: {
            return {
                ...state,
                ...action.payload
            }
        }
        case UPDATE_CURRENT_LINK_POS: {
            return {
                ...state,
                ...action.payload
            }
        }
        default: {
            return state;
        }
    }
};

