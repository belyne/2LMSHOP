$(document).ready(function () {
    const authToken = localStorage.getItem('authToken');
    $.ajax({
        type: 'GET',
        url: 'http://localhost:8000/cart/',
        headers: {
            'Authorization': `Token ${authToken}`
        },
        success: (res) => {
            $.each(res, (prop, value) => {
                let imageSrc = '../server' + value['image-urls'][0];
                let itemName = value['name'];
                let itemPrice = value['price'];
                let itemQuantity = value['quantity'];
                let itemQuantityInStock = value['quantity-in-stock']
                let subTotalPrice = itemPrice * itemQuantity;
                $('table.cart-table tbody').append(`
                <tr id='${prop}'>
                    <td><i class="fa-regular fa-circle-xmark cart-item-remove"></i></td>
                    <td><img src="${imageSrc}" alt=""></td>
                    <td>${itemName}</td>
                    <td class="item-price">$${itemPrice}</td>
                    <td><input class="quantity-input" type="number" value="${itemQuantity}" min=1 max="${itemQuantityInStock - 5}"></td>
                    <td class="sub-total-price">$${subTotalPrice}</td>
                </tr>
                `)
            })

            $('.quantity-input').on('input', function () {
                let row = $(this).closest('tr');
                let qty = $(this).val()
                let price = row.find('.item-price')
                row.find('.sub-total-price').text(`$${qty * parseInt(price.text().slice(1))}`)
            })

            const checkOut = () => {
                let cartSubTotal = 0;
                $('.sub-total-price').each(function (index, element) {
                    cartSubTotal += parseInt($(element).text().slice(1))
                })
                $('#cart-subtotal-price').find("td:nth-child(2)").text(`$${cartSubTotal}`)
                let totalPrice = cartSubTotal + parseInt($('#cart-shipping').find("td:nth-child(2)").text().slice(1))
                $('#cart-total-price').find("td:nth-child(2)").text(`$${totalPrice}`)

            }
            checkOut();

            $('.cart-item-remove').click(function () {
                let parentRow = $(this).closest('tr')
                $.ajax({
                    type: 'DELETE',
                    url: 'http://localhost:8000/cart/',
                    headers: {
                        'Authorization': `Token ${authToken}`
                    },
                    data : {
                        'item_id': parentRow.attr('id')
                    },
                    success: (res) => {
                        console.log(res)
                        checkOut();
                    }
                })
                parentRow.remove()
            })

            $('.shop-save-button').click(() => {
                $('table.cart-table tbody tr').each(function (index, element) {
                    let item_id = $(element).attr('id');
                    $.ajax({
                        type: 'PUT',
                        url: 'http://localhost:8000/cart/',
                        headers: {
                            'Authorization': `Token ${authToken}`
                        },
                        data: {
                            'item_id': item_id,
                            'quantity': parseInt($(element).find('.quantity-input').val())
                        },
                        success: function (res) {
                            console.log(res);
                        }
                    })
                })
                checkOut();
            })
        }
    })
})