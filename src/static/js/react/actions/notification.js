/**
 * Created by yuehaitao on 2016/10/4.
 */

function notify(messageType, title, message) {
    return dispatch => {
        return new PNotify({
            title: title,
            text: message,
            type: messageType,
            styling: 'bootstrap3'
        })
    }
}

export function notifySuccess(message) {
    return dispatch => {
        dispatch(notify("success", "Success", message))
    }
}
