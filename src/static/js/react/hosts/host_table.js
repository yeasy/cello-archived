/**
 * Created by yuehaitao on 2016/9/28.
 */
import React from 'react'
import {
    Table, Modal, Button, Form, FormGroup, ControlLabel, Col, FormControl, Checkbox, Label
} from 'react-bootstrap'
import isIP from 'validator/lib/isIP';
import { connect } from 'react-redux'
import * as AllActions from './actions'
import { bindActionCreators } from 'redux'
import "react-bootstrap-table/dist/react-bootstrap-table-all.min.css"
import { BootstrapTable, TableHeaderColumn } from 'react-bootstrap-table';
var IoGearB = require('react-icons/lib/io/gear-b');
var IoLoadC = require('react-icons/lib/io/load-c');
var MdTrendingUp = require('react-icons/lib/md/trending-up');
var MdTrendingDown = require('react-icons/lib/md/trending-down');
import "./spin.css"

var CreateHostModal = React.createClass({
    getInitialState: function () {
        return ({
            Name: '',
            daemonUrl: '',
            capacity: 1,
            loggerLevel: 'DEBUG',
            loggerType: 'LOCAL',
            disableCreate: true,
            schedulable: false,
            keepFilled: false
        })
    },
    nameValidationState: function () {
        const nameLength = this.state.Name.length;
        if (nameLength >= 1 && nameLength <= 16) {
            return 'success';
        } else {
            return 'error';
        }
    },
    nameChange: function (event) {
        this.setState({
            Name: event.target.value
        })
    },
    urlValidationState: function () {
        const urlArray = this.state.daemonUrl.split(":");
        if (urlArray.length < 2) {
            return 'error';
        } else {
            const port = parseInt(urlArray[1]);
            if (!isIP(urlArray[0]) || !(port >= 1 && port <= 65535)) {
                return 'error';
            } else {
                return 'success';
            }
        }
    },
    urlChange: function (event) {
        this.setState({
            daemonUrl: event.target.value
        })
    },
    capacityChange: function (event) {
        this.setState({
            capacity: parseInt(event.target.value)
        })
    },
    loggerLevelChange: function (e) {
        this.setState({
            loggerLevel: e.target.value
        })
    },
    loggerTypeChange: function (e) {
        this.setState({
            loggerType: e.target.value
        })
    },
    scheduleChange: function (e) {
        var schedulable = this.state.schedulable;
        this.setState({
            schedulable: !schedulable
        })
    },
    keepFilledChange: function (e) {
        var keepFilled = this.state.keepFilled;
        this.setState({
            keepFilled: !keepFilled
        })
    },
    createHost: function () {
        const {dispatch, actions} = this.props;
        var hostJson = {
            name: this.state.Name,
            daemon_url: this.state.daemonUrl,
            log_server: "",
            capacity: this.state.capacity,
            log_type: this.state.loggerType,
            log_level: this.state.loggerLevel,
            autofill: this.state.keepFilled ? "on" : "off",
            schedulable: this.state.schedulable ? "on": "off"
        };
        this.clearValues();
        this.props.close();
        var hostForm = new FormData();
        for (var key in hostJson) {
            hostForm.append(key, hostJson[key]);
        }
        dispatch(actions.createHost(hostForm));
    },
    clearValues: function () {
        this.setState({
            Name: '',
            daemonUrl: '',
            capacity: 1,
            loggerLevel: 'DEBUG',
            loggerType: 'LOCAL',
            disableCreate: true,
            schedulable: false,
            keepFilled: false
        });
    },
    close: function () {
        this.clearValues();
        this.props.close();
    },
    render: function () {
        return (
            <Modal show={this.props.showModal} onHide={this.close}>
                <Modal.Header closeButton>
                    <Modal.Title>Add a host</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <Form horizontal>
                        <FormGroup validationState={this.nameValidationState()} controlId="Name">
                            <Col componentClass={ControlLabel} sm={2}>
                                *Name
                            </Col>
                            <Col sm={6}>
                                <FormControl type="text" onChange={this.nameChange} value={this.state.Name} placeholder="Host_Name(1 ~ 16 char)" />
                            </Col>
                        </FormGroup>
                        <FormGroup validationState={this.urlValidationState()} controlId="Url">
                            <Col componentClass={ControlLabel} sm={2}>
                                *Daemon URL
                            </Col>
                            <Col sm={6}>
                                <FormControl type="text" onChange={this.urlChange} value={this.state.daemonUrl} placeholder="192.168.0.1:2375" />
                            </Col>
                        </FormGroup>
                        <FormGroup controlId="Capacity">
                            <Col componentClass={ControlLabel} sm={2}>
                                Capacity
                            </Col>
                            <Col sm={6}>
                                <FormControl type="number" onChange={this.capacityChange} value={this.state.capacity} />
                            </Col>
                        </FormGroup>
                        <FormGroup controlId="LoggerLevel">
                            <Col componentClass={ControlLabel} sm={2}>
                                Logger Level
                            </Col>
                            <Col sm={6}>
                                <FormControl componentClass="select" onChange={this.loggerLevelChange} value={this.state.loggerLevel} placeholder="DEBUG" >
                                    <option value="DEBUG">DEBUG</option>
                                    <option value="INFO">INFO</option>
                                    <option value="NOTICE">NOTICE</option>
                                    <option value="WARNING">WARNING</option>
                                    <option value="ERROR">ERROR</option>
                                    <option value="CRITICAL">CRITICAL</option>
                                </FormControl>
                            </Col>
                        </FormGroup>
                        <FormGroup controlId="LoggerType">
                            <Col componentClass={ControlLabel} sm={2}>
                                Logger Type
                            </Col>
                            <Col sm={6}>
                                <FormControl componentClass="select" onChange={this.loggerTypeChange} value={this.state.loggerType} placeholder="LOCAL" >
                                    <option value="LOCAL">LOCAL</option>
                                    <option value="SYSLOG">SYSLOG</option>
                                </FormControl>
                            </Col>
                        </FormGroup>
                        <FormGroup>
                            <Col sm={6}>
                                <Checkbox onChange={this.scheduleChange} value={this.state.schedulable} inline>Schedulable for cluster request</Checkbox>
                            </Col>
                            <Col sm={6}>
                                    <Checkbox onChange={this.keepFilledChange} value={this.state.keepFilled} inline>Keep filled with cluster</Checkbox>
                            </Col>
                        </FormGroup>
                    </Form>
                </Modal.Body>
                <Modal.Footer>
                    {(this.nameValidationState() == "error" || this.urlValidationState() == "error") ?
                        <Button bsStyle="success" disabled>Create</Button>
                        :
                        <Button onClick={this.createHost} bsStyle="success">Create</Button>
                    }
                    <Button onClick={this.close}>Close</Button>
                </Modal.Footer>
            </Modal>
        )
    }
});

