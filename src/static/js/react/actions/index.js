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
    setNotification,
    notifySuccess
} from '../hosts/actions/message'

import {
    fetchOverview
} from '../overview/actions/overview'

module.exports = {
    fetchHosts,
    createHost,
    updateHost,
    deleteHost,
    queryHost,
    hostAction,
    setNotification,
    fetchOverview,
    notifySuccess
};
