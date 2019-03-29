import {combineReducers} from 'redux'

import {reducer as formReducer} from 'redux-form'
import {personalInfoReducer} from './personalInfo/reducer/index'
import {landingPageReducer} from './landingPage/reducer/index'
import {experienceReducer} from './experience/reducer/index'

const allReducer = combineReducers({
    form: formReducer,
    personalInfo: personalInfoReducer,
    experience: experienceReducer,
    home: landingPageReducer
});

export default allReducer;