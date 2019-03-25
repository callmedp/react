import {call} from 'redux-saga/effects'
import watchPersonalInfo from './personalInfo/saga/index'

export default function*(){
    yield call(watchPersonalInfo)
}