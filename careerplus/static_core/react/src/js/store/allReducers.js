import {combineReducers} from 'redux';
import {reducer as formReducer} from 'redux-form'


import userInfoReducer from './userInfo/reducer/index';


const allReducer = combineReducers({
    userInfoReducer,
    form: formReducer

});

export default allReducer;