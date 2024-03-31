// Check if the createUserForm exists and set up its submit event
const createUserForm = document.getElementById('createUserForm');
if (createUserForm) {
    createUserForm.addEventListener('submit', function(e) {
        e.preventDefault();

        const email = document.getElementById('email').value;
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;

        fetch('/users-signup/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                email: email,
                username: username,
                password: password
            }),
        })
        .then(handleResponse)
        .catch(handleError);
    });
}

const loginForm = document.getElementById('loginForm');
if (loginForm) {
    loginForm.addEventListener('submit', function(e) {
        e.preventDefault();

        const username = document.getElementById('loginUsername').value;
        const password = document.getElementById('loginPassword').value;

        fetch('/users-login/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                username: username,
                password: password
            }),
        })
        .then(handleResponse)
        .catch(handleError);
    });
}

function handleResponse(response) {
    if (response.ok) {
        return response.json().then(data => {
            console.log(data);
            window.location.href = "/";
        });
    } else {
        throw new Error('Network response was not ok.');
    }
}

function handleError(error) {
    console.error('Error:', error);
}
