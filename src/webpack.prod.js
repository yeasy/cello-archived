/**
 * Created by yuehaitao on 16/1/23.
 */
var webpack = require('webpack');
var BundleTracker = require('webpack-bundle-tracker');
var Config = require('./webpack.prod.config');

var hostConfig = new Config('./static/js/react/hosts/index', new BundleTracker({filename: './webpack-stats-prod.json'}), "hosts.js");

module.exports = [
    hostConfig.config
];
