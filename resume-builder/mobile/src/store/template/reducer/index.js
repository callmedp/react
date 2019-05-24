import {SAVE_TEMPLATE,UPDATE_MODAL_STATUS, SET_CUSTOMIZATION} from "../actions/actionTypes";

const initialState = {
    'html': '',
    'modal_status': false,
    'text_font_size': 1,
    'heading_font_size': 1,
    'color': 1,
    'entity_position': []
};


export const templateReducer = (state = initialState, action) => {
    switch (action.type) {
        case SAVE_TEMPLATE: {
            return {
                ...state,
                ...action.data
            }
        }
        case UPDATE_MODAL_STATUS: {
            return {
                ...state,
                ...action.payload
            }
        }
        case SET_CUSTOMIZATION: {
            return {
                ...state,
                ...action.data
            }
        }
        default: {
            return state;
        }
    }
};

