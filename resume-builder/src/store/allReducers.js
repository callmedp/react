import {combineReducers} from 'redux'

import {reducer as formReducer} from 'redux-form'

const allReducer = combineReducers({
    form: formReducer
});

export default allReducer