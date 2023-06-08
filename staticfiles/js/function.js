$("#commentForm").submit(function (e) {
    e.preventDefault();

    $.ajax({
        data: $(this).serialize(),

        method: $(this).attr("method"),

        url: $(this).attr("action"),

        dataType: "json",

        success: function (res) {
            console.log("Comment Saved to DB...")

            if (res.bool == true) {
                $("#review-resp").html("Review Added Successfully.")
                $(".hide-comment-form").hide()
            }
        }
    })
})

$(document).ready(function () {
    // Add to cart functionality
    $(".add-to-cart-btn").on("click", function () {

        let this_val = $(this);
        let index = this_val.attr("data-index");

        let quantity = $(".product-quantity-" + index).val();
        let product_title = $(".product-title-" + index).val();

        let product_id = $(".product-id-" + index).val();
        let product_price = $(".current-product-price-" + index).attr("data-price");

        let product_pid = $(".product-pid-" + index).val();
        let product_image = $(".product-image-" + index).val();

        console.log("Quantity: ", quantity);
        console.log("Title: ", product_title);
        console.log("Price: ", product_price);
        console.log("ID: ", product_id);
        console.log("PID: ", product_pid);
        console.log("Image: ", product_image);
        console.log("Index: ", index);
        console.log("Current Element: ", this_val);

        $.ajax({
            url: '/products/add-to-cart/',
            data: {
                'id': product_id,
                'image': product_image,
                'qty': quantity,
                'title': product_title,
                'price': product_price,
            },
            dataType: 'json',
            beforeSend: function () {
                console.log("Adding Product to Cart...");
            },
            success: function (res) {
                this_val.html("✔")
                console.log("Added Product to Cart!");
                $(".cart-items-count").text(res.totalcartitems)
            }
        })
    })

    $(".delete-product").on("click", function () {
        let product_id = $(this).attr("data-product")
        let this_val = $(this)

        console.log("Product ID:", product_id);

        $.ajax({
            url: "/products/delete-from-cart/",
            data: {
                "id": product_id
            },
            dataType: "json",
            beforeSend: function () {
                this_val.hide()
            },
            success: function (res) {
                this_val.show()
                $(".cart-items-count").text(res.totalcartitems)
                $("#cart-list").html(res.data)
            }
        })
    })

    $(".update-product").on("click", function () {
        let product_id = $(this).attr("data-product")
        let this_val = $(this)
        let product_quantity = $(".product-qty-" + product_id).val()

        console.log("Product ID:", product_id);

        $.ajax({
            url: "/products/update-cart/",
            data: {
                "id": product_id,
                "qty": product_quantity,
            },
            dataType: "json",
            beforeSend: function () {
                this_val.hide()
            },
            success: function (res) {
                this_val.show()
                $(".cart-items-count").text(res.totalcartitems)
                $("#cart-list").html(res.data)
            }
        })
    })

    $(document).on("submit", "#contact-form-ajax", function (e) {
        e.preventDefault()
        console.log("Submited...")

        let full_name = $("#full_name").val()
        let email = $("#email").val()
        let phone = $("#phone").val()
        let subject = $("#subject").val()
        let message = $("#message").val()

        console.log("Name:", full_name);
        console.log("Email:", email);
        console.log("Phone Number:", phone);
        console.log("Subject:", subject);
        console.log("Message:", message);

        $.ajax({
            url: '/contact/ajax-contact-form/',
            data: {
                'full_name': full_name,
                'email': email,
                'phone': phone,
                'subject': subject,
                'message': message,
            },
            dataType: 'json',
            beforeSend: function () {
                console.log("Sending Data to Server...");
            },
            success: function (res) {
                console.log("Sent Data to Server...");
                $("#contact-form-ajax").hide()
                $("#message-response").html(res.message)
            }
        })

    })
})


