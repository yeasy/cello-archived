/**
 * Created by yuehaitao on 2016/11/9.
 */
import fetch from 'isomorphic-fetch'
import cookie from 'react-cookie'
import actionTypes from '../constants/actionTypes'
var Urls = require('../constants/Urls');
var Promise = require('es6-promise').Promise;
import {notifySuccess, notifyError} from '../../actions/notification'

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

function releasedCluster(clusterId) {
    return {
        type: actionTypes.released_cluster,
        clusterId: clusterId
    }
}

function clusterOperating(clusterId, inProgress, operation) {
    return {
        type: actionTypes.operating_cluster,
        clusterId: clusterId,
        inProgress: inProgress,
        operation: operation
    }
}

export function operateCluster(clusterId, clusterName, operation) {
    return dispatch => {
        dispatch(clusterOperating(clusterId, true, operation));
        var url = Urls.ClusterOpUrl + "?action=" + operation + "&cluster_id=" + clusterId;
        return {
            type: actionTypes.promise,
            payload: {
                promise: new Promise((resolve, reject) => {
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
                                    switch (operation) {
                                        case "release":
                                            dispatch(releasedCluster(clusterId));
                                            break;
                                        default:
                                            break;
                                    }
                                    dispatch(clusterOperating(clusterId, false, operation));
                                    dispatch(fetchCluster(clusterId));
                                    dispatch(notifySuccess(operation + " " + clusterName + " Success"));
                                });
                        } else if (response.status == 400) {
                            dispatch(notifySuccess(operation + " " + clusterName + " Fail"));
                        }
                    });
                })
            }
        }
    }
}

function fetchedCluster(clusterId, cluster) {
    return {
        type: actionTypes.fetched_cluster,
        clusterId: clusterId,
        cluster: cluster
    }
}

function fetchCluster(clusterId) {
    var url = Urls.ClusterUrl + "/" + clusterId;
    return dispatch => {
        return {
            type: actionTypes.promise,
            payload: {
                promise: new Promise((resolve, reject) => {
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
                                    dispatch(fetchedCluster(clusterId, json.data));
                                });
                        } else if (response.status == 400) {
                        }
                    });
                })
            }
        }
    }
}

function addingCluster(inProgress) {
    return {
        type: actionTypes.adding_cluster,
        inProgress: inProgress
    }
}

export function addChain(chainForm) {
    return dispatch => {
        dispatch(addingCluster(true));
        return {
            type: actionTypes.promise,
            payload: {
                promise: new Promise(() => {
                    fetch(Urls.ClusterUrl, {
                        method: "post",
                        credentials: 'include',
                        headers: {
                            "X-CSRFToken": cookie.load("csrftoken")
                        },
                        body: chainForm
                    }).then(response => {
                        if (response.ok) {
                            response.json()
                                .then(json => {
                                    dispatch(fetchCluster(json.data.cluster_id));
                                    dispatch(addingCluster(false));
                                    dispatch(notifySuccess("add Chain Success"));
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

function removeCluster(clusterId) {
    return {
        type: actionTypes.delete_cluster,
        clusterId: clusterId
    }
}

export function deleteCluster(clusterForm, clusterName) {
    return dispatch => {
        dispatch(clusterOperating(clusterForm.get("id"), true, "delete"));
        return {
            type: actionTypes.promise,
            payload: {
                promise: new Promise(() => {
                    fetch(Urls.ClusterUrl, {
                        method: "delete",
                        credentials: 'include',
                        headers: {
                            "X-CSRFToken": cookie.load("csrftoken")
                        },
                        body: clusterForm
                    }).then(response => {
                        if (response.ok) {
                            response.json()
                                .then(json => {
                                    dispatch(removeCluster(clusterForm.get("id")));
                                    dispatch(notifySuccess("Delete cluster " + clusterName + " success"));
                                })
                        } else if (response.status == 400) {
                            dispatch(notifyError("Delete cluster " + clusterName + " Fail"));
                            dispatch(clusterOperating(clusterForm.get("id"), false, "delete"));
                        }
                    });
                })
            }
        }
    }
}
