/**
 * Created by yuehaitao on 2016/10/30.
 */
import React from 'react'
import { connect } from 'react-redux'
import * as AllActions from '../actions'
import { bindActionCreators } from 'redux'
var IoLoadD = require('react-icons/lib/io/load-d');
import {Button} from 'react-bootstrap'
import { Table, search, Search} from 'reactabular';
import { compose } from 'redux';
import {Paginator, paginate} from '../helpers'
var classNames = require("classnames");
require("../style/table.css");
import AddChainModal from './modal_add_chain'
var Link = require('react-router').Link;


var Actions = React.createClass({
    hostAction: function (hostAction, hostId) {
        const {dispatch, actions} = this.props;

        var hostForm = new FormData();
        hostForm.append('id', hostId);
        hostForm.append('action', hostAction);

        dispatch(actions.hostAction(hostForm, hostId, hostAction));
    },
    operateCluster: function (operation) {
        const {dispatch, actions, rowData} = this.props;
        if ((operation == "release" && rowData.user_id == "") || ("action" in rowData && rowData.action != "")) {
            return null;
        }
        dispatch(actions.operateCluster(rowData.id, rowData.name, operation))
    },
    deleteCluster: function () {
        const {dispatch, actions, rowData} = this.props;
        var clusterJson = {
            id: rowData.id,
            col_name: "active"
        };
        var clusterForm = new FormData();
        for (var key in clusterJson) {
            clusterForm.append(key, clusterJson[key]);
        }
        dispatch(actions.deleteCluster(clusterForm, rowData.name));
    },
    render: function () {
        const {rowData} = this.props;
        const releaseActionClass = classNames({
            disabled: rowData.user_id == "" || ("action" in rowData && rowData.action != "")
        });
        const startActionClass = classNames({
            disabled: ("action" in rowData && rowData.action != "") || rowData.status == "running"
        });
        const stopActionClass = classNames({
            disabled: ("action" in rowData && rowData.action != "") || rowData.status == "stopped"
        });
        const actionClass = classNames({
            disabled: "action" in rowData && rowData.action != ""
        });
        return (
            <div className="btn-group">
                <button className="btn btn-primary btn-xs">Action</button>
                <button className="btn btn-primary dropdown-toggle btn-xs" data-toggle="dropdown">
                    <span className="caret"></span>
                    <span className="sr-only">Toggle Dropdown</span>
                </button>
                <ul className="dropdown-menu" role="menu">
                    <li className={startActionClass}><a onClick={() => this.operateCluster("start")}><span className="glyphicon glyphicon-play" /> Start</a></li>
                    <li className={stopActionClass}><a onClick={() => this.operateCluster("stop")}><span className="glyphicon glyphicon-stop" /> Stop</a></li>
                    <li className={actionClass}><a onClick={() => this.operateCluster("restart")}><span className="glyphicon glyphicon-repeat" /> Restart</a></li>
                    <li className={actionClass}><a onClick={this.deleteCluster}><span className="glyphicon glyphicon-trash" /> Delete</a></li>
                    <li className={releaseActionClass}><a onClick={() => this.operateCluster("release")}><span className="glyphicon glyphicon-refresh" /> Release</a></li>
                </ul>
            </div>
        )
    }
});

var ActionStatus = React.createClass({
    render: function () {
        const {rowData} = this.props;
        var action = "";
        if ("action" in rowData) {
            action = rowData.action;
        }
        return (
            <span>{action != "" ? <span><IoLoadD className="spin"/> {action}</span> : ""}</span>
        )
    }
});

