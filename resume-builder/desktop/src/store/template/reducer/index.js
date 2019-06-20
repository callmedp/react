import {
    FETCH_TEMPLATE,
    SAVE_TEMPLATE,
    SET_SELECTED_TEMPLATE,
    SET_CUSTOMIZATION,
    SAVE_TEMPLATE_IMAGES,
    SAVE_THUMBNAIL_IMAGES
} from "../actions/actionTypes";

const initialState = {
    'html': '',
    'template': 1,
    'templateId': 1,
    'text_font_size': 1,
    'heading_font_size': 1,
    'color': 1,
    'entity_position': [],
    'templateImage': '',
    'modalTemplateImage': '',
    'thumbnailImages': [],
    'templateToPreview': ''

};


export const templateReducer = (state = initialState, action) => {
    switch (action.type) {
        case FETCH_TEMPLATE: {
            return {
                ...state,
                ...action.data
            }
        }
        case SAVE_TEMPLATE: {
            return {
                ...state,
                ...action.data
            }
        }
        case SET_CUSTOMIZATION: {
            return {
                ...state,
                ...action.data
            }
        }
        case SAVE_TEMPLATE_IMAGES: {
            return {
                ...state,
                ...action.data
            }
        }

        case SAVE_THUMBNAIL_IMAGES: {
            return {
                ...state,
                ...action.data
            }
        }

        case SET_SELECTED_TEMPLATE: {
            return {
                ...state,
                ...{
                    templateId: action.templateId
                }
            }
        }
        default: {
            return state;
        }
    }
};

