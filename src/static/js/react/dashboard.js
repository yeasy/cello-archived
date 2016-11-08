/**
 * Created by yuehaitao on 2016/9/28.
 */
import React from 'react'
import { connect } from 'react-redux'
import * as AllActions from './actions'
import { bindActionCreators } from 'redux'
import Header from './header'
import LeftNav from './left_nav'
import TopNav from './top_nav'
import classNames from 'classnames'

var Dashboard = React.createClass({
    getInitialState: function () {
        return ({
            menuFolding: false,
            title: 'Cello Dashboard'
        })
    },
    foldMenu: function () {
        var menuFolding = this.state.menuFolding;
        this.setState({
            menuFolding: !menuFolding
        })
    },
    render: function() {
        var bodyClass = classNames({
            "nav-md": !this.state.menuFolding,
            "nav-sm": this.state.menuFolding
        });
        return (
            <div className={bodyClass}>
                <Header title={this.state.title} />
                <div className="container body">
                    <div className="main_container">
                        <LeftNav/>
                        <TopNav foldMenu={this.foldMenu} />
                        <div className="right_col" role="main">
                            {this.props.children}
                        </div>
                    </div>
                </div>
            </div>
        )
    }
});

export default Dashboard;
