import {all} from 'redux-saga/effects'
import watchPersonalInfo from './personalInfo/saga/index'
import watchLandingPage from './landingPage/saga/index'
import watchExperience from './experience/saga/index'

export default function* () {
    yield all([
        watchPersonalInfo(),
        watchLandingPage(),
        watchExperience()
    ])
}