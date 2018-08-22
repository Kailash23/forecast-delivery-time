function get_template(id, name, thumb, price) { 
    return `<div class="col-md-4">
                <div class="card mb-4 shadow-sm">
                    <img class="card-img-top" src=${thumb} alt="Card image cap">
                        <div class="card-body">
                            <p class="card-text">${name}</p>
                            <div class="d-flex justify-content-between align-items-center">
                                <form class="btn-group" action="/place-order" method="POST">
                                    <input type="hidden" id="order_id" name="order_id" value=${id}>
                                    <button type="submit" class="btn btn-sm btn-outline-secondary">Buy Now</button>
                                </form>
                                <small class="text-muted">${price}</small>
                            </div>
                        </div>
                    </div>
                </div>`;
}

const url = "http://localhost:5000/get-products";


$(document).ready(function(){

    // make a request to the server and send the name
    const req = new XMLHttpRequest();

    // capture the response and store it in a variable
    req.onreadystatechange = function() {
        if (req.readyState === XMLHttpRequest.DONE) {
            if (req.status === 200) {
                const results = JSON.parse(req.responseText);
                results.forEach(result => {
                    $('#products-container').append(get_template(result.id, result.name, result.thumb, result.price)); 
                });
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
    req.open("GET", url, true);
    req.send(null);

});