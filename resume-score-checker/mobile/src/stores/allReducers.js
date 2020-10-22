import { combineReducers } from 'redux';
import { uploadFileReducer } from './scorePage/reducer/index';

const allReducer = combineReducers({
    uploadFile : uploadFileReducer
})

export default allReducer;