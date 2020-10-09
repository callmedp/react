import { all } from 'redux-saga/effects';
import watchHomePage from './scorePage/saga/index';

export default function* rootSaga(){
    yield all([
        watchHomePage()
    ])
}