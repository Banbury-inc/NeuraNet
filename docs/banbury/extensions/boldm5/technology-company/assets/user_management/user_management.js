document.getElementById('login-button').addEventListener('click', async function() {
    const usernameTextbox = document.getElementById('username');  // Assuming 'username' is the id of the username textbox
    const passwordTextbox = document.getElementById('password');  // Assuming 'password' is the id of the password textbox

    const username = usernameTextbox.value;
    const password = passwordTextbox.value;
    localStorage.setItem('username', username)
    localStorage.setItem('password', password)
    try {
        const response = await fetch(`http://127.0.0.1:5000/authenticate?username=${username}&password=${password}`);
        const data = await response.json();

        if (data.username) {
            // redirect to dashboard
            window.location.href = 'Athena_Dashboard.html?cid=${data.cid}';


        } else {
            alert('Username not found in response.');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred while fetching data.');
    }
});


