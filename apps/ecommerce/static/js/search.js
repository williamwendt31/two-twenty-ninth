function updateSearch(query) {
    $.ajax({
        url: `/search/${query}`,
        success: function(serverResponse) {
            let output = "";
            for (let i = 0; i < serverResponse.length; i++) {
                output += "<li><a class='collapsible-header' href='/products/show/" + serverResponse[i].pk + "'>" + serverResponse[i].fields.name + "</a></li>";
            }

            $('#dropdown1').html(output);
        }
    });
}

$('#search-input').change(function() {
    if ($(this).val() !== "") {
        updateSearch($(this).val());
    }
});