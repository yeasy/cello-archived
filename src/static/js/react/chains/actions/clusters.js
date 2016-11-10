/**
 * Created by yuehaitao on 2016/11/9.
 */
import fetch from 'isomorphic-fetch'
import cookie from 'react-cookie'
import actionTypes from '../constants/actionTypes'
var Urls = require('../constants/Urls');
var Promise = require('es6-promise').Promise;

function fetchingClusters() {
    return {
        type: actionTypes.fetching_clusters
    }
}

function fetchedClusters(clusterType, clusters) {
    return {
        type: actionTypes.fetched_clusters,
        clusterType: clusterType,
        clusters: clusters
    }
}

export function fetchClusters(type) {
    return dispatch => {
        dispatch(fetchingClusters());
        return {
            type: actionTypes.promise,
            payload: {
                promise: new Promise((resolve, reject) => {
                    fetch(Urls.ClustersUrl + "?type=" + type, {
                        method: "get",
                        credentials: 'include',
                        headers: {
                            "X-CSRFToken": cookie.load("csrftoken")
                        }
                    }).then(response => {
                        if (response.ok) {
                            response.json()
                                .then(json => {
                                    dispatch(fetchedClusters(type, json.data));
                                });
                        } else if (response.status == 400) {
                        }
                    });
                })
            }
        }
    }
}

export function clearClusters(clusterType) {
    return dispatch => {
        return {
            type: actionTypes.clear_clusters,
            clusterType: clusterType
        }
    }
}
