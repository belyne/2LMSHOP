$(document).ready(function () {
    $.ajax({
        type: 'GET',
        url: 'http://127.0.0.1:8000/products/',
        success: (res) => {
            console.log(res);
            $.each(res, (prop, value) => {
                let imageSrc = value['image-urls'][0];
                imageSrc = '../server' + imageSrc;
                let itemCategory = value['category'];
                let itemName = value['name'];
                let itemPrice = value['price'];
                let itemRating = () => {
                    let rate = '';
                    for (let i = 0; i < value['rating']; i++) {
                        rate += "<i class='fa-solid fa-star'></i>";
                    }
                    return rate;
                }
                $('.pro-container').append(`<div id="${prop}" class="pro"">
                    <img src=${imageSrc} alt="">
                    <div class="des">
                      <span>${itemCategory}</span>
                      <h4>${itemName}</h4>
                      <div class="star">
                        ${itemRating()}
                      </div>
                      <h5>$${itemPrice}</h5>
                    </div>
                    <a href="#"><i class="fa-solid fa-cart-shopping"></i></a>
                  </div>`)
            })
        }
    })
})