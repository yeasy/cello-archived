import React from 'react'
import { Route, Router, IndexRoute, DefaultRoute, RouterContext } from 'react-router'
import Hosts from './hosts'
import HostTable from './host_table'

export default (
    <Route render={props => <RouterContext {...props} />} path="/" name="Hosts" component={Hosts}>
        <Route name="Index" path="index" component={HostTable} />
        <IndexRoute component={HostTable} />
    </Route>
)
