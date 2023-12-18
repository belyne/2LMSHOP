$(document).ready(function () {
    $('#checkout-form button').click((event) => {
        event.preventDefault();
        const token = localStorage.getItem('authToken')
        let fullName = $('#fullName').val()
        let email = $('#email').val()
        let address = $('#address').val()
        $.ajax({
            url: 'http://localhost:8000/checkout/',
            type: 'POST',
            headers: {
                'Authorization': `Token ${token}`
            },
            data: {
                'fullname': fullName,
                'email': email,
                'address': address
            },
            success: function (res) {
                $('section#checkout-form').html(`<h2 style='text-align: center;'>${res.message}</h2>`)
            }
        })
    })
})