function fetchTypes(category) {
    $.ajax({
        url: `add/types/${category}`,
        success: function(serverResponse) {
            console.log(serverResponse)
            if (serverResponse != "") {
                let output = "<option value=''>Choose a Type</option>"
                for (let i = 0; i < serverResponse.length; i++) {
                    output += "<option value='" + serverResponse[i].fields.name + "'>" + serverResponse[i].fields.name + "</option>";
                }
                $('#prod_type').html(output);
            }
            else {
                $('#prod_type').prop({
                    "disabled": true
                });
            }
            $('#prod_type').formSelect();
        }
    });
}
$('select').formSelect();

$('#prod_category').change(function() {
    if ($(this).val() !== "")  {
        $('#prod_type').prop({
            "disabled": false
        });
        fetchTypes($(this).val());
        $('select').formSelect();
        $('#new_category').prop({
            "disabled": true
        });
    }
    else {
        $('#prod_type').prop({
            "disabled": true
        });
        $('select').formSelect();
        $('#new_category').prop({
            "disabled": false
        });
    }
});

$('#prod_type').change(function() {
    if ($(this).val() !== "") {
        $('#new_type').prop({
            "disabled": true
        });
    }
    else {
        $('#new_typed').prop({
            "disabled": false
        });
    }
});

