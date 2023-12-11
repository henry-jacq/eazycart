// Add to car
$('.btn-add-cart').on('click', function(e) {
    product_id = $(this).attr('data-id');

    var data = {
        "product_id": parseInt(product_id),
        "product_qty": 1
    };

    if ($(this).children().hasClass('bi-cart-plus')) {
        $.ajax({
            url: "/api/cart/add",
            type: "POST",
            contentType: "application/json", // Set the Content-Type header
            data: JSON.stringify(data),
            success: function() {
                $(this).html('');
                $(this).html('<i class="bi bi-check2 me-2"></i>Added to cart');
                if ($(this).hasClass('btn-outline-secondary')) {
                    $(this).removeClass('btn-outline-secondary');
                    $(this).addClass('btn-secondary')
                }
                $(this).prev().attr('readonly', 'true');
            },
            error: function(error) {
                console.error(error);
            }
        });
    } else {
        $.ajax({
            url: "/api/cart/remove",
            type: "POST",
            contentType: "application/json", // Set the Content-Type header
            data: JSON.stringify(data),
            success: function() {
                $(this).html('');
                $(this).html('<i class="bi bi-cart-plus me-2"></i>Add to cart');
                if ($(this).hasClass('btn-secondary')) {
                    $(this).removeClass('btn-secondary');
                    $(this).addClass('btn-outline-secondary')
                }
                $(this).prev().removeAttr('readonly')
            },
            error: function(error) {
                console.error(error);
            }
        });
    }
});

// Remove from cart
$('.remove-from-cart').on('click', function(e) {
    itemName = $(this).parents('.product-price-section').prev().find('.product-name').html();
    pid = $(this).attr('data-id');
    $this = $(this).parents('.cart-item')
    d = new Dialog('Remove from cart', 'Are you sure you want to remove the <b>' + itemName + '</b> from the cart?');
    d.setButtons([{
            'name': "Cancel",
            "class": "btn-secondary",
            "onClick": function(event) {
                $(event.data.modal).modal('hide');
            }
        },
        {
            'name': "Remove",
            "class": "btn-danger",
            "onClick": function(event) {
                $.ajax({
                    url: "/api/cart/remove",
                    type: "POST",
                    contentType: "application/json", // Set the Content-Type header
                    data: JSON.stringify({ "product_id": parseInt(pid) }),
                    success: function() {
                        $this.remove();
                    },
                    error: function(error) {
                        console.error(error);
                    }
                });

                $(event.data.modal).modal('hide')
            }
        }
    ]);
    d.show();
})

// Increase count of items
$('.items-increase').click(function(e) {
    c_qty = parseInt($(this).prev().html());
    max = parseInt($(this).prev().attr('data-max'))
    total_price_el = $(this).parents('.quantity-section').next().find('.total-item-price');
    original_price = parseInt($(this).parents('.quantity-section').prev().find('.price-per-item').html())
    if (max > c_qty) {
        c_qty += 1;
        new_price = original_price + parseInt(total_price_el.html())
        total_price_el.html(new_price)
    }
    $(this).prev().html(c_qty);
});

// Decrease count of items
$('.items-decrease').click(function(e) {
    c_qty = parseInt($(this).next().html());
    total_price_el = $(this).parents('.quantity-section').next().find('.total-item-price');
    original_price = parseInt($(this).parents('.quantity-section').prev().find('.price-per-item').html())
    if (c_qty > 1) {
        c_qty -= 1;
        new_price = parseInt(total_price_el.html()) - original_price
        total_price_el.html(new_price)
    }
    $(this).next().html(c_qty);
});