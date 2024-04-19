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
        return false; // Kein asynchroner Prozess, kein Kanal offen halten
    }
    else if (request.type === "getAuthStatus") {
        fetch('http://127.0.0.1:5000/authorize-user', { 
            method: 'GET',
            headers: {
                token: tokenVal
            },
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Netzwerkantwort war nicht ok');
            }
            return response.json();
        })
        .then(data => {
            sendResponse({authStatus: true});
        })
        .catch(error => {
            console.error('Error:', error);
            sendResponse({authStatus: false});
        });
        return true; // Nachrichtenkanal offen halten
    }
});




