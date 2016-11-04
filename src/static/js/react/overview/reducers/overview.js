/**
 * Created by yuehaitao on 2016/10/31.
 */
import Immutable from 'immutable';
import actionTypes from '../constants/actionTypes'

export default function overview(state = Immutable.Map({
    fetchingOverview: false,
    overview: Immutable.fromJS({})
}), action) {
    switch (action.type) {
        case actionTypes.fetching_overview:
            state = state.set("fetchingOverview", true);
            return state;
        case actionTypes.fetched_overview:
            state = state.set("overview", Immutable.fromJS(action.overview));
            state = state.set("fetchingOverview", false);
            return state;
        default:
            return state;
    }
}