var ActiveChains = React.createClass({
    getInitialState: function () {
        return ({
            query: {},
            searchColumn: "all",
            pagination: {
                page: 1,
                perPage: 10
            },
            showAddModal: false
        })
    },
    componentDidMount: function () {
        const {dispatch, actions} = this.props;

        dispatch(actions.fetchClusters("active"));
    },
    componentWillUnmount: function () {
        const {dispatch, actions} = this.props;
        dispatch(actions.clearClusters("active"));
    },
    searchColumnChange: function (searchColumn) {
        this.setState({
            searchColumn: searchColumn
        })
    },
    searchChange: function (query) {
        this.setState({
            query: query
        })
    },
    closeModal: function () {
        this.setState({
            showAddModal: false
        })
    },
    addChain: function () {
        this.setState({
            showAddModal: true
        })
    },
    onSelect: function(data) {
        const {clusters} = this.props;
        var pagination = this.state.pagination;
        var page = data.selected + 1;
        var clustersLength = clusters.get("activeClusters").valueSeq().toJS().length;
        var perPage = this.state.pagination.perPage;
        const pages = Math.ceil(
            clustersLength / perPage
        );

        this.setState({
            pagination: {
                page: Math.min(Math.max(page, 1), pages),
                perPage: pagination.perPage
            }
        });
    },
    perPageChange: function (e) {
        var pagination = this.state.pagination;
        this.setState({
            pagination: {
                page: pagination.page,
                perPage: parseInt(e.target.value)
            }
        })
    },
    onRow: function (row, { rowIndex, rowKey }) {
        return {
            className: row.user_id ? "used_row" : ""
        }
    },
    render: function () {
        const {clusters} = this.props;
        const columns = [
            {
                property: 'name',
                header: {
                    label: 'Name'
                },
                cell: {
                    format: (name, {rowData}) => (
                        <Link to={`/chains/cluster/${rowData.id}`}>{name}</Link>
                    )
                }
            },
            {
                property: 'consensus_plugin',
                header: {
                    label: 'Type'
                },
                cell: {
                    format: (plugin, {rowData}) => (
                        <span>{plugin}{rowData.consensus_mode ? <span>/{rowData.consensus_mode}</span>: <span></span>}</span>
                    )
                }
            },
            {
                property: 'status',
                header: {
                    label: 'Status'
                },
                cell: {
                    format: (status, extra) => (
                        <span className={classNames("label", {
                            "label-success": status == "running",
                            "label-danger": status == "stopped"
                        })}>{status}</span>
                    )
                }
            },
            {
                property: 'health',
                header: {
                    label: 'Health'
                },
                cell: {
                    format: (health, extra) => (
                        <span className={classNames("label", {
                            "label-success": health == "OK",
                            "label-danger": health != "OK"
                        })}>{health}</span>
                    )
                }
            },
            {
                property: 'size',
                header: {
                    label: 'Size'
                }
            },
            {
                property: 'host_id',
                header: {
                    label: 'Host'
                }
            },
            {
                cell: {
                    format: (value, { rowData }) => (
                        <Actions {...this.props} rowData={rowData} />
                    )
                },
                visible: true
            },
            {
                cell: {
                    format: (value, { rowData }) => (
                        <ActionStatus {...this.props} rowData={rowData} />
                    )
                }
            }
        ];
        const {query, pagination} = this.state;
        const paginated = compose(
            paginate(pagination),
            search.multipleColumns({ columns, query})
        )(clusters.get("activeClusters").valueSeq().toJS());
        const pageSizeArray = [10, 20, 30, 40, 50];
        return (
            <div className="">
                <div className="page-title">
                    <div className="title_left">
                        <h3>Active Chains <small>{clusters.get("fetchingClusters", false) ? <IoLoadD className="spin" size={30} /> : clusters.get("activeClusters").valueSeq().toJS().length}</small></h3>
                    </div>
                    <div className="title_right">
                        <div className="col-md-2 col-sm-2 col-xs-12 pull-right">
                            <Button onClick={this.addChain} bsStyle="success" >
                                Add Chain
                            </Button>
                        </div>
                    </div>
                </div>
                <div className="clearfix"></div>
                <div className="row">
                    <div className="col-md-12">
                        <div className="x_panel">
                            <div className="x_title">
                                <h2>Active Chains List {clusters.get("addingCluster", false) && <IoLoadD className="spin"/>}</h2>
                                <div className="clearfix"></div>
                            </div>
                            <div className="x_content">
                                <div className="row">
                                    <div className="col-sm-6">
                                        <div className="dataTables_length">
                                            <label>
                                                <select onChange={this.perPageChange} className="form-control input-sm">
                                                    {pageSizeArray.map((pageSize, i) =>
                                                        <option key={i} value={pageSize}>{pageSize}</option>
                                                    )}
                                                </select>
                                            </label>
                                        </div>
                                    </div>
                                    <div className="col-sm-6">
                                        <div className="dataTables_filter">
                                            <label>
                                                <Search
                                                    className="input-group"
                                                    column={this.state.searchColumn}
                                                    query={this.state.query}
                                                    columns={columns}
                                                    onColumnChange={this.searchColumnChange}
                                                    onChange={this.searchChange}
                                                    rows={clusters.get("activeClusters").valueSeq().toJS()}
                                                />
                                            </label>
                                        </div>
                                    </div>
                                </div>
                                <div className="row">
                                    <div className="col-sm-12">
                                        <Table.Provider
                                            className="table table-striped projects"
                                            columns={columns}
                                        >
                                            <Table.Header />

                                            <Table.Body rows={paginated.rows} onRow={this.onRow}
                                                        rowKey="id" />
                                        </Table.Provider>
                                    </div>
                                </div>
                                <div className="row">
                                    <div className="col-sm-5"></div>
                                    <div className="col-sm-7">
                                        <div className="dataTables_paginate paging_simple_numbers">
                                            <Paginator
                                                pagination={pagination}
                                                pages={paginated.amount}
                                                onSelect={this.onSelect}
                                            />
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <AddChainModal showModal={this.state.showAddModal} close={this.closeModal} />
            </div>
        )
    }
});

export default connect(state => ({
    clusters: state.clusters
}), dispatch => ({
    actions: bindActionCreators(AllActions, dispatch),
    dispatch: dispatch
}))(ActiveChains)
