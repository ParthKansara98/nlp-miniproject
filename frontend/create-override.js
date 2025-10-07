const fs = require('fs');
const path = require('path');

// Create a custom webpack config override
const configPath = path.join(__dirname, 'config-overrides.js');

const overrideContent = `
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
`;

// Write the override file
fs.writeFileSync(configPath, overrideContent);
console.log('Config override created successfully!');