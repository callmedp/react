import {combineReducers} from 'redux';
import {reducer as formReducer} from 'redux-form'


import {UserReducer} from './userInfo/reducer/index';


const allReducer = combineReducers({
    userInfoReducer: UserReducer.userInfoReducer,
    skill: UserReducer.skillReducer,
    form: formReducer

});

export default allReducer;