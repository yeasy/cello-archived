/**
 * Created by yuehaitao on 16/4/22.
 */
import {
    fetchHosts,
    createHost,
    updateHost,
    deleteHost
} from './host'

import {
    setNotification,
    notifySuccess
} from './message'

module.exports = {
    fetchHosts,
    createHost,
    updateHost,
    deleteHost,
    setNotification,
    notifySuccess
};
