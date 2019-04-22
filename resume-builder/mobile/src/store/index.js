import {createStore, applyMiddleware} from 'redux';
import reducer from './allReducers'
import rootSaga from './sagas'
import createSagaMiddleware from 'redux-saga';
import { composeWithDevTools } from 'redux-devtools-extension';


const sagaMiddleware = createSagaMiddleware();

const store = createStore(
    reducer,
    +window.__REDUX_DEVTOOLS_EXTENSION__ && window.__REDUX_DEVTOOLS_EXTENSION__(),
    composeWithDevTools(
    applyMiddleware(sagaMiddleware))
);

sagaMiddleware.run(rootSaga);


export default store;