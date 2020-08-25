import { SAVE_USER_INFO, SAVE_INTEREST_LIST, UPDATE_SUMMARY_WITH_SUGGESTION } from "../actions/actionTypes";

const initialState = {
    active_subscription: false,
    candidate_id: '',
    id: 0,
    first_name: '',
    last_name: '',
    email: '',
    number: '',
    image: '',
    date_of_birth: '',
    location: '',
    gender: {},
    extracurricular: [],
    extra_info: '',
    entity_preference_data: [],
    interest_list: [],
    selected_template: '',
    free_resume_downloads: 0
};


export const personalInfoReducer = (state = initialState, action) => {
    switch (action.type) {

        case SAVE_USER_INFO: {
            return {
                ...state,
                ...action.data,
            };
        }
        case SAVE_INTEREST_LIST: {
            return {
                ...state,
                ...{
                    interest_list: action.data
                }
            }
        }
        case UPDATE_SUMMARY_WITH_SUGGESTION: {
            return {
                ...state,
                ...{
                    extra_info: action.payload
                }
            }
        }
        default: {
            return state;
        }
    }
};