var ActionFormatter = React.createClass({
    configClick: function (e) {
        console.log('config click ' + this.props.cell);
    },
    render: function () {
        return (
            <span>
                <Button style={{marginRight: 5}} bsSize="xsmall" bsStyle="primary" onClick={this.configClick}><MdTrendingUp /></Button>
                <Button style={{marginRight: 5}} bsSize="xsmall" bsStyle="warning" onClick={this.configClick}><MdTrendingDown /></Button>
                <Button bsSize="xsmall" bsStyle="info" onClick={this.configClick}><IoGearB /></Button>
            </span>
        )
    }
});

var HostTable = React.createClass({
    getInitialState() {
        return { showModal: false };
    },
    close() {
        this.setState({ showModal: false });
    },

    open() {
        this.setState({ showModal: true });
    },
    componentDidMount: function () {
        const {dispatch, actions} = this.props;

        dispatch(actions.fetchHosts());
    },
    configClick: function (e) {
        console.log('config click');
    },
    statusFormatter: function(cell, row){
        var label = "success";
        if (cell == "error") {
            label = "danger";
        }
        return '<span class="label label-' + label + '">' + cell + '</span>';
    },
    actionFormatter: function (cell, row) {
        return (
            <ActionFormatter cell={cell} />
        )
    },
    clustersFormatter: function (cell, row) {
        return cell.length;
    },
    getCaret: function(direction) {
        if (direction === 'asc') {
            return (
                <span> up</span>
            );
        }
        if (direction === 'desc') {
            return (
                <span> down</span>
            );
        }
        return (
            <span> up/down</span>
        );
    },
    render: function() {
        const {hosts} = this.props;
        const statusFilter = {
            'active': 'active',
            'error': 'error'
        };
        return (
            <div className="row">
                <h2 className="page-header">Hosts:
                    <Button bsStyle="success" onClick={this.open} style={{float: "right"}}>
                        Add Host
                    </Button>
                </h2>
                <BootstrapTable pagination data={hosts.get("hosts").valueSeq().toJS()} striped={true} hover={true}>
                    <TableHeaderColumn dataField="name" isKey={true} dataAlign="center" dataSort={true} filter={ { type: 'TextFilter', placeholder: 'Please enter a value' } }>Name</TableHeaderColumn>
                    <TableHeaderColumn dataField="type" dataSort={true} caretRender={this.getCaret}>Type</TableHeaderColumn>
                    <TableHeaderColumn dataField="status" dataSort={true} dataFormat={this.statusFormatter} formatExtraData={ statusFilter } filter={ { type: 'SelectFilter', options: statusFilter} }>Status</TableHeaderColumn>
                    <TableHeaderColumn dataField="clusters" dataFormat={this.clustersFormatter} dataSort={true}>Chains</TableHeaderColumn>
                    <TableHeaderColumn dataField="capacity" dataSort={true}>Cap</TableHeaderColumn>
                    <TableHeaderColumn dataField="log_level" dataSort={true}>Log Config</TableHeaderColumn>
                    <TableHeaderColumn dataField="id" dataFormat={this.actionFormatter}></TableHeaderColumn>
                </BootstrapTable>
                <CreateHostModal showModal={this.state.showModal} close={this.close} {...this.props} />
            </div>
        )
    }
});

export default connect(state => ({
    hosts: state.hosts,
    message: state.message
}), dispatch => ({
    actions: bindActionCreators(AllActions, dispatch),
    dispatch: dispatch
}))(HostTable)
