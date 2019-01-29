function fetchTypes(category) {
    //retrieve all categories from database
    $.ajax({
        url: `add/types/${category}`,
        success: function(serverResponse) {
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

$(document).ready(function () {
    $('select').formSelect();
    
    // toggle between new or old options -- if chose old, disable new && vice versa

    $('#prod_category').change(function() {
        if ($(this).val() !== "")  {
            $('#prod_type').prop({
                "disabled": false
            });
    
            fetchTypes($(this).val());
    
            $('#new_category').prop({
                "disabled": true
            });
        }
        else {
            $('#prod_type').prop({
                "disabled": true
            });
            $('#new_category').prop({
                "disabled": false
            });
            $('#new_type').prop({
                "disabled": false
            });
        }
    
        $('select').formSelect();
    });
    
    $('#prod_type').change(function() {
        console.log($(this).val());
        if ($(this).val() !== "") {  //if selected type is valid
            $('#new_type').prop({
                "disabled": true
            });
        }
        else {
            $('#new_type').prop({
                "disabled": false
            });
        }
    
        $('select').formSelect();
    });
});

