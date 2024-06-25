$('#add-to-cart-form').on('click', function(event){
    
    event.preventDefault();
    var product_id = $('#add-to-cart-form').val();
    $.ajax({
        url: "add/"+product_id,
        type: 'POST',
        data: {
            'csrfmiddlewaretoken': '{{ csrf_token }}'
        },
        success: function(response){
            if(response.success) {
                alert(response.message);
            } else {
                alert('Failed to add product to cart.');
            }
        }
    });
});
;