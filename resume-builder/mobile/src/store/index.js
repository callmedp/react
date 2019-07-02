import {createStore, applyMiddleware} from 'redux';
import reducer from './allReducers'
import rootSaga from './sagas'
import createSagaMiddleware from 'redux-saga';
import { composeWithDevTools } from 'redux-devtools-extension';
import { createMiddleware } from 'redux-beacon';
import GoogleAnalytics from '@redux-beacon/google-analytics';
import {eventsMap} from './googleAnalayticsEventMap';

const ga = GoogleAnalytics();
const google_analytics_middleware = createMiddleware(eventsMap, ga)
const sagaMiddleware = createSagaMiddleware();

const store = createStore(
    reducer,
    +window.__REDUX_DEVTOOLS_EXTENSION__ && window.__REDUX_DEVTOOLS_EXTENSION__(),
    composeWithDevTools(
    applyMiddleware(sagaMiddleware,google_analytics_middleware))
);

sagaMiddleware.run(rootSaga);


export default store;