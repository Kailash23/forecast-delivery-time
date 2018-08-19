const url = "http://localhost:5000/get-delivery-estimate/?city=";

const make_request = function() {

    // make a request to the server and send the name
    const req = new XMLHttpRequest();

    // capture the response and store it in a variable
    req.onreadystatechange = function() {
        if (req.readyState === XMLHttpRequest.DONE) {
            if (req.status === 200) {
                const result = JSON.parse(req.responseText);
                console.log(`It'll take ${result.result} hours for your product to be delivered!`);
            } else if (req.status === 403) {
                alert("Status 403!");
            } else if (req.status === 500) {
                alert("Status 500!");
            } else {
                alert("Unexpected Error Occured");
            }
        }
    };
    
    // make the request
    req.open("GET", `${url}Pune`, true);
    req.send(null);
};

make_request();