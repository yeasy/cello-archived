import { combineReducers } from 'redux'
import hosts from '../hosts/reducers/hosts'
import overview from '../overview/reducers/overview'
import clusters from '../chains/reducers/clusters'

const rootReducer = combineReducers({
    hosts,
    overview,
    clusters
});

export default rootReducer
