import { all } from 'redux-saga/effects';
import watchLandingPage from './LandingPage/saga/index'

export default function* rootSaga() {
    yield all([
        watchLandingPage()
    ])
}