$(function() {
    $('#create_cluster_button').click(function() {
        var name = $('#cluster_name').val();
        var daemon_url = $('#cluster_daemon_url').val();
        $.ajax({
            url: "/cluster",
            type: 'POST',
            dataType: 'json',
            data:{
                "name": name,
                "daemon_url": daemon_url,
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
    $('.delete_cluster_button').click(function() {
        // Confirm
        var id = $(this).attr('data-id');

        $.ajax({
            url: "/cluster",
            type: 'DELETE',
            dataType: 'json',
            data:{
                "id": id
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