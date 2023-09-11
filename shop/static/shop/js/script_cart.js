$(document).ready(function() {
    var selected = {
        id: 0,
        name: '',
        brand: '',
        price: 0.0,
        unit_label: '',
        qty: 0,
        available: false
    };
    var cart = {};      // {"<id>": [<cart-position>, <input-quantity>, <product-price>]}
    var count = 0;      // Number of cart-items

    /* Initial treatments */
    $('#product_details').hide();   // Hide product-details initially
    updateFooter();                 // Update footer initially
    $('#input_id').focus()          // Get focus on input-id

    /* ID typing event */
    $('#input_id').on(
        'input', function() {
            // Hide product-details and show product-list
            $('#product_details').hide();
            $('#product_list').show();
            // Capture typed text
            let typed = $(this).val();
            if(typed == '') {
                // Show all products
                $("#product_list button").show();
            } else {
                // Only show the matched products
                $('#product_list button[data-id="' + typed + '"]').show();
                $('#product_list button[data-id!="' + typed + '"]').hide();
            }
        }
    );
    $('#input_id').on(
        'focus', function() {
            // Hide product-details and show product-list
            $('#product_details').hide();
            $('#product_list').show();
            // Capture typed text
            let typed = $(this).val();
            if(typed == '') {
                // Show all products
                $("#product_list button").show();
            } else {
                // Only show the matched products
                $('#product_list button[data-id="' + typed + '"]').show();
                $('#product_list button[data-id!="' + typed + '"]').hide();
            }
        }
    );
    $('#input_id').keydown(
        'change', function(event) {
            // Capture enter key to select-product
            const keyCode = (event.keyCode ? event.keyCode : event.which);   
            if (keyCode == 13) {
                let typed = $(this).val();
                if(typed != '') {
                    $('#product_list button[data-id="' + parseInt(typed) + '"]').trigger('click');
                }
            }
        }
    );

    /* Quantity typing event */
    $('#input_quantity').keydown(
        'change', function(event) {
            // Capture enter key to add-to-cart
            const keyCode = (event.keyCode ? event.keyCode : event.which);   
            if (keyCode == 13) {
                let typed = parseInt($(this).val());
                if(typed != NaN && typed > 0) {
                    $('#btn_add_product').trigger('click');
                }
            }
        }
    );

    /* Product selection event */
    $('#product_list button').click(function() {
        // Clear submitted id
        $('#input_id').val('');
        // Hide product-list and show product-details
        $('#product_list').hide();
        $('#product_details').show();

        // Retrieve values of this product
        selected.id = parseInt($(this).attr('data-id'))
        selected.name = $(this).text();
        selected.brand = $(this).attr('data-brand');
        selected.price = parseFloat($(this).attr('data-price'));
        selected.unit_label = $(this).attr('data-unit-label');
        selected.qty = parseInt($(this).attr('data-quantity'));
        let available = $(this).attr('data-available') != 'False' && selected.qty > 0;
        selected.available = available;
        
        // Updating description values
        $('#product_name').text(selected.name);
        $('#product_price').text(selected.price);
        $('#product_brand').text(selected.brand);
        $('#product_available').text(selected.available ? 'Yes' : 'No');
        $('#product_quantity').text(selected.qty + ' ' + selected.unit_label);
        $('#product_unit_label').text(selected.unit_label);
        if (available) {
            // Product available, hence show quantity-area & add-cart button
            $('#selection_box #quantity_area').show();
            $('#btn_add_product').show();
            $('#btn_unavailable_product').hide();
            // Updating quantity-area
            $('#input_quantity').attr('max', selected.qty);
            // Focus on input-quantity
            $('#input_quantity').val('');
            $('#input_quantity').focus();
        } else {
            // Not available, hence hide quantity-area & add-cart button
            $('#selection_box #quantity_area').hide()
            $('#btn_unavailable_product').show();
            $('#btn_add_product').hide();
        }
    });

    /* Action button click events */
    $('#btn_reset').click(function() {
        // Reload page
        location.reload();
    });
    $('#btn_cancel_product').click(function() {
        // Focus on input-id box again
        $('#input_id').focus();
    });
    $('#btn_checkout').click(function() {
        // Packing up data
        let today = new Date();
        let date = today.getFullYear() + '-' + String(today.getMonth()+1).padStart(2, '0') + '-' + String(today.getDate()).padStart(2, '0');
        let time = String(today.getHours()).padStart(2, '0') + '-' + String(today.getMinutes()).padStart(2, '0');
        let packed = {
            'date': date,
            'time': time,
            'cart': JSON.stringify(cart)
        };
        // Send request
        $.post(
            '/shop/checkout/',
            packed,
            function(data, status) {
                if (status == 'success') {
                    // Post successful
                    console.log(data['checkout']);
                    if (data['checkout']) {
                        console.log(data['url']);
                        location.replace(data['url'])
                    } else {
                        $('#toast_checkout_error_content').text(data['message']);
                        $('#toast_checkout_error').toast('show');
                    }
                } else {
                    // Post unsuccessful
                    $('#toast_checkout_error_content').text('Checkout failed due to unknown network error.');
                    $('#toast_checkout_error').toast('show');
                }

                console.log('checkout=' + data['checkout'] + ' url=' + data['url'] + ' message=' + data['message'] + ' Status=' + status);
            }
        );
    });
    $('#btn_add_product').click(function() {
        // Getting & checking input-quantity
        let qty_input = parseInt($('#input_quantity').val());
        if(qty_input > selected.qty) {
            // Toast: input quantity exceeded
            $('#toast_qty_exceed').toast('show');
        } else {
            selected.qty -= qty_input;
            if (cart[selected.id]) {
                // Product already in cart, hence update qty in cart
                cart[selected.id][1] += qty_input;
                qty_input = cart[selected.id][1];

                console.log('Id=' + selected.id + ' qty_remaining=' + selected.qty + ' qty_selected=' + qty_input);

                // Updating in product-list
                $('#product_list button[data-id="' + selected.id + '"]').attr('data-quantity', selected.qty);
                // Updating in cart-list
                let td = '<th scope="col">' + cart[selected.id][0] + '</th><td>' + selected.name + '</td><td>' + selected.brand + '</td><td>' + qty_input + '</td><td>' + selected.price + '</td><td>' + (selected.price*qty_input) + '</td>';
                $('#cart_list tr[data-id="' + selected.id + '"]').html(td);
            } else {
                // New product to add into cart
                ++count;
                cart[selected.id] = [count, qty_input, selected.price];
                // Updating in product-list
                $('#product_list button[data-id="' + selected.id + '"]').attr('data-quantity', selected.qty);
                // Adding in cart-list
                let tr = '<tr data-id="' + selected.id + '"><th scope="col">' + count + '</th><td>' + selected.name + '</td><td>' + selected.brand + '</td><td>' + qty_input + '</td><td>' + selected.price + '</td><td>' + (selected.price*qty_input) + '</td></tr>';
                $('#cart_list').append(tr);
            }
            // Finally update footer & focus on input-id box
            updateFooter();
            $('#input_id').focus();
        }
    });

    /* Updates total price, counts etc. in footer section */
    function updateFooter() {
        let total_price = 0.0;
        let total_qty = 0;
        for(const item in cart) {
            total_price += (cart[item][1] * cart[item][2]); // Product price
            total_qty += cart[item][1]; // Product Quantity
        }
        $('#total_price').text(total_price);
        $('#product_count').text(count);
        $('#total_quantity').text(total_qty);
        $('#btn_checkout').attr('disabled', (count == 0));
    }

});