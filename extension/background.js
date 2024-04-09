chrome.action.onClicked.addListener((tab) => {
    chrome.scripting.executeScript({
      target: {tabId: tab.id},
      files: ['content.js']
    });
  });
  
  chrome.identity.getAuthToken({ 'interactive': true }, function(token) {
    // Use the token.
    console.log(token);
  });