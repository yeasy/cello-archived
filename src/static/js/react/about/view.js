/**
 * Created by yuehaitao on 2016/10/30.
 */
import React from 'react'

var About = React.createClass({
    render: function () {
        return (
            <div className="">
                <div className="row">
                    <div className="col-md-12">
                        <div className="x_panel">
                            <div className="x_title">
                                <h2>About</h2>
                                <ul className="nav navbar-right panel_toolbox">
                                    <li><a className="collapse-link"><i className="fa fa-chevron-up" /></a>
                                    </li>
                                </ul>
                                <div className="clearfix"></div>
                            </div>
                            <div className="x_content">
                                <div className="col-md-12">
                                    <p>Platform to manage blockchains, and targets automating deployment, operations, and scaling.</p>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div className="col-md-12">
                        <div className="x_panel">
                            <div className="x_title">
                                <h2>Release Information</h2>
                                <ul className="nav navbar-right panel_toolbox">
                                    <li><a className="collapse-link"><i className="fa fa-chevron-up" /></a>
                                    </li>
                                </ul>
                                <div className="clearfix"></div>
                            </div>
                            <div className="x_content">
                                <div className="col-md-12">
                                    <p>
                                        Written-By: Baohua Yang (baohyang@cn.ibm.com)
                                    </p>
                                    <p>Version: 1.0.0-rc2</p>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div className="col-md-12">
                        <div className="x_panel">
                            <div className="x_title">
                                <h2>Terms</h2>
                                <ul className="nav navbar-right panel_toolbox">
                                    <li><a className="collapse-link"><i className="fa fa-chevron-up" /></a>
                                    </li>
                                </ul>
                                <div className="clearfix"></div>
                            </div>
                            <div className="x_content">
                                <div className="col-md-12">
                                    <p>
                                        Host: An aggregation of some physical/virtual machines to hold the clusters.
                                    </p>
                                    <p>
                                        Cluster: A blockchain with numbers of peer nodes.
                                    </p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        )
    }
});

export default About;
