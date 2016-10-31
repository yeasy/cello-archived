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

module.exports = {
    fetchHosts,
    createHost,
    updateHost,
    deleteHost,
    queryHost,
    hostAction,
    setNotification,
    notifySuccess
};
