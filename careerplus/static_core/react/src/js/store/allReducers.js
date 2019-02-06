import {combineReducers} from 'redux';


import homeReducer from './home/reducer/index';


const allReducer = combineReducers({
    homeReducer
});

export default allReducer;