import { combineReducers } from 'redux';
import { HomepageReducer } from './HomePage/reducers';

const rootReducer = combineReducers({
    home: HomepageReducer

});


export default rootReducer;
