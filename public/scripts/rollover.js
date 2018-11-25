function get_template( delivery_estimate, product_name, address) { 
  return `<div class="jugger container estimates">
            <div class="my-3 p-3 bg-white rounded shadow-sm">
                <h6 class="border-bottom border-gray pb-2 mb-0"></h6>
                <div class="media text-muted pt-3">
                  <img data-src="holder.js/32x32?theme=thumb&bg=007bff&fg=007bff&size=1" alt="" class="mr-2 rounded">
                  <p class="media-body pb-3 mb-0 small lh-125 border-bottom border-gray">
                    <strong class="d-block address text-gray-dark">${product_name}</strong>
                    ${address}
                  </p>
                </div>
            
                  <small class="d-block text-right mt-3">
                      <div class="days-left container">
                        <span class="estimate_number d-none">${delivery_estimate} hrs</span>
                      </div> 
                  </small>
              </div>
          </div>`;
}

const attach_listeners = function() {
  $('.estimates').mouseover(function() {
    $(this).find('.estimate_number').toggleClass('d-none');
  });
  $('.estimates').mouseout(function() {
    $(this).find('.estimate_number').toggleClass('d-none');
  });
};

const orders_url = "http://localhost:5000/get-orders";

$(document).ready(function(){

  // make a request to the server and send the name
  const req = new XMLHttpRequest();

  // capture the response and store it in a variable
  req.onreadystatechange = function() {
      if (req.readyState === XMLHttpRequest.DONE) {
          if (req.status === 200) {
              const results = JSON.parse(req.responseText);
              results.forEach(result => {
                  $('#orders-container').append(get_template(result.delivery_estimate, result.name, result.address)); 
              });
              attach_listeners();
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
  req.open("GET", orders_url, true);
  req.send(null);
});

