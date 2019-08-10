import {createStore, applyMiddleware, compose} from 'redux';
import reducer from './allReducers'
import rootSaga from './sagas'
import createSagaMiddleware from 'redux-saga';
import {createMiddleware} from 'redux-beacon';
import GoogleAnalytics from '@redux-beacon/google-analytics';
import {eventsMap} from './googleAnalayticsEventMap';

const ga = GoogleAnalytics();
const google_analytics_middleware = createMiddleware(eventsMap, ga)
const sagaMiddleware = createSagaMiddleware();

const composeEnhancers = (typeof window !== 'undefined') && window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__ || compose;

const store = createStore(reducer, composeEnhancers(
    applyMiddleware(sagaMiddleware, google_analytics_middleware)));
sagaMiddleware.run(rootSaga);


export default store;