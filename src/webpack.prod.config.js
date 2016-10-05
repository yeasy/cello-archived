/**
 * Created by yuehaitao on 16/1/23.
 */
var path = require("path");
var webpack = require('webpack');
var precss       = require('precss');
var autoprefixer = require('autoprefixer');
var atImport = require("postcss-import");


function Config(entry, plugins, filename) {
  this.config = {
    context: __dirname,

    entry: entry,

    output: {
      path: path.resolve('./static/dist/'),
      filename: filename
    },

    plugins: [
      // removes a lot of debugging code in React
      new webpack.DefinePlugin({
        'process.env': {
          'NODE_ENV': JSON.stringify('production')
        }}),

      // keeps hashes consistent between compilations
      new webpack.optimize.OccurenceOrderPlugin(),

      // minifies your code
      new webpack.optimize.UglifyJsPlugin({
        compressor: {
          warnings: false
        }
      }),
      plugins
    ], // add all common plugins here

    module: {
      loaders: [
        {test: /\.jsx?$/, exclude: /node_modules/, loader: 'babel'},
        { test: /\.css$/, loader: "style-loader!css-loader!postcss-loader" },
        {
          test: /\.scss$/,
          loader: "style-loader!css-loader!postcss-loader"
        }
      ] // add all common loaders here
    },

    postcss: function(webpack) {
      return [
        autoprefixer({
          browsers: ['last 3 versions']
        }),
        atImport({
          addDependencyTo: webpack
        }),
        require('precss')
      ];
    },

    resolve: {
      modulesDirectories: ['node_modules', 'bower_components'],
      extensions: ['', '.js', '.jsx']
    }
  };
}

module.exports = Config;
