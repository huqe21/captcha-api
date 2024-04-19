chrome.runtime.sendMessage({type: "getAuthStatus"}, function(response) {
    console.log("popup.js")
    console.log(response);
    if (response.authStatus) {
        document.getElementById("text").innerText = "authorized!";
        document.getElementById("colorPoint").style.backgroundColor = "green";
    } else {
        document.getElementById("text").innerText = "unauthorized!";
        document.getElementById("colorPoint").style.backgroundColor = "red";
    }
}
);