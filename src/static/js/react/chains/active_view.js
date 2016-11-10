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

var ActiveChains = React.createClass({
    getInitialState: function () {
        return ({
            query: {},
            searchColumn: "all",
            pagination: {
                page: 1,
                perPage: 10
            }
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
    render: function () {
        const {clusters} = this.props;
        const columns = [
            {
                property: 'name',
                header: {
                    label: 'Name'
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
                        <span className="label label-success">{status}</span>
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
                            <Button bsStyle="success" >
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
                                <h2>Active Chains List</h2>
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

                                            <Table.Body rows={paginated.rows} rowKey="id" />
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
