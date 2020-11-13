import { createStore, applyMiddleware, compose } from 'redux';
import rootReducer from './allReducers'
import rootSaga from './sagas'
import createSagaMiddleware from 'redux-saga';



const sagaMiddleware = createSagaMiddleware();



const composeEnhancers = (typeof window !== 'undefined') && window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__ || compose;

// Grab the state from a global variable injected into the server-generated HTML
const preloadedState = window.__PRELOADED_STATE__

// Allow the passed state to be garbage-collected
delete window.__PRELOADED_STATE__

// Create Redux store with initial state
const store = createStore(rootReducer, preloadedState, composeEnhancers(applyMiddleware(sagaMiddleware)));
sagaMiddleware.run(rootSaga);


export default store;
