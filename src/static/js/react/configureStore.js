import { compose, createStore, applyMiddleware } from 'redux'
import thunkMiddleware from 'redux-thunk'
import rootReducer from './reducers'
import { persistState } from 'redux-devtools';
import promiseMiddleware from 'redux-promise-middleware';

const enhancer = compose(
    applyMiddleware(thunkMiddleware, promiseMiddleware()),
    persistState(
        window.location.href.match(
            /[?&]debug_session=([^&]+)\b/
        )
    )
);

export default function configureStore(initialState) {
    const store = createStore(rootReducer, initialState, enhancer);

    if (module.hot) {
        module.hot.accept('../reducers', () =>
            store.replaceReducer(require('../reducers').default)
        );
    }

    return store;
}
