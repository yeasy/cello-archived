/**
 * Created by yuehaitao on 16/1/23.
 */
var webpack = require('webpack');
var BundleTracker = require('webpack-bundle-tracker');
var Config = require('./webpack.base.config');

var hostsConfig = new Config('./static/js/react/hosts/index', new BundleTracker({filename: './webpack-stats.json'}), "hosts.js");

module.exports = [
    hostsConfig.config
];