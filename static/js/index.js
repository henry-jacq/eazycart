$('.btn-add-cart').on('click', function(e) {
    quantity = $(this).prev().val();
    product_id = $(this).attr('data-id');

    var data = {
        "product_id": parseInt(product_id),
        "product_qty": parseInt(quantity)
    };

    console.log(data);

    if ($(this).children().hasClass('bi-cart-plus')) {
        $(this).html('');
        $(this).html('<i class="bi bi-check2 me-2"></i>Added to cart');
        if ($(this).hasClass('btn-outline-secondary')) {
            $(this).removeClass('btn-outline-secondary');
            $(this).addClass('btn-secondary')
        }
        $(this).prev().attr('readonly', 'true');
        $.ajax({
            url: "/api/cart/add",
            type: "POST",
            contentType: "application/json", // Set the Content-Type header
            data: JSON.stringify(data),
            success: function(response) {
                console.log(response);
            },
            error: function(error) {
                console.log(error);
            }
        });
    } else {
        $(this).html('');
        $(this).html('<i class="bi bi-cart-plus me-2"></i>Add to cart');
        if ($(this).hasClass('btn-secondary')) {
            $(this).removeClass('btn-secondary');
            $(this).addClass('btn-outline-secondary')
        }
        $(this).prev().removeAttr('readonly')
        $.ajax({
            url: "/api/cart/remove",
            type: "POST",
            contentType: "application/json", // Set the Content-Type header
            data: JSON.stringify(data),
            success: function(response) {
                console.log(response);
            },
            error: function(error) {
                console.log(error);
            }
        });
    }
});