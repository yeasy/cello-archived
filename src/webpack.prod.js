/**
 * Created by yuehaitao on 16/1/23.
 */
var webpack = require('webpack');
var BundleTracker = require('webpack-bundle-tracker');
var Config = require('./webpack.prod.config');

var dashboardConfig = new Config('./static/js/react/index', new BundleTracker({filename: './webpack-stats-prod.json'}), "cello.js");

module.exports = [
    dashboardConfig.config
];
