/**
 * Created by yuehaitao on 2016/10/4.
 */
import Immutable from 'immutable';
import actionTypes from '../constants/actionTypes'

export default function hosts(state = Immutable.Map({
    hosts: Immutable.Map({}),
    hostsList: Immutable.List([])
}), action) {
    switch (action.type) {
        case actionTypes.fetching_hosts:
            console.log('fetching hosts');
            return state;
        case actionTypes.fetched_hosts:
            state = state.set("hosts", Immutable.fromJS(action.hosts));
            return state;
        default:
            return state;
    }
}
