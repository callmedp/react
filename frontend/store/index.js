import rootReducer from './allReducers';
import { createStore } from 'redux';

const store = createStore(rootReducer);


export default store;