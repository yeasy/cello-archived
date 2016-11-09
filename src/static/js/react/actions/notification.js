/**
 * Created by yuehaitao on 2016/10/4.
 */

function notify(messageType, title, message) {
    return dispatch => {
        return new PNotify({
            title: title,
            text: message,
            type: messageType,
            delay: 5000,
            styling: 'bootstrap3'
        })
    }
}

export function notifySuccess(message) {
    return dispatch => {
        dispatch(notify("success", "Success", message))
    }
}

export function notifyError(message) {
    return dispatch => {
        dispatch(notify("error", "Error", message))
    }
}
