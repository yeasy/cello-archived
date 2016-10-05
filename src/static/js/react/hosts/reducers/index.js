import { combineReducers } from 'redux'
import hosts from './hosts'
import message from './message'

const rootReducer = combineReducers({
    hosts,
    message
});

export default rootReducer
