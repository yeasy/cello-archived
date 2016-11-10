/**
 * Created by yuehaitao on 2016/11/9.
 */
import Immutable from 'immutable';
import actionTypes from '../constants/actionTypes'

export default function clusters(state = Immutable.Map({
    activeClusters: Immutable.Map({}),
    inuseClusters: Immutable.Map({}),
    fetchingClusters: false
}), action) {
    switch (action.type) {
        case actionTypes.fetching_clusters:
            return state.set("fetchingClusters", true);
        case actionTypes.fetched_clusters:
            switch (action.clusterType) {
                case "active":
                    state = state.set("activeClusters", Immutable.fromJS(action.clusters));
                    break;
                case "inuse":
                    state = state.set("inuseClusters", Immutable.fromJS(action.clusters));
                    break;
                default:
                    break;
            }
            state = state.set("fetchingClusters", false);
            return state;
        case actionTypes.clear_clusters:
            switch (action.clusterType) {
                case 'active':
                    state = state.set("activeClusters", Immutable.fromJS({}));
                    break;
                case 'inuse':
                    state = state.set("inuseClusters", Immutable.fromJS({}));
                    break;
                default:
                    break;
            }
            return state;
        default:
            return state;
    }
}
