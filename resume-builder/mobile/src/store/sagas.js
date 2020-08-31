import {all} from 'redux-saga/effects'
import watchPersonalInfo from './personalInfo/saga/index'
import watchLandingPage from './landingPage/saga/index'
import watchExperience from './experience/saga/index'
import watchEducation from './education/saga/index'
import watchSkill from './skill/saga/index'
import watchLanguage from './language/saga/index'
import watchAward from './award/saga/index'
import watchCourse from './course/saga/index'
import watchProject from './project/saga/index'
import watchReference from './reference/saga/index'
import watchProductId from './buy/saga/index'
import watchTemplate from './template/saga/index'
import watchTracking from './tracking/saga/index'

export default function* () {
    yield all([
        watchPersonalInfo(),
        watchLandingPage(),
        watchExperience(),
        watchEducation(),
        watchSkill(),
        watchLanguage(),
        watchAward(),
        watchCourse(),
        watchProject(),
        watchReference(),
        watchProductId(),
        watchTemplate(),
        watchTracking(),
    ])
}