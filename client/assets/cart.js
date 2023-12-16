$(document).ready(function () {
    const authToken = localStorage.getItem('authToken');
    let cartSubTotal = 0;
    $.ajax({
        type: 'GET',
        url: 'http://localhost:8000/cart/',
        headers: {
            'Authorization': `Token ${authToken}`
        },
        success: (res) => {
            console.log(res)
            $.each(res, (prop, value) => {
                let imageSrc = '../server' + value['image-urls'][0];
                let itemName = value['name'];
                let itemPrice = value['price'];
                let itemQuantity = value['quantity'];
                let subTotalPrice = itemPrice * itemQuantity;
                cartSubTotal += subTotalPrice
                $('table.cart-table tbody').append(`
                <tr>
                    <td><i class="fa-regular fa-circle-xmark cart-item-remove"></i></td>
                    <td><img src="${imageSrc}" alt=""></td>
                    <td>${itemName}</td>
                    <td>$${itemPrice}</td>
                    <td><input type="number" value="${itemQuantity}" min=1></td>
                    <td class="sub-total-price">$${subTotalPrice}</td>
                </tr>
                `)
            })
            console.log(cartSubTotal)

            const checkOut = () => {
                $('#cart-subtotal-price').find("td:nth-child(2)").text(`$${cartSubTotal}`)
                let totalPrice = cartSubTotal + parseInt($('#cart-shipping').find("td:nth-child(2)").text().slice(1))
                $('#cart-total-price').find("td:nth-child(2)").text(`$${totalPrice}`)
            }
            checkOut();
            // $('.shop-save-button').click(() => {
            //     checkOut();
            // })
        }
    })
})