/**
 * Created by yuehaitao on 2016/10/5.
 */
import React from 'react'
import { connect } from 'react-redux'
import * as AllActions from '../actions'
import { bindActionCreators } from 'redux'
var IoIosUndo = require('react-icons/lib/io/ios-undo');
var IoLoadD = require('react-icons/lib/io/load-d');
import {
    Button, Grid, Col, Row, Modal, Label, ListGroup, ListGroupItem
} from 'react-bootstrap'
var Link = require('react-router').Link;
import Immutable from 'immutable';

const styles = {
    icon: {
        marginRight: 5
    },
    rightAlign: {
        textAlign: "right"
    }
};

var ClusterInfo = React.createClass({
    getInitialState: function () {
        return ({
            showDeleteModal: false
        })
    },
    linkTo: function(url) {
        this.props.history.push(url);
    },
    componentDidMount: function () {
        const {dispatch, actions} = this.props;
        const {clusterId} = this.props.params;

        dispatch(actions.fetchCluster(clusterId));
    },
    componentWillUnmount: function () {
        const {dispatch, actions} = this.props;
        dispatch(actions.clearClusters("active"));
    },
    render: function () {
        const {clusters} = this.props;
        const {clusterId} = this.props.params;

        const currentCluster = clusters.get("activeClusters").get(clusterId, Immutable.fromJS({}));

        return (
            <div className="">
                <div className="page-title">
                    <div className="title_left">
                        <h3>
                            Cluster Detail &nbsp;&nbsp; {clusters.get("fetchingCluster", false) && <IoLoadD className="spin"/>}
                            <Link to="/chains/active">
                                <Button style={styles.icon}>
                                    <IoIosUndo size={16} />
                                </Button>
                            </Link> &nbsp;&nbsp;
                        </h3>
                    </div>
                </div>
                <div className="clearfix"></div>
                <div className="row">
                    <div className="col-md-12">
                        <div className="x_panel">
                            <div className="x_title">
                                {currentCluster.get("name", "")}
                            </div>
                            <div className="x_content">
                                <div className="col-md-9 col-sm-9 col-xs-12">
                                    <ul className="stats-overview">
                                        <li>
                                            <span className="name"> ID </span>
                                            <span className="value text-success"> {currentCluster.get("id", "")} </span>
                                        </li>
                                        <li>
                                            <span className="name"> Status </span>
                                            <span className="value text-success"> {currentCluster.get("status", "")} </span>
                                        </li>
                                        <li>
                                            <span className="name"> Health </span>
                                            <span className="value text-success"> {currentCluster.get("health", "")} </span>
                                        </li>
                                    </ul>
                                    <br />
                                    <div>
                                        {currentCluster.get("containers", Immutable.fromJS({})).keySeq().toJS().map((container, i) =>
                                            <ListGroupItem key={i} style={{width: "40%"}}>{container}</ListGroupItem>
                                        )}
                                    </div>
                                </div>
                                <div className="col-md-3 col-sm-3 col-xs-12">

                                    <section className="panel">

                                        <div className="x_title">
                                            <h2>Cluster Detail</h2>
                                            <div className="clearfix"></div>
                                            <div className="panel-body">
                                                <h3 className="green"><i className="fa fa-exclamation-circle" /> {currentCluster.get("name")}</h3>
                                                {!clusters.get("fetchingCluster", false) &&
                                                <div className="project_detail">

                                                    <p className="title">Consensus</p>
                                                    <p>{currentCluster.get("consensus_plugin", "")}{currentCluster.get("consensus_mode") &&
                                                    <span>/{currentCluster.get("consensus_mode")}</span>}</p>
                                                    <p className="title">Host</p>
                                                    <p>{currentCluster.get("host_id")}</p>
                                                    <p className="title">Create Time</p>
                                                    <p>{currentCluster.get("create_ts")}</p>
                                                    <p className="title">Apply Time</p>
                                                    <p>{currentCluster.get("apply_ts")}</p>
                                                    <p className="title">Release Time</p>
                                                    <p>{currentCluster.get("release_ts")}</p>
                                                    <p className="title">Server Url</p>
                                                    {currentCluster.get("service_url", Immutable.fromJS({})).entrySeq().toJS().map((service, i) =>
                                                        <p>{service}</p>
                                                    )}
                                                    <p className="title">User Id</p>
                                                    <p>{currentCluster.get("user_id")}</p>
                                                </div>
                                                }
                                            </div>
                                        </div>
                                    </section>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        )
    }
});

export default connect(state => ({
    clusters: state.clusters
}), dispatch => ({
    actions: bindActionCreators(AllActions, dispatch),
    dispatch: dispatch
}))(ClusterInfo)
