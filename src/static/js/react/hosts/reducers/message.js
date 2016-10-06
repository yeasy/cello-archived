/**
 * Created by yuehaitao on 2016/10/4.
 */
import Immutable from 'immutable';
import actionTypes from '../constants/actionTypes'

export default function message(state = Immutable.Map({
    notificationSystem: null
}), action) {
    switch (action.type) {
        case actionTypes.set_notification:
            state = state.set("notificationSystem", action.notificationSystem);
            return state;
        case actionTypes.notify_success:
            var notificationSystem = state.get("notificationSystem");
            notificationSystem.addNotification({
                title: 'Success',
                message: action.message,
                level: 'success'
            });
            return state;
        default:
            return state;
    }
}
