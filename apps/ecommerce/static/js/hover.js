function changeOrder(sort_by) {
    console.log("changing sort");
    $.ajax({
        url: `change-order/${sort_by}`,
        success: function(serverResponse) {
            console.log("here")
            $('.products').html(serverResponse);
            $('.product_price').hide();
            $('.card').hover(function() {
                $(this).children().children(".product_price").show()
            }, function() {
                $(this).children().children(".product_price").hide()
            });
        }
    });
}

$(document).ready(function() {
    // hide all product prices
    $('.product_price').hide();

    //hover on image animation shows price
    $('.card').hover(function() {
        $(this).children().children(".product_price").show()
    }, function() {
        $(this).children().children(".product_price").hide()
    });

    //change order on selection
    $('#sort').change(function() {
        changeOrder($('#sort').val());
    });
});