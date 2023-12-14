$(document).ready(function () {
    $('#signup form button').click(() => {
        const username = $('input#username').val()
        const password = $('input#password').val()
        const email = $('input#email').val()

        $.ajax({
            type: 'POST',
            url: 'http://127.0.0.1:8000/user/register1/',
            data: {
                'username': username,
                'password': password,
                'email': email
            },
            success: (res) => {
                console.log(res.token);
                // authToken = token;
            }
        })
    })
})
