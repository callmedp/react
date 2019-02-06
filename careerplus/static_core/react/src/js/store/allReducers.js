import {combineReducers} from 'redux';
import {reducer as formReducer} from 'redux-form'


import homeReducer from './home/reducer/index';


const allReducer = combineReducers({
    homeReducer,
    form: formReducer

});

export default allReducer;