import fetch from 'isomorphic-fetch'
import cookie from 'react-cookie'
import actionTypes from '../constants/actionTypes'
var Urls = require('../constants/Urls');
var Promise = require('es6-promise').Promise;
import {notifySuccess, notifyError} from '../../actions/notification'

function setFetchingHosts() {
    return {
        type: actionTypes.fetching_hosts
    }
}

function fetchedHosts(hosts) {
    return {
        type: actionTypes.fetched_hosts,
        hosts: hosts
    }
}

function removeHost(hostId) {
    return {
        type: actionTypes.remove_host,
        hostId: hostId
    }
}

function addHost(host) {
    return {
        type: actionTypes.add_host,
        host: host
    }
}

function setHostAction(hostId, inAction, actionType) {
    return {
        type: actionTypes.set_host_action,
        hostId: hostId,
        inAction: inAction,
        actionType: actionType
    }
}

function updateSpecialHost(hostId, host) {
    return {
        type: actionTypes.update_host,
        hostId: hostId,
        host: host
    }
}

export function fetchHosts() {
    return dispatch => {
        dispatch(setFetchingHosts());
        return {
            type: actionTypes.promise,
            payload: {
                promise: new Promise((resolve, reject) => {
                    fetch(Urls.HostsUrl, {
                        method: "get",
                        credentials: 'include',
                        headers: {
                            "X-CSRFToken": cookie.load("csrftoken")
                        }
                    }).then(response => {
                        if (response.ok) {
                            response.json()
                                .then(json => {
                                    dispatch(fetchedHosts(json.hosts));
                                });
                        } else if (response.status == 400) {
                        }
                    });
                })
            }
        }
    }
}

export function createHost(hostForm) {
    return dispatch => {
        return {
            type: actionTypes.promise,
            payload: {
                promise: new Promise(() => {
                    fetch(Urls.HostUrl, {
                        method: "post",
                        credentials: 'include',
                        headers: {
                            "X-CSRFToken": cookie.load("csrftoken")
                        },
                        body: hostForm
                    }).then(response => {
                        if (response.ok) {
                            response.json()
                                .then(json => {
                                    dispatch(addHost(json.data));
                                    dispatch(notifySuccess("Create Host success"));
                                })
                        } else if (response.status == 400) {
                            dispatch(notifyError("Create Host Fail"));
                        }
                    });
                })
            }
        }
    }
}

export function updateHost(hostForm) {
    return dispatch => {
        return {
            type: actionTypes.promise,
            payload: {
                promise: new Promise(() => {
                    fetch(Urls.HostUrl, {
                        method: "put",
                        credentials: 'include',
                        headers: {
                            "X-CSRFToken": cookie.load("csrftoken")
                        },
                        body: hostForm
                    }).then(response => {
                        if (response.ok) {
                            response.json()
                                .then(json => {
                                    dispatch(updateSpecialHost(json.host_id, json.data));
                                    dispatch(notifySuccess("Update host " + json.host_id + " success"));
                                })
                        } else if (response.status == 400) {
                            dispatch(notifyError("Update Host Fail"));
                        }
                    });
                })
            }
        }
    }
}

export function deleteHost(hostForm, hostId) {
    return dispatch => {
        return {
            type: actionTypes.promise,
            payload: {
                promise: new Promise(() => {
                    fetch(Urls.HostUrl, {
                        method: "delete",
                        credentials: 'include',
                        headers: {
                            "X-CSRFToken": cookie.load("csrftoken")
                        },
                        body: hostForm
                    }).then(response => {
                        if (response.ok) {
                            response.json()
                                .then(json => {
                                    dispatch(removeHost(hostId));
                                    dispatch(notifySuccess("Remove " + hostId + " success"))
                                })
                        } else if (response.status == 400) {
                            console.log("is bad request");
                        }
                    });
                })
            }
        }
    }
}

export function hostAction(hostForm, hostId, actionType) {
    return dispatch => {
        dispatch(setHostAction(hostId, true, actionType));
        return {
            type: actionTypes.promise,
            payload: {
                promise: new Promise(() => {
                    fetch(Urls.HostActionUrl, {
                        method: "post",
                        credentials: 'include',
                        headers: {
                            "X-CSRFToken": cookie.load("csrftoken")
                        },
                        body: hostForm
                    }).then(response => {
                        if (response.ok) {
                            response.json()
                                .then(json => {
                                    dispatch(setHostAction(hostId, false, actionType));
                                    dispatch(queryHost(hostId));
                                })
                        } else if (response.status == 400) {
                            console.log("is bad request");
                        }
                    });
                })
            }
        }
    }
}

export function queryHost(hostId) {
    var url = Urls.HostUrl + '/' + hostId;
    return dispatch => {
        return {
            type: actionTypes.promise,
            payload: {
                promise: new Promise(() => {
                    fetch(url, {
                        method: "get",
                        credentials: 'include',
                        headers: {
                            "X-CSRFToken": cookie.load("csrftoken")
                        }
                    }).then(response => {
                        if (response.ok) {
                            response.json()
                                .then(json => {
                                    dispatch(updateSpecialHost(hostId, json));
                                })
                        } else if (response.status == 400) {
                            console.log("is bad request");
                        }
                    });
                })
            }
        }
    }
}
