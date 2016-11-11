/**
 * Created by yuehaitao on 16/4/22.
 */
import {
    fetchHosts,
    createHost,
    updateHost,
    deleteHost,
    queryHost,
    hostAction
} from '../hosts/actions/host'

import {
    notifySuccess
} from './notification'

import {
    fetchOverview
} from '../overview/actions/overview'

import {
    fetchClusters,
    clearClusters,
    operateCluster,
    addChain,
    fetchCluster,
    deleteCluster
} from '../chains/actions/clusters'

module.exports = {
    fetchHosts,
    createHost,
    updateHost,
    deleteHost,
    queryHost,
    hostAction,
    fetchOverview,
    notifySuccess,
    fetchClusters,
    clearClusters,
    operateCluster,
    addChain,
    fetchCluster,
    deleteCluster
};
