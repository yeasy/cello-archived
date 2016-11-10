/**
 * Created by yuehaitao on 2016/10/30.
 */
import React from 'react'
import {Link} from 'react-router'
var activeComponent = require('react-router-active-component');
var NavLink = activeComponent('li');
var classNames = require('classnames');

var LeftNav = React.createClass({
    getInitialState: function () {
        return ({
            chainsOpen: false
        })
    },
    componentDidMount: function () {
        var CURRENT_URL = window.location.href.split('?')[0],
            $BODY = $('body'),
            $MENU_TOGGLE = $('#menu_toggle'),
            $SIDEBAR_MENU = $('#sidebar-menu'),
            $SIDEBAR_FOOTER = $('.sidebar-footer'),
            $LEFT_COL = $('.left_col'),
            $RIGHT_COL = $('.right_col'),
            $NAV_MENU = $('.nav_menu'),
            $FOOTER = $('footer');

        var setContentHeight = function () {
            // reset height
            $RIGHT_COL.css('min-height', $(window).height());

            var bodyHeight = $BODY.outerHeight(),
                footerHeight = $BODY.hasClass('footer_fixed') ? 0 : $FOOTER.height(),
                leftColHeight = $LEFT_COL.eq(1).height() + $SIDEBAR_FOOTER.height(),
                contentHeight = bodyHeight < leftColHeight ? leftColHeight : bodyHeight;

            // normalize content
            contentHeight -= $NAV_MENU.height() + footerHeight;

            $RIGHT_COL.css('min-height', contentHeight);
        };

        $('.toggle-menu').on('click', function(ev) {
            var $li = $(this).parent();

            if ($li.is('.active')) {
                $li.removeClass('active active-sm');
                $('ul:first', $li).slideUp(function() {
                    setContentHeight();
                });
            } else {
                // prevent closing menu if we are on child menu
                if (!$li.parent().is('.child_menu')) {
                    $SIDEBAR_MENU.find('li').removeClass('active active-sm');
                    $SIDEBAR_MENU.find('li ul').slideUp();
                }

                $li.addClass('active');

                $('ul:first', $li).slideDown(function() {
                    setContentHeight();
                });
            }

        });

        $('.single-menu').on('click', function (ev) {
            var $li = $('.toggle-menu').parent();
            $li.removeClass('active active-sm');
            $('ul:first', $li).slideUp(function() {
                setContentHeight();
            });
        });

        // recompute content when resizing
        $(window).smartresize(function(){
            setContentHeight();
        });

        setContentHeight();
    },
    render: function () {
        return (
            <div className="col-md-3 left_col">
                <div className="left_col scroll-view">
                    <div className="navbar nav_title" style={{border: 0}}>
                        <a href="index.html" className="site_title"><i className="fa fa-dashboard" /> <span>Cello Dashboard</span></a>
                    </div>

                    <div className="clearfix"></div>

                    <br />
                    <div id="sidebar-menu" className="main_menu_side hidden-print main_menu">
                        <div className="menu_section">
                            <ul className="nav side-menu">
                                <NavLink className="single-menu" to="/overview">
                                    <i className="fa fa-eye" /> Overview
                                </NavLink>
                                <NavLink className="single-menu" to="/hosts">
                                    <i className="fa fa-desktop" /> Hosts
                                </NavLink>
                                <li>
                                    <a className="toggle-menu"><i className="fa fa-chain" /> Chains<span className="fa fa-chevron-down" /></a>
                                    <ul className="nav child_menu">
                                        <NavLink to="/chains/active" activeClassName="current-page">
                                            Active Chains
                                        </NavLink>
                                        <NavLink to="/chains/inused" activeClassName="current-page">
                                            Inused Chains
                                        </NavLink>
                                        <NavLink to="/chains/release_history" activeClassName="current-page">
                                            Release History
                                        </NavLink>
                                    </ul>
                                </li>
                                <NavLink className="single-menu" to="/about">
                                    <i className="fa fa-info-circle" /> About
                                </NavLink>
                            </ul>
                        </div>

                    </div>
                    <div className="sidebar-footer hidden-small">
                    </div>
                </div>
            </div>
        )
    }
});

export default LeftNav;
