// import {authToken} from './signup.js'
$(document).ready(function () {
    $('#signin form button').click((event) => {
        event.preventDefault();
        const username = $('input#username').val()
        const password = $('input#password').val()
        $.ajax({
            type: 'POST',
            url: 'http://127.0.0.1:8000/user/login/',
            data: {
                'username': username,
                'password': password
            },
            success: (res) => {
                if (res.hasOwnProperty('token')) {
                    localStorage.setItem('authToken', res.token)
                    window.location.href = './index.html'
                }
                else if (res.hasOwnProperty('error'))   console.log(res.error)
            }
        })
    })
})