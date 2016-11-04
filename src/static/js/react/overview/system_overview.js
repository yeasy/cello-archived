/**
 * Created by yuehaitao on 2016/11/1.
 */
import React from 'react';
import { connect } from 'react-redux'
import * as AllActions from '../actions'
import { bindActionCreators } from 'redux'
import Immutable from 'immutable';
var IoLoadD = require('react-icons/lib/io/load-d');

var SystemOverview = React.createClass({
    componentDidMount: function () {
        const {dispatch, actions} = this.props;
        dispatch(actions.fetchOverview());
    },
    render: function () {
        const {overview} = this.props;
        return(
            <div className="">
                <div className="row top_tiles">
                    <div className="animated flipInY col-lg-3 col-md-3 col-sm-6 col-xs-12">
                        <div className="tile-stats">
                            <div className="icon"><i className="fa fa-caret-square-o-right" /></div>
                            <div className="count">
                                {overview.get("fetchingOverview", false)
                                    ? <IoLoadD className="spin"/>
                                    : overview.get("overview", Immutable.fromJS({})).get("hosts_active", Immutable.fromJS([])).size
                                }
                            </div>
                            <h3>Active Hosts</h3>
                        </div>
                    </div>
                </div>
            </div>
        )
    }
});

export default connect(state => ({
    overview: state.overview
}), dispatch => ({
    actions: bindActionCreators(AllActions, dispatch),
    dispatch: dispatch
}))(SystemOverview)
