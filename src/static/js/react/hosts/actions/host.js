import fetch from 'isomorphic-fetch'
import cookie from 'react-cookie'
import Immutable from 'immutable'
import actionTypes from '../constants/actionTypes'
var Urls = require('../constants/Urls');
var Promise = require('es6-promise').Promise;
import notifySucces from './message'

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
    return {
        type: actionTypes.create_host,
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
