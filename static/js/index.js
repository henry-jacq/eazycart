// Add to cart
$('.btn-add-cart').on('click', function(e) {
    product_id = $(this).attr('data-id');

    var data = {
        "product_id": parseInt(product_id),
        "product_qty": 1
    };

    if ($(this).children().hasClass('bi-cart-plus')) {
        $this = $(this);
        $this.html('');
        $this.html('<i class="bi bi-check2 me-2"></i>Added to cart');
        if ($this.hasClass('btn-outline-secondary')) {
            $this.removeClass('btn-outline-secondary');
            $this.addClass('btn-secondary')
        }
        $.ajax({
            url: "/api/cart/add",
            type: "POST",
            contentType: "application/json", // Set the Content-Type header
            data: JSON.stringify(data),
            success: function() {
                $this.html('');
                $this.html('<i class="bi bi-check2 me-2"></i>Added to cart');
                if ($this.hasClass('btn-outline-secondary')) {
                    $this.removeClass('btn-outline-secondary');
                    $this.addClass('btn-secondary')
                }
            },
            error: function(error) {
                $this.html('');
                $this.html('<i class="bi bi-cart-plus me-2"></i>Add to cart');
                if ($this.hasClass('btn-secondary')) {
                    $this.removeClass('btn-secondary');
                    $this.addClass('btn-outline-secondary')
                }
            }
        });
    } else {
        $this = $(this);
        $this.html('');
        $this.html('<i class="bi bi-cart-plus me-2"></i>Add to cart');
        if ($this.hasClass('btn-secondary')) {
            $this.removeClass('btn-secondary');
            $this.addClass('btn-outline-secondary')
        }
        $.ajax({
            url: "/api/cart/remove",
            type: "POST",
            contentType: "application/json", // Set the Content-Type header
            data: JSON.stringify(data),
            success: function() {
                $this.html('');
                $this.html('<i class="bi bi-cart-plus me-2"></i>Add to cart');
                if ($this.hasClass('btn-secondary')) {
                    $this.removeClass('btn-secondary');
                    $this.addClass('btn-outline-secondary')
                }
            },
            error: function() {
                $this.html('');
                $this.html('<i class="bi bi-check2 me-2"></i>Added to cart');
                if ($this.hasClass('btn-outline-secondary')) {
                    $this.removeClass('btn-outline-secondary');
                    $this.addClass('btn-secondary')
                }
            }
        });
    }
});

