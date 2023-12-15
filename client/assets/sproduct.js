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
            $('div.single-pro-details h2').text(res.category)
            $('div.single-pro-details .product-name').text(res.name)
            $('div.single-pro-details .product-price').text(`$${res.price}`)
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
    })
}