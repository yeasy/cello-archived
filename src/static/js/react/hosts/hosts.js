/**
 * Created by yuehaitao on 2016/9/28.
 */
import React from 'react'
var NotificationSystem = require('react-notification-system');
import { connect } from 'react-redux'
import * as AllActions from './actions'
import { bindActionCreators } from 'redux'

var Hosts = React.createClass({
    componentDidMount: function () {
        const {dispatch, actions} = this.props;
        dispatch(actions.setNotification(this.refs.notificationSystem));
    },
    render: function() {
        return (
            <div>
                <NotificationSystem ref="notificationSystem" />
                {this.props.children}
            </div>
        )
    }
});

export default connect(state => ({
    message: state.message
}), dispatch => ({
    actions: bindActionCreators(AllActions, dispatch),
    dispatch: dispatch
}))(Hosts)