// Remove from cart
$('.remove-from-cart').on('click', function(e) {
    itemName = $(this).parents('.product-price-section').prev().find('.product-name').html();
    pid = $(this).attr('data-id');
    $this = $(this).parents('.cart-item')
    d = new Dialog('Remove from cart', 'Are you sure want to remove the <b>' + itemName + '</b> from the cart?');
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
                        updateOrderSummary()
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

// Update cart quantity
$('.btn-update-cart').on('click', function(e) {
    e.preventDefault();
    var $this = $(this);
    var data = [];

    $('.cart-item').each(function() {
        var productId = $(this).data('product-id');
        var quantity = $(this).find('.product-quantity').text();
        data.push({
            product_id: productId,
            qty: quantity
        });
    });

    var oldHtml = $this.html();
    var spinner = `<div class="spinner-border spinner-border-sm text-body me-2" role="status"></div>`
    $this.html(spinner + 'Updating...');
    $this.attr('disabled', true);
    $.ajax({
        url: "/api/cart/update",
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify(data),
        success: function() {
            location.reload();
        },
        error: function() {
            $this.html(oldHtml);
            $this.removeAttr('disabled')
        }
    });
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
    updateOrderSummary()
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
    updateOrderSummary()
});

// Add to wishlist
$('.btn-add-wishlist').on('click', function(e) {
    product_id = $(this).attr('data-id');
    var data = { "product_id": parseInt(product_id) };

    if ($(this).children().hasClass('bi-suit-heart')) {
        $this = $(this);
        $this.html('');
        $this.html('<i class="bi bi-suit-heart-fill me-2"></i>Added to wishlist');
        if ($this.hasClass('btn-outline-secondary')) {
            $this.removeClass('btn-outline-secondary');
            $this.addClass('btn-secondary')
        }
        $.ajax({
            url: "/api/wishlist/add",
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify(data),
            success: function() {
                $this.html('');
                $this.html('<i class="bi bi-suit-heart-fill me-2"></i>Added to wishlist');
                if ($this.hasClass('btn-outline-secondary')) {
                    $this.removeClass('btn-outline-secondary');
                    $this.addClass('btn-secondary')
                }
            },
            error: function(error) {
                $this.html('');
                $this.html('<i class="bi bi-suit-heart me-2"></i>Add to wishlist');
                if ($this.hasClass('btn-secondary')) {
                    $this.removeClass('btn-secondary');
                    $this.addClass('btn-outline-secondary')
                }
            }
        });
    } else {
        $this = $(this);
        $this.html('');
        $this.html('<i class="bi bi-suit-heart me-2"></i>Add to wishlist');
        if ($this.hasClass('btn-secondary')) {
            $this.removeClass('btn-secondary');
            $this.addClass('btn-outline-secondary')
        }
        $.ajax({
            url: "/api/wishlist/remove",
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify(data),
            success: function() {
                $this.html('');
                $this.html('<i class="bi bi-suit-heart me-2"></i>Add to wishlist');
                if ($this.hasClass('btn-secondary')) {
                    $this.removeClass('btn-secondary');
                    $this.addClass('btn-outline-secondary')
                }
            },
            error: function() {
                $this.html('');
                $this.html('<i class="bi bi-suit-heart-fill me-2"></i>Added to wishlist');
                if ($this.hasClass('btn-outline-secondary')) {
                    $this.removeClass('btn-outline-secondary');
                    $this.addClass('btn-secondary')
                }
            }
        });
    }

    console.log(product_id);

});

// Remove from wishlist
$('.remove-from-wishlist').on('click', function(e) {
    itemName = $(this).parents('.product-price-section').prev().find('.product-name').html();
    pid = $(this).attr('data-id');
    $this = $(this).parents('.cart-item')
    d = new Dialog('Remove from wishlist', 'Are you sure want to remove the <b>' + itemName + '</b> from your wishlist?');
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
                    url: "/api/wishlist/remove",
                    type: "POST",
                    contentType: "application/json",
                    data: JSON.stringify({ "product_id": parseInt(pid) }),
                    success: function() {
                        $this.remove();
                        location.reload();
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

// Update order summary details
function updateOrderSummary() {
    var prices = $('.total-item-price').map(function() {
        return parseFloat($(this).text());
    }).get();

    let sum = 0;

    for (let i = 0; i < prices.length; i++) {
        sum += prices[i];
    }

    shipping_cost = parseInt($('.cart-shipping-cost').text());
    $('.cart-subtotal').text(sum);
    $('.cart-total').text(sum + shipping_cost);
}

if (window.location.pathname == '/checkout') {
    $(document).ready(function() {
        // Function to check if all form fields are filled
        function checkForm() {
            var formFilled = true;

            // Check each input field in the form
            $('#checkout-form input').each(function() {
                if ($(this).val() === '') {
                    formFilled = false;
                    return false; // Exit the loop if any field is empty
                }
            });

            // Enable or disable the submit button based on the formFilled variable
            if (formFilled) {
                $('.btn-review-order').removeClass('disabled');
            } else {
                $('.btn-review-order').addClass('disabled');
            }
        }

        // Call the checkForm function whenever a form field changes
        $('#checkout-form input').on('input', checkForm);
    });
}

if (window.location.pathname === '/orders') {
    $('.btn-remove-order').on('click', function() {
        var $this = $(this);
        var oid = $this.data('id');
        console.log("Removing order " + oid);
        d = new Dialog('Cancel Order', 'Want to cancel order <b>#' + oid + '</b>?');
        d.setButtons([{
                'name': "Dismiss",
                "class": "btn-secondary",
                "onClick": function(event) {
                    $(event.data.modal).modal('hide');
                }
            },
            {
                'name': "Cancel order",
                "class": "btn-danger",
                "onClick": function(event) {
                    $.ajax({
                        url: "/api/order/remove",
                        type: "POST",
                        contentType: "application/json", // Set the Content-Type header
                        data: JSON.stringify({ "order_id": parseInt(oid) }),
                        success: function() {
                            $this.parent().parent().remove();
                            location.reload();
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
}