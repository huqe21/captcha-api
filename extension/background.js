let tokenVal = null;


chrome.action.onClicked.addListener((tab) => {
    chrome.scripting.executeScript({
      target: {tabId: tab.id},
      files: ['content.js']
    });
  });

  chrome.identity.getAuthToken({ 'interactive': true }, function(token) {
    // Use the token.
    tokenVal = token;
  });
  
  setInterval(() => {
    chrome.identity.getAuthToken({ 'interactive': true }, function(token) {
      // Use the token.
      tokenVal = token;
    });
  }, 60000);

  chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.type === "getAuthToken") {
        sendResponse({token: tokenVal});
    }
  });