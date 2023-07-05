
function showAllDishes() {
  // Fetch the dishes data from the backend API
  fetch('http://127.0.0.1:5000/menu')
    .then(response => response.json())
    .then(data => {
      // Get the container element where the dishes will be displayed
      const container = document.getElementById('dishesContainer');

      // Clear the container before adding new dishes
      container.innerHTML = '';

      // Iterate through each dish and create the HTML elements
      data.forEach(dish => {
        // Create a div element for each dish
        const dishDiv = document.createElement('div');
        dishDiv.classList.add('dish');

        // Create the dish details elements
        const name = document.createElement('h3');
        name.textContent = dish[1];
        const price = document.createElement('p');
        price.textContent = `Price: $${dish[2]}`;
        const availability = document.createElement('p');
        availability.textContent = `Availability: ${dish[3]}`;

        // Append the dish details to the dish div
        dishDiv.appendChild(name);
        dishDiv.appendChild(price);
        dishDiv.appendChild(availability);

        // Append the dish div to the container
        container.appendChild(dishDiv);
      });
    })
    .catch(error => {
      console.error('Error:', error);
    });
}

// Call the function to display the dishes on page load
showAllDishes();

  // // Handle form submission
  // const orderForm = document.getElementById('orderForm');
  // orderForm.addEventListener('submit', event => {
  //   event.preventDefault();

  //   const customerName = document.getElementById('customerName').value;
  //   const dishIds = document.getElementById('dishIds').value.split(',');

  //   // Send the order data to the backend
  //   fetch('http://127.0.0.1:5000/place-order', {
  //     method: 'POST',
  //     headers: {
  //       'Content-Type': 'application/json'
  //     },
  //     body: JSON.stringify({ customerName, dishIds })
  //   })
  //     .then(response => {
  //       if (response.ok) {
  //         return response.json();
  //       } else {
  //         throw new Error('Error placing order. Please try again.');
  //       }
  //     })
  //     .then(data => {
  //       // Display the order status
  //       const orderStatus = document.createElement('p');
  //       orderStatus.classList.add('order-status');
  //       orderStatus.textContent = `Order ID: ${data.orderId} - Status: ${data.status}`;
  //       orderForm.appendChild(orderStatus);

  //       // Clear the form inputs
  //       document.getElementById('customerName').value = '';
  //       document.getElementById('dishIds').value = '';
  //     })
  //     .catch(error => {
  //       // Display error message
  //       const errorMessage = document.createElement('p');
  //       errorMessage.classList.add('error-message');
  //       errorMessage.textContent = error.message;
  //       orderForm.appendChild(errorMessage);
  //     });
  // });


// window.addEventListener("load", () => {
//   let promise = fetch("http://127.0.0.1:5000/menu")
//   promise.then((res) => {
//     // console.log(1);
//     return res.json();
// })
//     .then((response) => {
//         // console.log(2,3,response);
//         console.log(response);
//     })
// })

// Get the add dish form and submit button
const addDishForm = document.getElementById('addDishForm');
const addDishButton = document.getElementById('add-dish-button');

// Add event listener to the add dish form submit button
addDishForm.addEventListener('submit', function(event) {
  event.preventDefault(); // Prevent form submission
  addDish(); // Call the addDish function
});

// Get the update dish form and submit button
const updateDishForm = document.getElementById('updateDishForm');
const updateDishButton = document.getElementById('update-dish-button');

// Add event listener to the update dish form submit button
updateDishForm.addEventListener('submit', function(event) {
  event.preventDefault(); // Prevent form submission
  updateDish(); // Call the updateDish function
});


// Function to add a new dish
function addDish() {
  // Get the dish details from the form inputs
  const name = document.getElementById('add-dish-name').value;
  const price = document.getElementById('add-dish-price').value;
  const availability = document.getElementById('add-dish-availability').checked ? 'Available' : 'Not Available';

  // Create an object with the dish details
  const dish = {
    name: name,
    price: price,
    availability: availability
  };

  // Send a POST request to the backend API to add the dish
  fetch('http://127.0.0.1:5000/menu', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(dish)
  })
    .then(response => response.json())
    .then(data => {
      // Display a success message
      alert(data.message);

      // Clear the form inputs
      document.getElementById('add-dish-name').value = '';
      document.getElementById('add-dish-price').value = '';
      document.getElementById('add-dish-availability').checked = false;

      // Refresh the dishes list
      showAllDishes();
    })
    .catch(error => {
      console.error('Error:', error);
    });
}

// Function to update an existing dish
function updateDish() {
  // Get the dish details from the form inputs
  const id = document.getElementById('update-dish-id').value;
  const name = document.getElementById('update-dish-name').value;
  const price = document.getElementById('update-dish-price').value;
  const availability = document.getElementById('update-dish-availability').checked ? 'Available' : 'Not Available';

  // Create an object with the dish details
  const dish = {
    name: name,
    price: price,
    availability: availability
  };

  // Send a PUT request to the backend API to update the dish
  fetch(`http://127.0.0.1:5000/menu/${id}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(dish)
  })
    .then(response => response.json())
    .then(data => {
      // Display a success message
      alert(data.message);

      // Clear the form inputs
      document.getElementById('update-dish-id').value = '';
      document.getElementById('update-dish-name').value = '';
      document.getElementById('update-dish-price').value = '';
      document.getElementById('update-dish-availability').checked = false;

      // Refresh the dishes list
      showAllDishes();
    })
    .catch(error => {
      console.error('Error:', error);
    });
}
