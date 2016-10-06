/**
 * Created by yuehaitao on 2016/9/28.
 */
import React from 'react'
import {
    Table, Modal, Button, Form, FormGroup, ControlLabel,
    Col, FormControl, Checkbox, Label, OverlayTrigger, Tooltip
} from 'react-bootstrap'
import isIP from 'validator/lib/isIP';
import { connect } from 'react-redux'
import * as AllActions from './actions'
import { bindActionCreators } from 'redux'
import "react-bootstrap-table/dist/react-bootstrap-table-all.min.css"
import { BootstrapTable, TableHeaderColumn } from 'react-bootstrap-table';
var IoGearB = require('react-icons/lib/io/gear-b');
var IoLoadD = require('react-icons/lib/io/load-d');
var IoTrashA = require('react-icons/lib/io/trash-a');
var MdTrendingUp = require('react-icons/lib/md/trending-up');
var MdTrendingDown = require('react-icons/lib/md/trending-down');
import "./spin.css"
var Link = require('react-router').Link;
import immutableRenderMixin from 'react-immutable-render-mixin';
import Immutable from 'immutable'

const styles = {
    actionBtn: {
        marginRight: 5
    }
};

var CreateHostModal = React.createClass({
    getInitialState: function () {
        return ({
            Name: '',
            daemonUrl: '',
            capacity: 1,
            loggerLevel: 'DEBUG',
            loggerType: 'local',
            loggerServer: '',
            showLoggerServer: false,
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
    loggerServerChange: function (e) {
        this.setState({
            loggerServer: e.target.value
        })
    },
    loggerServerValidationState: function () {
        const urlArray = this.state.loggerServer.split(":");
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
        var loggerType = e.target.value;
        if (loggerType == "syslog") {
            this.setState({
                showLoggerServer: true
            })
        } else {
            this.setState({
                showLoggerServer: false,
                loggerServer: ''
            })
        }
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
            capacity: this.state.capacity,
            log_type: this.state.loggerType,
            log_level: this.state.loggerLevel,
            log_server: this.state.loggerServer,
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
            loggerServer: '',
            showLoggerServer: false,
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
                                    <option value="local">LOCAL</option>
                                    <option value="syslog">SYSLOG</option>
                                </FormControl>
                            </Col>
                        </FormGroup>
                        {this.state.showLoggerServer &&
                        <FormGroup controlId="LoggerServer" validationState={this.loggerServerValidationState()}>
                            <Col componentClass={ControlLabel} sm={2}>
                                Log Server
                            </Col>
                            <Col sm={6}>
                                <FormControl type="text" onChange={this.loggerServerChange} value={this.state.loggerServer} placeholder="192.168.0.1:5000" />
                            </Col>
                        </FormGroup>
                        }
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
                    {(this.nameValidationState() == "error" || this.urlValidationState() == "error" || (this.state.loggerType == "syslog" && this.loggerServerValidationState() == "error")) ?
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

var EditHostModal = React.createClass({
    getInitialState: function () {
        return ({
            currentHost: Immutable.Map({}),
            capacity: 1,
            loggerLevel: 'INFO',
            loggerServer: '',
            showLoggerServer: false,
            loggerType: '',
            schedulable: false,
            autoFill: false,
            Name: ''
        })
    },
    close: function () {
        this.props.close();
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
    loggerServerChange: function (e) {
        this.setState({
            loggerServer: e.target.value
        })
    },
    loggerServerValidationState: function () {
        const urlArray = this.state.loggerServer.split(":");
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
    scheduleChange: function (e) {
        var schedulable = this.state.schedulable;
        this.setState({
            schedulable: !schedulable
        })
    },
    autoFillChange: function (e) {
        var autoFill = this.state.autoFill;
        this.setState({
            autoFill: !autoFill
        })
    },
    loggerTypeChange: function (e) {
        var loggerType = e.target.value;
        if (loggerType == "syslog") {
            this.setState({
                showLoggerServer: true
            })
        } else {
            this.setState({
                showLoggerServer: false,
                loggerServer: ''
            })
        }
        this.setState({
            loggerType: e.target.value
        })
    },
    enterModal: function () {
        const {hosts, currentHostId} = this.props;
        if (currentHostId.length > 0) {
            var currentHost = hosts.get("hosts").get(currentHostId);
            var loggerType = currentHost.get("log_type", "");
            var autoFill = currentHost.get("autofill");
            var schedulable = currentHost.get("schedulable");
            if (loggerType == "syslog") {
                this.setState({
                    showLoggerServer: true,
                    loggerServer: currentHost.get("log_server", "").split("//")[1]
                })
            } else {
                this.setState({
                    showLoggerServer: false,
                    loggerServer: ''
                })
            }
            this.setState({
                currentHost: currentHost,
                Name: currentHost.get("name", ""),
                loggerLevel: currentHost.get("log_level", ""),
                loggerType: currentHost.get("log_type", ""),
                autoFill: (autoFill == "true" || autoFill == "on"),
                schedulable: (schedulable == "true" || schedulable == "on"),
                capacity: parseInt(currentHost.get("capacity", 1))
            })
        }
    },
    updateHost: function () {
        const {dispatch, actions, currentHostId} = this.props;
        var hostJson = {
            id: currentHostId,
            name: this.state.Name,
            capacity: this.state.capacity,
            log_type: this.state.loggerType,
            log_server: this.state.loggerServer,
            schedulable: this.state.schedulable ? "on" : "off",
            autofill: this.state.autoFill ? "on" : "off",
            log_level: this.state.loggerLevel
        };
        this.props.close();
        var hostForm = new FormData();
        for (var key in hostJson) {
            hostForm.append(key, hostJson[key]);
        }
        dispatch(actions.updateHost(hostForm));
    },
    render: function () {
        return (
            <Modal onEnter={this.enterModal} show={this.props.showModal} onHide={this.close}>
                <Modal.Header closeButton>
                    <Modal.Title>Edit the host config</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <Form horizontal>
                        <FormGroup controlId="Id">
                            <Col componentClass={ControlLabel} sm={2}>
                                ID
                            </Col>
                            <Col sm={6}>
                                <FormControl type="text" value={this.state.currentHost.get("id", "")} disabled />
                            </Col>
                        </FormGroup>
                        <FormGroup validationState={this.nameValidationState()} controlId="Name">
                            <Col componentClass={ControlLabel} sm={2}>
                                Name
                            </Col>
                            <Col sm={6}>
                                <FormControl type="text" onChange={this.nameChange} value={this.state.Name} />
                            </Col>
                        </FormGroup>
                        <FormGroup controlId="DaemonUrl">
                            <Col componentClass={ControlLabel} sm={2}>
                                Daemon URL
                            </Col>
                            <Col sm={6}>
                                <FormControl type="text" value={this.state.currentHost.get("daemon_url", "")} disabled />
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
                        <FormGroup controlId="Status">
                            <Col componentClass={ControlLabel} sm={2}>
                                Status
                            </Col>
                            <Col sm={2}>
                                <FormControl type="text" value={this.state.currentHost.get("status", "")} disabled />
                            </Col>
                            <Col sm={4}>
                                <Checkbox onChange={this.scheduleChange} checked={this.state.schedulable} inline>Schedulable</Checkbox>
                            </Col>
                            <Col sm={4}>
                                <Checkbox onChange={this.autoFillChange} checked={this.state.autoFill} inline>Autofill</Checkbox>
                            </Col>
                        </FormGroup>
                        <FormGroup controlId="Type">
                            <Col componentClass={ControlLabel} sm={2}>
                                Type
                            </Col>
                            <Col sm={6}>
                                <FormControl type="text" value={this.state.currentHost.get("type", "")} disabled />
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
                                    <option value="local">LOCAL</option>
                                    <option value="syslog">SYSLOG</option>
                                </FormControl>
                            </Col>
                        </FormGroup>
                        {this.state.showLoggerServer &&
                        <FormGroup controlId="LoggerServer" validationState={this.loggerServerValidationState()}>
                            <Col componentClass={ControlLabel} sm={2}>
                                Log Server
                            </Col>
                            <Col sm={6}>
                                <FormControl type="text" onChange={this.loggerServerChange} value={this.state.loggerServer} placeholder="192.168.0.1:5000" />
                            </Col>
                        </FormGroup>
                        }
                        <FormGroup controlId="Created">
                            <Col componentClass={ControlLabel} sm={2}>
                                Created
                            </Col>
                            <Col sm={6}>
                                <FormControl type="text" value={this.state.currentHost.get("create_ts", "")} disabled />
                            </Col>
                        </FormGroup>
                        <FormGroup controlId="Chains">
                            <Col componentClass={ControlLabel} sm={2}>
                                Running Chains
                            </Col>
                            <Col sm={6}>
                                <FormControl type="text" value={this.state.currentHost.get("clusters", Immutable.List([])).size} disabled />
                            </Col>
                        </FormGroup>
                    </Form>
                </Modal.Body>
                <Modal.Footer>
                    <Button bsStyle="primary" onClick={this.updateHost}>Save</Button>
                    <Button onClick={this.close}>Close</Button>
                </Modal.Footer>
            </Modal>
        )
    }
});

var ConfirmDeleteModal = React.createClass({
    getInitialState: function () {
        return ({
            hostName: ""
        })
    },
    deleteHost: function () {
        const {dispatch, actions, currentHostId} = this.props;

        var hostForm = new FormData();
        hostForm.append('id', currentHostId);

        dispatch(actions.deleteHost(hostForm, currentHostId));
        this.props.close();
    },
    close: function () {
        this.props.close();
    },
    enterModal: function () {
        const {currentHostId, hosts} = this.props;
        if (currentHostId.length > 0) {
            var hostName = hosts.get("hosts").get(currentHostId).get("name");
            this.setState({
                hostName: hostName
            })
        }
    },
    render: function () {
        return (
            <Modal onEnter={this.enterModal} show={this.props.showModal} onHide={this.props.close}>
                <Modal.Header closeButton>
                    <Modal.Title>
                        <span className="text-danger">(Danger) Confirm Delete</span>
                    </Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <p>Do you Confirm delete host {this.state.hostName}?</p>
                </Modal.Body>
                <Modal.Footer>
                    <Button bsStyle="danger" onClick={this.deleteHost}>Confirm</Button>
                    <Button onClick={this.close}>Close</Button>
                </Modal.Footer>
            </Modal>
        )
    }
});

var ActionFormatter = React.createClass({
    deleteHost: function () {
        var hostId = this.props.cell;
        this.props.openDeleteModal(hostId);
    },
    configClick: function () {
        var hostId = this.props.cell;
        this.props.openEditModal(hostId);
    },
    tooltip: function (message) {
        return (
            <Tooltip id="tooltip"><strong>{message}</strong></Tooltip>
        )
    },
    hostAction: function (hostAction) {
        const {dispatch, actions} = this.props;
        var hostId = this.props.cell;

        var hostForm = new FormData();
        hostForm.append('id', hostId);
        hostForm.append('action', hostAction);

        dispatch(actions.hostAction(hostForm, hostId, hostAction));
    },
    render: function () {
        const {hosts} = this.props;
        var hostId = this.props.cell;
        var currentHost = hosts.get("hosts").get(hostId);
        var chains = currentHost.get("clusters", Immutable.List([])).size;
        var capacity = parseInt(currentHost.get("capacity"));
        return (
            <span>
                <OverlayTrigger placement="top" overlay={this.tooltip("fill up host")}>
                    <Button style={styles.actionBtn} bsSize="xsmall" disabled={chains == capacity} bsStyle="primary" onClick={() => this.hostAction("fillup")}>{hosts.get("hosts").get(hostId).get("fillup", false) ? <IoLoadD className="spin"/> : <MdTrendingUp />}</Button>
                </OverlayTrigger>
                <OverlayTrigger placement="top" overlay={this.tooltip("clean host")}>
                    <Button style={styles.actionBtn} bsSize="xsmall" disabled={chains == 0} bsStyle="warning" onClick={() => this.hostAction("clean")}>{hosts.get("hosts").get(hostId).get("clean", false) ? <IoLoadD className="spin"/> : <MdTrendingDown />}</Button>
                </OverlayTrigger>
                <Button style={styles.actionBtn} bsSize="xsmall" bsStyle="info" onClick={this.configClick}><IoGearB /></Button>
                <Button style={styles.actionBtn} bsSize="xsmall" bsStyle="danger" onClick={this.deleteHost}><IoTrashA /></Button>
            </span>
        )
    }
});

var NameFormatter = React.createClass({
    render: function () {
        return (
            <Link to={`/host/${this.props.hostId}`}>{this.props.name}</Link>
        )
    }
});

var HostTable = React.createClass({
    mixins: [immutableRenderMixin],

    getInitialState() {
        return {
            showModal: false,
            showEditModal: false,
            showDeleteModal: false,
            currentHostId: ''
        };
    },
    close() {
        this.setState({ showModal: false });
    },
    open() {
        this.setState({ showModal: true });
    },
    closeEditModal() {
        this.setState({ showEditModal: false });
    },
    openEditModal: function(hostId) {
        this.setState({
            showEditModal: true,
            currentHostId: hostId
        });
    },
    closeDeleteModal() {
        this.setState({ showDeleteModal: false });
    },
    openDeleteModal: function(hostId) {
        this.setState({
            showDeleteModal: true,
            currentHostId: hostId
        });
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
            <ActionFormatter {...this.props} cell={cell} openEditModal={this.openEditModal} openDeleteModal={this.openDeleteModal} />
        )
    },
    clustersFormatter: function (cell, row) {
        return cell.length;
    },
    nameFormatter: function (cell, row) {
        return (
            <NameFormatter {...this.props} hostId={row.id} name={cell}/>
        )
    },
    loggerFormatter: function (cell, row) {
        return cell + "/" + row.log_type.toLowerCase();
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
                <h2 className="page-header">Hosts: {hosts.get("fetchingHosts", false) ? <IoLoadD className="spin" size={30} /> : hosts.get("hosts").valueSeq().toJS().length}
                    <Button bsStyle="success" onClick={this.open} style={{float: "right"}}>
                        Add Host
                    </Button>
                </h2>
                <BootstrapTable pagination data={hosts.get("hosts").valueSeq().toJS()} striped={true} hover={true}>
                    <TableHeaderColumn dataField="name" dataAlign="center" dataFormat={this.nameFormatter} dataSort={true} filter={ { type: 'TextFilter', placeholder: 'Please enter a value' } }>Name</TableHeaderColumn>
                    <TableHeaderColumn dataField="type" dataSort={true} caretRender={this.getCaret}>Type</TableHeaderColumn>
                    <TableHeaderColumn dataField="status" dataSort={true} dataFormat={this.statusFormatter} formatExtraData={ statusFilter } filter={ { type: 'SelectFilter', options: statusFilter} }>Status</TableHeaderColumn>
                    <TableHeaderColumn dataField="clusters" dataFormat={this.clustersFormatter} dataSort={true}>Chains</TableHeaderColumn>
                    <TableHeaderColumn dataField="capacity" dataSort={true}>Cap</TableHeaderColumn>
                    <TableHeaderColumn dataField="log_level" dataSort={true} dataFormat={this.loggerFormatter}>Log Config</TableHeaderColumn>
                    <TableHeaderColumn dataField="id" isKey={true} dataFormat={this.actionFormatter}></TableHeaderColumn>
                </BootstrapTable>
                <CreateHostModal showModal={this.state.showModal} close={this.close} {...this.props} />
                <EditHostModal currentHostId={this.state.currentHostId} showModal={this.state.showEditModal} close={this.closeEditModal} {...this.props} />
                <ConfirmDeleteModal currentHostId={this.state.currentHostId} showModal={this.state.showDeleteModal} close={this.closeDeleteModal} {...this.props} />
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
