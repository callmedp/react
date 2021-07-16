if (typeof global.window == "undefined") {
  global.window = {
    config: {
        isServerRendered: false,
        siteDomain: "http://127.0.0.1:8000",
        imageUrl: "/media/images/",
        resumeShineSiteDomain: "https://pp-resume.shine.com",
        shineSiteDomain: "https://mapi.shine.com",
        chatbotDomain: "https://learning1.shine.com/chatbot",
        trackingSiteDomain: "http://34.93.108.100:80"
    },
  };
}

module.exports = require("../ssrBuild/server.js");
