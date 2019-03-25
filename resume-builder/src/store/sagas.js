import watchPersonalInfo from './personalInfo/saga/index'

import {call} from 'redux-saga/effects'


export default function*(){
call(watchPersonalInfo)
}