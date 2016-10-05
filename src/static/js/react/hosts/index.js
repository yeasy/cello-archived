/**
 * Created by yuehaitao on 16/4/20.
 */

import React from 'react'
import {render} from 'react-dom'
import configureStore from './configureStore'
import { Provider } from 'react-redux'
import { Router, browserHistory, hashHistory } from 'react-router'
import routes from './routes'

const store = configureStore();

render(
    <Provider store={store}>
        <div>
            <Router history={hashHistory}>
                {routes}
            </Router>
        </div>
    </Provider>,
    document.getElementById('hosts'));
