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
                <div className="row tile_count">
                    <div className="col-md-2 col-sm-4 col-xs-6 tile_stats_count">
                        <span className="count_top green">Active Hosts</span>
                        <div className="count green">
                            {overview.get("fetchingOverview", false)
                                ? <IoLoadD className="spin"/>
                                : overview.get("overview", Immutable.fromJS({})).get("hosts_active", Immutable.fromJS([])).size
                            }
                        </div>
                    </div>
                    <div className="col-md-2 col-sm-4 col-xs-6 tile_stats_count">
                        <span className="count_top">Avaliable Hosts</span>
                        <div className="count">
                            {overview.get("fetchingOverview", false)
                                ? <IoLoadD className="spin"/>
                                : overview.get("overview", Immutable.fromJS({})).get("hosts_available", Immutable.fromJS([])).size
                            }
                        </div>
                    </div>
                    <div className="col-md-2 col-sm-4 col-xs-6 tile_stats_count">
                        <span className="count_top red">Inactive Hosts</span>
                        <div className="count red">
                            {overview.get("fetchingOverview", false)
                                ? <IoLoadD className="spin"/>
                                : overview.get("overview", Immutable.fromJS({})).get("hosts_inactive", Immutable.fromJS([])).size
                            }
                        </div>
                    </div>
                    <div className="col-md-2 col-sm-4 col-xs-6 tile_stats_count">
                        <span className="count_top green">Active Clusters</span>
                        <div className="count green">
                            {overview.get("fetchingOverview", false)
                                ? <IoLoadD className="spin"/>
                                : overview.get("overview", Immutable.fromJS({})).get("clusters_active", Immutable.fromJS([]))
                            }
                        </div>
                    </div>
                    <div className="col-md-2 col-sm-4 col-xs-6 tile_stats_count">
                        <span className="count_top">Free Clusters</span>
                        <div className="count">
                            {overview.get("fetchingOverview", false)
                                ? <IoLoadD className="spin"/>
                                : overview.get("overview", Immutable.fromJS({})).get("clusters_free", Immutable.fromJS([]))
                            }
                        </div>
                    </div>
                    <div className="col-md-2 col-sm-4 col-xs-6 tile_stats_count">
                        <span className="count_top red">Inuse Clusters</span>
                        <div className="count red">
                            {overview.get("fetchingOverview", false)
                                ? <IoLoadD className="spin"/>
                                : overview.get("overview", Immutable.fromJS({})).get("clusters_inuse", Immutable.fromJS([]))
                            }
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
