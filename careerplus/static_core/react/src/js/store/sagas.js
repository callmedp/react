import watchFetchHomeData from './home/saga/index';
import {call} from 'redux-saga/effects';

export default function* () {
    return yield [
        call(watchFetchHomeData)
    ]
}

