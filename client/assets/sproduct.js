const urlParams = new URLSearchParams(window.location.search);
const id = urlParams.get('id');
console.log(id)
if (id === null || id === undefined) {
    $('body').html("<h1 style='text-align: center;'> Product not Found </h1>");
}
else {
    $.ajax({
        type: 'GET',
        url: `http://localhost:8000/product/${id}`,
        success: (res) => {
            console.log(res);
            if (res.hasOwnProperty('error')) {
                $('body').html(`<h1 style='text-align: center;'> ${res.error} </h1>`);
            }
            else {
                $('div.single-pro-details h2').text(res.category)
                $('div.single-pro-details .product-name').text(res.name)
                $('div.single-pro-details .product-price').text(`$${res.price}`)
                $('.single-pro-details input').attr('max', res.quantity_in_stock - 5)
                res['image_urls'].forEach((element, index) => {
                    element = '../server' + element
                    if (index === 0) {
                        $("div.large-image").html(`<img src="${element}" width="100%" id="MainImg"  alt="">`)
                    }
                    else {
                        $('div.small-img-group').append(`<div class="small-img-col">
                             <img src="${element}" width="100%" class="small-img" alt="">
                            </div>`)
                    }
                })
            }
        }
    })


    $('.single-pro-details .add-to-cart').click(() => {
        // console.log($('.single-pro-details input').val())
        const authToken = localStorage.getItem('authToken')
        if (authToken === null || authToken === undefined) {
            window.location.href = '/signin.html'
        }
        else {
            $.ajax({
                url: 'http://localhost:8000/addCart/',
                type: 'POST',
                headers: {
                    'Authorization': `Token ${authToken}`
                },
                data: {
                    'item_id': id,
                    'quantity': $('.single-pro-details input').val()
                },
                success: (res) => {
                    console.log(res.statusCode)
                    if (res.statusCode === 200) {
                        window.location.href = 'cart.html'
                    }
                }
            })
        }
        
    })
}