/**
 * Created by yuehaitao on 2016/10/5.
 */
import React from 'react'
import { connect } from 'react-redux'
import * as AllActions from './actions'
import { bindActionCreators } from 'redux'
var IoGearB = require('react-icons/lib/io/gear-b');
var IoAndroidRefresh = require('react-icons/lib/io/android-refresh');
var IoTrashA = require('react-icons/lib/io/trash-a');
var IoIosUndo = require('react-icons/lib/io/ios-undo');
import {
    Button, Grid, Col, Row, Modal, Label, ListGroup, ListGroupItem
} from 'react-bootstrap'
var Link = require('react-router').Link;

const styles = {
    icon: {
        marginRight: 5
    },
    rightAlign: {
        textAlign: "right"
    }
};

var InfoCol = React.createClass({
    render: function () {
        const {currentHost} = this.props;
        return (
            <div>
                <Row>
                    <Col sm={2} style={styles.rightAlign}><b>Name</b></Col>
                    <Col sm={10}>{currentHost.get("name", "")}</Col>
                </Row>
                <Row>
                    <Col sm={2} style={styles.rightAlign}><b>Id</b></Col>
                    <Col sm={10}>{currentHost.get("id", "")}</Col>
                </Row>
                <Row>
                    <Col sm={2} style={styles.rightAlign}><b>Status</b></Col>
                    <Col sm={10}>{currentHost.get("status", "")}</Col>
                </Row>
                <Row>
                    <Col sm={2} style={styles.rightAlign}><b>Schedulable</b></Col>
                    <Col sm={10}>{currentHost.get("schedulable", "")}</Col>
                </Row>
                <Row>
                    <Col sm={2} style={styles.rightAlign}><b>AutoFill</b></Col>
                    <Col sm={10}>{currentHost.get("autofill", "")}</Col>
                </Row>
                <Row>
                    <Col sm={2} style={styles.rightAlign}><b>Type</b></Col>
                    <Col sm={10}>{currentHost.get("type", "")}</Col>
                </Row>
                <Row>
                    <Col sm={2} style={styles.rightAlign}><b>Capacity</b></Col>
                    <Col sm={10}>{currentHost.get("capacity", "")}</Col>
                </Row>
                <Row>
                    <Col sm={2} style={styles.rightAlign}><b>Host URL</b></Col>
                    <Col sm={10}>{currentHost.get("daemon_url", "")}</Col>
                </Row>
                <Row>
                    <Col sm={2} style={styles.rightAlign}><b>Logging Level</b></Col>
                    <Col sm={10}>{currentHost.get("log_level", "")}</Col>
                </Row>
                <Row>
                    <Col sm={2} style={styles.rightAlign}><b>Log Collector</b></Col>
                    <Col sm={10}>{currentHost.get("log_type", "")}</Col>
                </Row>
                <Row>
                    <Col sm={2} style={styles.rightAlign}><b>Create Time</b></Col>
                    <Col sm={10}>{currentHost.get("create_ts", "")}</Col>
                </Row>
                <Row>
                    <Col sm={2} style={styles.rightAlign}><b>Clusters</b></Col>
                    <Col sm={10}>
                         <ListGroup>
                             {currentHost.get("clusters").map((cluster, i) =>
                                 <ListGroupItem style={{width: "40%"}}>{cluster}</ListGroupItem>
                             )}
                         </ListGroup>
                    </Col>
                </Row>
            </div>
        )
    }
});

var ConfirmDeleteModal = React.createClass({
    getInitialState: function () {
        return ({
            hostName: ""
        })
    },
    linkTo: function(url) {
        this.props.history.push(url);
    },
    deleteHost: function () {
        const {dispatch, actions} = this.props;
        const {hostId} = this.props.params;

        var hostForm = new FormData();
        hostForm.append('id', hostId);

        dispatch(actions.deleteHost(hostForm, hostId));
        this.props.close();
        this.linkTo("/");
    },
    close: function () {
        this.props.close();
    },
    enterModal: function () {
        const {hosts} = this.props;
        const {hostId} = this.props.params;
        var hostName = hosts.get("hosts").get(hostId).get("name");
        this.setState({
            hostName: hostName
        })
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

var HostInfo = React.createClass({
    getInitialState: function () {
        return ({
            showDeleteModal: false
        })
    },
    closeDeleteModal() {
        this.setState({ showDeleteModal: false });
    },
    openDeleteModal: function(hostId) {
        this.setState({
            showDeleteModal: true
        });
    },
    linkTo: function(url) {
        this.props.history.push(url);
    },
    deleteHost: function () {
        const {dispatch, actions} = this.props;
        const {hostId} = this.props.params;

        var hostForm = new FormData();
        hostForm.append('id', hostId);

        dispatch(actions.deleteHost(hostForm, hostId));
        this.linkTo("/");
    },
    render: function () {
        const {hosts} = this.props;
        const {hostId} = this.props.params;
        var currentHost = hosts.get("hosts").get(hostId);

        return (
            <div className="row">
                <h2 className="page-header">Host Information
                    <span style={{float: "right"}}>
                    <Link to="/">
                    <Button style={styles.icon}>
                        <IoIosUndo size={16} />
                    </Button>
                    </Link>
                    <Button bsStyle="info" style={styles.icon}>
                        <IoGearB size={16} />
                    </Button>
                    <Button bsStyle="danger" style={styles.icon}>
                        <IoAndroidRefresh size={16} />
                    </Button>
                    <Button bsStyle="danger">
                        <IoTrashA onClick={this.openDeleteModal} size={16} />
                    </Button>
                    </span>
                </h2>
                <InfoCol currentHost={currentHost} {...this.props} />
                <ConfirmDeleteModal showModal={this.state.showDeleteModal} close={this.closeDeleteModal} {...this.props} />
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
}))(HostInfo)
