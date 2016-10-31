/**
 * Created by yuehaitao on 2016/10/30.
 */
import React from 'react'

var TopNav = React.createClass({
    render: function () {
        return (
            <div className="top_nav">
                <div className="nav_menu">
                    <nav className="" role="navigation">
                        <div className="nav toggle">
                            <a id="menu_toggle" onClick={this.props.foldMenu}><i className="fa fa-bars"/></a>
                        </div>
                    </nav>
                </div>
            </div>
        )
    }
});

export default TopNav;
