
const { override } = require('customize-cra');

module.exports = override(
  (config) => {
    // Fix for webpack-dev-server allowedHosts issue
    if (config.devServer) {
      config.devServer.allowedHosts = 'all';
      config.devServer.host = 'localhost';
    }
    return config;
  }
);
