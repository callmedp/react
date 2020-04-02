import { combineReducers } from 'redux';
import { uploadFileReducer } from './homePage/reducer/index';

const allReducer = combineReducers({
    uploadFile : uploadFileReducer
})

export default allReducer;