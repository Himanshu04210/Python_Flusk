// Function to fetch and display the menu
function showMenu() {
  fetch('http://127.0.0.1:5000/menu')
    .then(response => response.json())
    .then(data => {
      const dishList = document.getElementById('dish-list');

      // Clear the dish list before adding new dishes
      dishList.innerHTML = '';

      // Iterate through each dish and create list items
      for (let i = 0; i < data.length; i += 2) {
        const rowContainer = document.createElement('div');
        rowContainer.classList.add('row');

        const dish1 = data[i];
        const dish2 = data[i + 1];

        // Create a container for the first dish
        const dish1Container = createDishContainer(dish1);
        rowContainer.appendChild(dish1Container);

        // Create a container for the second dish if available
        if (dish2) {
          const dish2Container = createDishContainer(dish2);
          rowContainer.appendChild(dish2Container);
        }

        dishList.appendChild(rowContainer);
      }
    })
    .catch(error => {
      console.error('Error:', error);
    });
}
// Call the showMenu function to display the menu on page load


function createDishContainer(dish) {
  const container = document.createElement('div');
  container.classList.add('dish-item');

  const dishId = document.createElement('span');
  dishId.classList.add('dish-id');
  dishId.textContent = `ID: ${dish[0]}`;

  const dishName = document.createElement('h3');
  dishName.textContent = dish[1];

  const dishPrice = document.createElement('p');
  dishPrice.textContent = `Price: $${dish[2]}`;

  const dishAvailability = document.createElement('p');
  dishAvailability.textContent = `Availability: ${dish[3]}`;

  container.appendChild(dishId);
  container.appendChild(dishName);
  container.appendChild(dishPrice);
  container.appendChild(dishAvailability);

  return container;
}

showMenu();




// Add Dish Form Submission
const addDishForm = document.getElementById('add-dish-form');

addDishForm.addEventListener('submit', function(event) {
  event.preventDefault(); // Prevent form submission
  const dishName = document.getElementById('dish-name').value;
  const dishPrice = document.getElementById('dish-price').value;
  let dishAvailability = document.getElementById('dish-availability').value;

  if(dishAvailability == "avilable") dishAvailability = true;
  else dishAvailability = false;

  // Create a new dish object with the form data
  const dish = {
    name: dishName,
    price: dishPrice,
    availability: dishAvailability
  };
  console.log(dish);
  // Send the dish data to the server
  fetch('http://127.0.0.1:5000/menu', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(dish)
  })
  .then(response => response.json())
  .then(data => {
    console.log(data); // Log the response data
    // Clear the form inputs
    addDishForm.reset();
    // Refresh the menu to display the updated list
    showMenu();
  })
  .catch(error => {
    console.error('Error:', error);
  });
});

// Update Dish Form Submission
const updateDishForm = document.getElementById('update-dish-form');

updateDishForm.addEventListener('submit', function(event) {
  event.preventDefault(); // Prevent form submission
  const dishId = document.getElementById('dish-id').value;
  const updatedDishName = document.getElementById('updated-dish-name').value;
  const updatedDishPrice = document.getElementById('updated-dish-price').value;
  let updatedDishAvailability = document.getElementById('updated-dish-availability').value;
  if(updatedDishAvailability == "unavailable") dishAvailability = false;
  else updatedDishAvailability = true;
  // Create a new updated dish object with the form data
  const updatedDish = {
    id: dishId,
    name: updatedDishName,
    price: updatedDishPrice,
    availability: updatedDishAvailability
  };

  console.log(updatedDish);
  // Send the updated dish data to the server
  fetch(`http://127.0.0.1:5000/menu/${dishId}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(updatedDish)
  })
  .then(response => response.json())
  .then(data => {
    console.log(data); // Log the response data
    // Clear the form inputs
    updateDishForm.reset();
    // Refresh the menu to display the updated list
    showMenu();
  })
  .catch(error => {
    console.error('Error:', error);
  });
});
