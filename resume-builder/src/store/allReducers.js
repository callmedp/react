import {combineReducers} from 'redux'

import {reducer as formReducer} from 'redux-form'
import {personalInfoReducer} from './personalInfo/reducer/index'
import {landingPageReducer} from './landingPage/reducer/index'
import {experienceReducer} from './experience/reducer/index'
import {educationReducer} from './education/reducer/index'
import {skillReducer} from './skill/reducer/index'
import {languageReducer} from './language/reducer/index'
import {awardReducer} from './award/reducer/index'
import {courseReducer} from './course/reducer/index'
import {projectReducer} from './project/reducer/index'
import {referenceReducer} from './reference/reducer/index'
import {getProductIdsReducer} from './buy/reducer/index'
import {templateReducer} from './template/reducer/index'

const allReducer = combineReducers({
        form: formReducer,
        personalInfo: personalInfoReducer,
        experience: experienceReducer,
        education: educationReducer,
        skill: skillReducer,
        language: languageReducer,
        home: landingPageReducer,
        award: awardReducer,
        course: courseReducer,
        project: projectReducer,
        reference: referenceReducer,
        productIds: getProductIdsReducer,
        template: templateReducer
    })
;

export default allReducer;