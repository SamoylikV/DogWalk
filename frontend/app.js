document.getElementById('createItemForm').addEventListener('submit', function(e) {
    e.preventDefault();

    const itemName = document.getElementById('itemName').value;
    const itemPrice = document.getElementById('itemPrice').value;

    fetch('/items', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            // Add any required headers, such as authentication tokens
        },
        body: JSON.stringify({
            name: itemName,
            price: itemPrice
        }),
    })
    .then(response => response.json())
    .then(data => console.log(data))
    .catch((error) => {
        console.error('Error:', error);
    });
});
