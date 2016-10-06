import fetch from 'isomorphic-fetch'
import cookie from 'react-cookie'
import actionTypes from '../constants/actionTypes'
var Urls = require('../constants/Urls');
var Promise = require('es6-promise').Promise;

function notifySuccess(message) {
    return {
        type: actionTypes.notify_success,
        message: message
    }
}

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
                            console.log("is bad request");
                        }
                    });
                })
            }
        }
    }
}

export function updateHost(hostForm) {
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
                                console.log(json);
                            })
                    } else if(response.status == 400) {
                        console.log("is bad request");
                    }
                });
            })
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
