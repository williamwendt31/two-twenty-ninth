$(document).ready(function () {
    // toggle disabling billing info form if shipping and billing are same
    $('#same').change(function() {
        if ( $(this).is(":checked") ) {
            $('#billing_info').prop({
                "disabled": true
            });
        }
        else {
            $('#billing_info').prop({
                "disabled": false
            });
        }
    });
    $('#s_state').formSelect();
    $('#b_state').formSelect();
});
