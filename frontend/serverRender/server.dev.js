if (typeof global.window == "undefined") {
    global.window = {
      config: {
      },
    };
  }
  
  module.exports = require("../ssrBuild/server.js");
  