import reducer from './allReducers';
import { createStore, applyMiddleware } from  'redux';
import createSagaMiddleware from 'redux-saga';
import {createMiddleware} from 'redux-beacon';
import GoogleAnalytics from '@redux-beacon/google-analytics';
import {eventsMap} from './googleAnalayticsEventMap';

import rootSaga from './sagas';


const ga = GoogleAnalytics();
const google_analytics_middleware = createMiddleware(eventsMap, ga)
const sagaMiddleware = createSagaMiddleware();


const store = createStore(reducer,applyMiddleware(sagaMiddleware, google_analytics_middleware));
sagaMiddleware.run(rootSaga);


export default store;