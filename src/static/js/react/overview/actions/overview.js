/**
 * Created by yuehaitao on 2016/10/31.
 */
import fetch from 'isomorphic-fetch'
import cookie from 'react-cookie'
import actionTypes from '../constants/actionTypes'
var Urls = require('../constants/Urls');
var Promise = require('es6-promise').Promise;

function fetchedOverview(overview) {
    return {
        type: actionTypes.fetched_overview,
        overview: overview
    }
}

function fetchingOverview() {
    return {
        type: actionTypes.fetching_overview
    }
}

export function fetchOverview() {
    return dispatch => {
        dispatch(fetchingOverview());
        return {
            type: actionTypes.promise,
            payload: {
                promise: new Promise((resolve, reject) => {
                    fetch(Urls.OverviewUrl, {
                        method: "get",
                        credentials: 'include',
                        headers: {
                            "X-CSRFToken": cookie.load("csrftoken")
                        }
                    }).then(response => {
                        if (response.ok) {
                            response.json()
                                .then(json => {
                                    dispatch(fetchedOverview(json));
                                });
                        }
                    });
                })
            }
        }
    }
}
