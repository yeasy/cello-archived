/**
 * Created by yuehaitao on 2016/10/30.
 */
import React from 'react'
import { connect } from 'react-redux'
import * as AllActions from '../actions'
import { bindActionCreators } from 'redux'
import PlatformStatus from './platform_status'
import SystemOverview from './system_overview'

var OverView = React.createClass({
    render: function () {
        return (
            <div>
                <SystemOverview/>
                <PlatformStatus/>
            </div>
        )    
    }
});

export default connect(state => ({
    overview: state.overview
}), dispatch => ({
    actions: bindActionCreators(AllActions, dispatch),
    dispatch: dispatch
}))(OverView)
