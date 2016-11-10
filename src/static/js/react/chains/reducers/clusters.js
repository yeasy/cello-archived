/**
 * Created by yuehaitao on 2016/11/9.
 */
import Immutable from 'immutable';
import actionTypes from '../constants/actionTypes'

export default function clusters(state = Immutable.Map({
    activeClusters: Immutable.Map({}),
    inUsedClusters: Immutable.Map({}),
    releasedClusters: Immutable.Map({}),
    fetchingClusters: false,
    addingCluster: false
}), action) {
    var activeClusters = state.get("activeClusters");
    switch (action.type) {
        case actionTypes.fetching_clusters:
            return state.set("fetchingClusters", true);
        case actionTypes.fetched_clusters:
            switch (action.clusterType) {
                case "active":
                    state = state.set("activeClusters", Immutable.fromJS(action.clusters));
                    break;
                case "inused":
                    state = state.set("inUsedClusters", Immutable.fromJS(action.clusters));
                    break;
                case "released":
                    state = state.set("releasedClusters", Immutable.fromJS(action.clusters));
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
                case 'inused':
                    state = state.set("inUsedClusters", Immutable.fromJS({}));
                    break;
                case 'released':
                    state = state.set("releasedClusters", Immutable.fromJS({}));
                    break;
                default:
                    break;
            }
            return state;
        case actionTypes.released_cluster:
            activeClusters = activeClusters.update(action.clusterId, (x) => (x.set("user_id", "")));
            return state = state.set("activeClusters", activeClusters);
        case actionTypes.operating_cluster:
            var actionInProgress = "";
            if (action.inProgress) {
                switch (action.operation) {
                    case "release":
                        actionInProgress = "releasing";
                        break;
                    case "start":
                        actionInProgress = "starting";
                        break;
                    case "stop":
                        actionInProgress = "stopping";
                        break;
                    case "restart":
                        actionInProgress = "restarting";
                        break;
                    default:
                        break;
                }
            }
            activeClusters = activeClusters.update(action.clusterId, (x) => (x.set("action", actionInProgress)));
            return state = state.set("activeClusters", activeClusters);
        case actionTypes.fetched_cluster:
            activeClusters = activeClusters.set(action.clusterId, Immutable.fromJS(action.cluster));
            return state.set("activeClusters", activeClusters);
        case actionTypes.adding_cluster:
            return state.set("addingCluster", action.inProgress);
        default:
            return state;
    }
}
