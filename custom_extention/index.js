async function search_history() {
    return new Promise((resolve, reject) => {
        chrome.history.search({text: ''}, (results) => {
            if (chrome.runtime.lastError) {
                reject(chrome.runtime.lastError);
            } else {
                resolve(results);
            }
        });
    });
}

async function fetchDataAndSendToServer() {
    try {
        const data = await search_history(); // Wait for the Promise to resolve and get the result
        // Do something with the data
        console.log("Data:", data);
        send_data(data)
        // Send data to server using XHR or fetch()
        // ...
    } catch (error) {
        console.error("Error:", error);
    }
}

fetchDataAndSendToServer();


function send_data(data){
    var obj = JSON.stringify({
        "data": data
    });

    var xhr = new XMLHttpRequest();

    xhr.withCredentials = true;

    xhr.addEventListener("readystatechange", function() {
        if(this.readyState === 4) {
            console.log(this.responseText);
            document.getElementById('result').innerHTML = this.responseText
        }
    });

    xhr.open("POST", "http://3.111.37.230/pintrverse/history-extension-api/");
    xhr.setRequestHeader("Content-Type", "application/json");
    // WARNING: Cookies will be stripped away by the browser before sending the request.
    //   xhr.setRequestHeader("Cookie", "csrftoken=LmB9YPxwENib0sBVaviYlgM3ekbSE3CB8nYiqLSEpPVp2Hj2dDmXqZNR8jMtT4pc");

    xhr.send(obj);
}

