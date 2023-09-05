// Select all elements with class 'update-cart'
const updateButtons = document.querySelectorAll('.update-cart');

// Add click event listeners to each button
updateButtons.forEach((button) => {
    button.addEventListener('click', handleUpdateClick);
});

function handleUpdateClick(event) {
    const dishId = event.target.dataset.dish;
    const action = event.target.dataset.action;

    if (user === 'AnonymousUser') {
        console.log('Not logged');
    } else {
        updateUserOrder(dishId, action);
    }
}

function updateUserOrder(dishId, action) {
    console.log('Logged');
    const url = '/update_item/';

    fetch(url, {
        method: 'POST',
        headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({ dishId, action }),
    })
    .then((response) => response.json())
    .then((data) => {
        console.log('Data:', data);
        location.reload();
    });
}