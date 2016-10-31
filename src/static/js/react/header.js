/**
 * Created by yuehaitao on 2016/10/30.
 */
import React from 'react'
import Helmet from "react-helmet";

var Header = React.createClass({
    render: function () {
        return (
            <Helmet title={this.props.title} />
        )
    }
});

export default Header;
