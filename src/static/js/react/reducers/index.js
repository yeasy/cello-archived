import { combineReducers } from 'redux'
import hosts from '../hosts/reducers/hosts'
import overview from '../overview/reducers/overview'

const rootReducer = combineReducers({
    hosts,
    overview
});

export default rootReducer
