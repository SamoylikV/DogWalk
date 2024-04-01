const createUserForm = document.getElementById('createUserForm');
if (createUserForm) {
    createUserForm.addEventListener('submit', function (e) {
        e.preventDefault();

        const email = document.getElementById('email').value;
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;
        const walker = +document.getElementById('walker').checked;

        fetch('/users-signup/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                email: email,
                username: username,
                password: password,
                walker: walker
            }),
        })
            .then(handleResponse)
            .catch(handleError);
    });
}

const loginForm = document.getElementById('loginForm');
if (loginForm) {
    loginForm.addEventListener('submit', function (e) {
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
const logoutButton = document.getElementById('logoutButton');
if (logoutButton) {
    logoutButton.addEventListener('click', function (e) {
        e.preventDefault();

        fetch('/logout', {
            method: 'GET',
        })
            .then(handleResponse)
            .catch(handleError);
    });
}


// document.addEventListener('DOMContentLoaded', function () {
//     var map = L.map('map').setView([59.9342802, 30.3350986], 13);
//
//     L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
//         attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
//     }).addTo(map);
// });

document.addEventListener('DOMContentLoaded', function () {
    const accessToken = localStorage.getItem('access_token');
    if (!accessToken) {
        window.location.href = "/login";
    } else {
        document.getElementById('email').textContent = localStorage.getItem('user_email');
        document.getElementById('userEmail').style.display = 'block';
        document.getElementById('logoutButton').style.display = 'block';
        var map = L.map('map').setView([59.9342802, 30.3350986], 13);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        }).addTo(map);
    }
});

function handleResponse(response) {
    if (response.ok) {
        return response.json().then(data => {
            console.log(data);
            if (response.url.endsWith('/users-login/')) {
                localStorage.setItem('access_token', data.access_token);
                localStorage.setItem('user_email', data.email);
            }
            window.location.href = "/";
        });
    } else {
        response.json().then(data => {
            console.error('Error:', data.detail);
            document.getElementById('error_message').textContent = data.detail;
        });
        throw new Error('Network response was not ok.');
    }
}

function handleError(error) {
    console.error('Error:', error);
}
