$(document).ready(function() {
    $('#login-form').submit(function(event) {
        event.preventDefault(); // Prevent default form submission

        var username = $('#username').val();
        var password = $('#password').val();

        var requestData = {
            username: username,
            password: password
        };
        $.ajax({
            type: 'POST',  // Set to POST
            url: "/authenticate",  // The Flask route you set up
            data: JSON.stringify(requestData),
            contentType: 'application/json',
            // ... other options ...
        });
        $.post('user_management/authenticate', requestData, function(response) {
            $('#authenticationStatus').text(response); // Display the result
        });
    });
});
