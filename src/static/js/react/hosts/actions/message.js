/**
 * Created by yuehaitao on 2016/10/4.
 */
import actionTypes from '../constants/actionTypes'

export function setNotification(notificationSystem) {
    return {
        type: actionTypes.set_notification,
        notificationSystem: notificationSystem
    }
}

export function notifySuccess(message) {
    return dispatch => {
        return {
            type: actionTypes.notify_success,
            message: message
        }
    }
}
