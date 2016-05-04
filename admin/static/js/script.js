$(document).ready(function() {
    $('.create_host_button').click(function() {
        //var name = $(this).parents('form:first').find('[name="name"]').val();
        //var daemon_url = $(this).parents('form:first').find('[name="daemon_url"]').val();
        var form_data = $('#add_new_host_form').serialize();
        
        $.ajax({
            url: "/host",
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
    $('.delete_host_button').click(function() {
        // Confirm
        var id_data = $(this).attr('id_data');

        $.ajax({
            url: "/host",
            type: 'DELETE',
            dataType: 'json',
            data:{
                "id": id_data,
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
    $('.create_cluster_button').click(function() {
        //var name = $(this).parents('form:first').find('[name="name"]').val();
        //var daemon_url = $(this).parents('form:first').find('[name="daemon_url"]').val();
        var form_data = $('#add_new_cluster_form').serialize();
        
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
        var id_data = $(this).attr('id_data');
        var col_name = $(this).attr('col_name');

        $.ajax({
            url: "/cluster",
            type: 'DELETE',
            dataType: 'json',
            data:{
                "id": id_data,
                "col_name": col_name
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
