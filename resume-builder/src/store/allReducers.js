import {combineReducers} from 'redux'

import {reducer as formReducer} from 'redux-form'
import {personalInfoReducer} from './personalInfo/reducer/index'
import {landingPageReducer} from './landingPage/reducer/index'

const allReducer = combineReducers({
    form: formReducer,
    personalInfo: personalInfoReducer,
    home: landingPageReducer
});

export default allReducer;