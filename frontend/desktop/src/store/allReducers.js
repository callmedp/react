import { combineReducers } from 'redux';
import { NeedHelpReducer } from './NeedHelp/reducer';



const rootReducer = combineReducers({
    needHelp : NeedHelpReducer
});


export default rootReducer;