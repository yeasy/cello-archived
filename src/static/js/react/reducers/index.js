import { combineReducers } from 'redux'
import hosts from '../hosts/reducers/hosts'
import message from '../hosts/reducers/message'

const rootReducer = combineReducers({
    hosts,
    message
});

export default rootReducer
