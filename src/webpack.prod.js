/**
 * Created by yuehaitao on 16/1/23.
 */
var webpack = require('webpack');
var Config = require('./webpack.base.config');

var dashboardConfig = new Config('./static/js/react/index', './webpack-stats-prod.json', "cello.js", true);

module.exports = [
    dashboardConfig.config
];
