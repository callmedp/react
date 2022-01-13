import { all } from 'redux-saga/effects'
import WatchHomePage from './HomePage/saga';

export default function* () {
    yield all([
        WatchHomePage()
    ])
}
