import {combineReducers} from 'redux'

import {reducer as formReducer} from 'redux-form'
import {personalInfoReducer} from './personalInfo/reducer/index'

const allReducer = combineReducers({
    form: formReducer,
    personalInfo: personalInfoReducer
});

export default allReducer;