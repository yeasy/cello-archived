import { combineReducers } from 'redux'
import hosts from '../hosts/reducers/hosts'
import message from '../hosts/reducers/message'
import overview from '../overview/reducers/overview'

const rootReducer = combineReducers({
    hosts,
    message,
    overview
});

export default rootReducer
