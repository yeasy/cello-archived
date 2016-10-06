/**
 * Created by yuehaitao on 2016/10/4.
 */
import Immutable from 'immutable';
import actionTypes from '../constants/actionTypes'

export default function hosts(state = Immutable.Map({
    hosts: Immutable.Map({}),
    fetchingHosts: false,
    hostsList: Immutable.List([])
}), action) {
    var hosts = state.get("hosts");
    switch (action.type) {
        case actionTypes.fetching_hosts:
            state = state.set("fetchingHosts", true);
            return state;
        case actionTypes.fetched_hosts:
            state = state.set("fetchingHosts", false);
            state = state.set("hosts", Immutable.fromJS(action.hosts));
            return state;
        case actionTypes.remove_host:
            hosts = hosts.remove(action.hostId);
            state = state.set("hosts", hosts);
            return state;
        case actionTypes.add_host:
            hosts = hosts.merge(Immutable.fromJS(action.host));
            state = state.set("hosts", hosts);
            return state;
        case actionTypes.update_host:
            hosts = hosts.set(action.hostId, Immutable.fromJS(action.host));
            state = state.set("hosts", hosts);
            return state;
        case actionTypes.set_host_action:
            const actionUpdater = (x) => (x.set(action.actionType, action.inAction));
            hosts = hosts.update(action.hostId, actionUpdater);
            state = state.set("hosts", hosts);
            return state;
        default:
            return state;
    }
}
