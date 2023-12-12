$(document).ready(function () {
    $('#signin form button').click(() => {
        const username = $('input#username').val()
        const password = $('input#password').val()
        const token = localStorage.getItem('authToken');
        $.ajax({
            type: 'POST',
            url: 'http://127.0.0.1:8000/user/login/',
            headers: {
                'Authorization': `Token ${token}`
            },
            data: {
                'username': username,
                'password': password
            },
            success: (res) => {
                if (res.hasOwnProperty('token'))    console.log(res.token);
                else if (res.hasOwnProperty('error'))   console.log(res.error)
            }
        })
    })
})