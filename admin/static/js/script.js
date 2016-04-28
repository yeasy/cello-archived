$(document).ready(function() {
    $('.create_cluster_button').click(function() {
        //var name = $(this).parents('form:first').find('[name="name"]').val();
        //var daemon_url = $(this).parents('form:first').find('[name="daemon_url"]').val();
        var form_data = $(this).parents('form:first').serialize();
        
        $.ajax({
            url: "/cluster",
            type: 'POST',
            dataType: 'json',
            data: form_data,
            success: function(response) {
                console.log(response);
                location.reload(); 
            },
            error: function(error) {
                console.log(error);
                location.reload(); 
            }
        });
    });
    $('.delete_cluster_button').click(function() {
        // Confirm
        var id_data = $(this).attr('data-id');

        $.ajax({
            url: "/cluster",
            type: 'DELETE',
            dataType: 'json',
            data:{
                "id": id_data
            },
            success: function(response) {
                console.log(response);
                location.reload(); 
            },
            error: function(error) {
                console.log(error);
                location.reload(); 
            }
        });
    });
});
