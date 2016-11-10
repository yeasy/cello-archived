/**
 * Created by yuehaitao on 2016/11/10.
 */
import React from 'react'
import { connect } from 'react-redux'
import * as AllActions from '../actions'
import { bindActionCreators } from 'redux'
import {
    Modal, Button, Form, FormGroup, ControlLabel,
    Col, FormControl, Checkbox, Label
} from 'react-bootstrap'
var Select = require('react-select');
require("react-select/dist/react-select.css");
import fetch from 'isomorphic-fetch'
import cookie from 'react-cookie'
var Urls = require('../hosts/constants/Urls');
import Immutable from 'immutable';

var AddChainModal = React.createClass({
    getInitialState: function () {
        return ({
            Name: "",
            hostName: "",
            chainSize: "",
            plugin: "",
            mode: ""
        })
    },
    initialState: function () {
        this.setState({
            Name: "",
            hostName: "",
            chainSize: "",
            plugin: "",
            mode: ""
        });
    },
    close: function () {
        this.initialState();
        this.props.close();
    },
    addChain: function () {
        const {dispatch, actions} = this.props;
        var hostJson = {
            name: this.state.Name,
            host_id: this.state.hostName,
            consensus_plugin: this.state.plugin,
            size: this.state.chainSize,
            consensus_mode: this.state.mode
        };
        var chainForm = new FormData();
        for (var key in hostJson) {
            chainForm.append(key, hostJson[key]);
        }
        dispatch(actions.addChain(chainForm));
        this.close();
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
    hostNameChange: function (val) {
        if (val) {
            this.setState({
                hostName: val.value
            })
        }
    },
    hostNameClose: function () {
        this.setState({
            hostName: ""
        })
    },
    chainSizeChange: function (val) {
        if (val) {
            this.setState({
                chainSize: val.value
            })
        }
    },
    chainSizeClose: function () {
        this.setState({
            chainSize: ""
        })
    },
    pluginChange: function (val) {
        if (val) {
            this.setState({
                plugin: val.value
            })
        }
    },
    pluginClose: function () {
        this.setState({
            plugin: ""
        })
    },
    modeChange: function (val) {
        if (val) {
            this.setState({
                mode: val.value
            })
        }
    },
    modeClose: function () {
        this.setState({
            mode: ""
        })
    },
    getHostNameOptions: function () {
        return fetch(Urls.HostsUrl, {
            method: "get",
            credentials: 'include',
            headers: {
                "X-CSRFToken": cookie.load("csrftoken")
            }
        })
            .then((response) => {
                return response.json();
            }).then((json) => {
                var hosts = Immutable.fromJS(json.data);
                var hostsList = [];
                hosts.map((host, i) => {
                    var capacity = parseInt(host.get("capacity"));
                    var clusterLen = parseInt(host.get("clusters").size);
                    if (capacity > clusterLen) {
                        var hostName = host.get("name");
                        var hostId = host.get("id");
                        hostsList.push({value: hostId, label: hostName});
                    }
                });
                return { options: hostsList};
            });
    },
    render: function () {
        return (
            <Modal show={this.props.showModal} onHide={this.close}>
                <Modal.Header closeButton>
                    <Modal.Title>Add Chain</Modal.Title>
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
                        <FormGroup controlId="hostName">
                            <Col componentClass={ControlLabel} sm={2}>
                                Select a Host
                            </Col>
                            <Col sm={6}>
                                <Select.Async
                                    cache={false}
                                    name="form-field-name"
                                    loadOptions={this.getHostNameOptions}
                                    value={this.state.hostName}
                                    onChange={this.hostNameChange}
                                    onClose={this.hostNameClose}
                                />
                            </Col>
                        </FormGroup>
                        <FormGroup controlId="chainSize">
                            <Col componentClass={ControlLabel} sm={2}>
                                Chain Size
                            </Col>
                            <Col sm={6}>
                                <Select
                                    cache={false}
                                    name="form-field-name"
                                    value={this.state.chainSize}
                                    options={[
                                        {label: "4", value: "4"},
                                        {label: "6", value: "6"}
                                    ]}
                                    onChange={this.chainSizeChange}
                                    onClose={this.chainSizeClose}
                                />
                            </Col>
                        </FormGroup>
                        <FormGroup controlId="plugin">
                            <Col componentClass={ControlLabel} sm={2}>
                                Consensus Plugin
                            </Col>
                            <Col sm={6}>
                                <Select
                                    cache={false}
                                    name="form-field-name"
                                    value={this.state.plugin}
                                    options={[
                                        {label: "NOOPS", value: "noops"},
                                        {label: "PBFT", value: "pbft"},
                                    ]}
                                    onChange={this.pluginChange}
                                    onClose={this.pluginClose}
                                />
                            </Col>
                        </FormGroup>
                        {this.state.plugin == "pbft" &&
                        <FormGroup controlId="mode">
                            <Col componentClass={ControlLabel} sm={2}>
                                Consensus Mode
                            </Col>
                            <Col sm={6}>
                                <Select
                                    cache={false}
                                    name="form-field-name"
                                    value={this.state.mode}
                                    options={[
                                        {label: "BATCH", value: "batch"},
                                    ]}
                                    onChange={this.modeChange}
                                    onClose={this.modeClose}
                                />
                            </Col>
                        </FormGroup>
                        }
                    </Form>
                </Modal.Body>
                <Modal.Footer>
                    {(this.nameValidationState() == "error" || !this.state.hostName || !this.state.chainSize || !this.state.plugin) ?
                        <Button bsStyle="success" disabled>Create</Button>
                        :
                        <Button onClick={this.addChain} bsStyle="success">Create</Button>
                    }
                    <Button onClick={this.close}>Close</Button>
                </Modal.Footer>
            </Modal>
        )
    }
});

export default connect(state => ({
    hosts: state.hosts
}), dispatch => ({
    actions: bindActionCreators(AllActions, dispatch),
    dispatch: dispatch
}))(AddChainModal)
