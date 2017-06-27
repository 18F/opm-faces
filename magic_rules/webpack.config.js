var webpack = require('webpack');
module.exports = [
  {
  name: 'rules',
  entry: [
    "./js/rules.js"
  ],
  output: {
    path: __dirname + '/static/js',
    filename: "rules.js"
  },
  module: {
    loaders: [
      {
        test: /\.js?$/,
        loader: 'babel-loader',
        query: {
          presets: ['es2015', 'react']
        },
        exclude: /node_modules/
      }
    ]
  },
  plugins: [
  ]
}, {
  name: 'objects',
  entry: [
    "./js/objects.js"
  ],
  output: {
    path: __dirname + '/static/js',
    filename: "objects.js"
  },
  module: {
    loaders: [
      {
        test: /\.js?$/,
        loader: 'babel-loader',
        query: {
          presets: ['es2015', 'react']
        },
        exclude: /node_modules/
      }
    ]
  },
  plugins: [
  ]
}, {
  name: 'calculations',
  entry: [
    "./js/calculations.js"
  ],
  output: {
    path: __dirname + '/static/js',
    filename: "calculations.js"
  },
  module: {
    loaders: [
      {
        test: /\.js?$/,
        loader: 'babel-loader',
        query: {
          presets: ['es2015', 'react']
        },
        exclude: /node_modules/
      }
    ]
  },
  plugins: [
  ]
}
];
