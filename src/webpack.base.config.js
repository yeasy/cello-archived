/**
 * Created by yuehaitao on 16/1/23.
 */
var path = require("path");
var webpack = require('webpack');
var precss       = require('precss');
var autoprefixer = require('autoprefixer');
var BundleTracker = require('webpack-bundle-tracker');


function Config(entry, stats_file, filename, prod=false) {
  this.config = {
    context: __dirname,

    entry: entry,

    output: {
      path: path.resolve('./static/js/bundles/'),
      filename: filename
    },

    plugins: [
      new BundleTracker({filename: stats_file})
    ], // add all common plugins here

    module: {
      loaders: [
        // we pass the output from babel loader to react-hot loader
        { test: /\.jsx?$/, exclude: /node_modules/, loaders: ['babel'] },
        { test: /\.css$/, loader: "style-loader!css-loader!postcss-loader" },
        {
          test: /\.json$/,
          loader: 'json'
        },
        {
          test: /\.scss$/,
          loaders: ['style', 'css', 'postcss', 'sass']
        }
      ]
    },

    postcss() {
      return [autoprefixer];
    },

    resolve: {
      modulesDirectories: ['node_modules', 'bower_components'],
      extensions: ['', '.js', '.jsx']
    }
  };
  if (prod) {
    var plugins = this.config["plugins"];
    plugins.push(
        new webpack.DefinePlugin({
          'process.env': {
            'NODE_ENV': JSON.stringify('production')
          }})
    );
    plugins.push(
        new webpack.optimize.OccurenceOrderPlugin()
    );
    plugins.push(
        new webpack.optimize.UglifyJsPlugin({
          compressor: {
            warnings: false
          }
        })
    );
    this.config["plugins"] = plugins;
    this.config["output"] = {
      path: path.resolve('./static/js/bundles/'),
      filename: filename
    }
  }
}

module.exports = Config;
