import { all } from 'redux-saga/effects';
import watchHomePage from './homePage/saga/index';

export default function* rootSaga(){
    yield all([
        watchHomePage()
    ])
}