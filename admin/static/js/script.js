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
        var id = $(this).attr('data-id');

        $.ajax({
            url: "/host",
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
    $('#save_host_button').click(function(e) {
            // Save the form data via an Ajax request
            e.preventDefault();
            var $form = $('#config_host_form');

            var id    = $form.find('[name="id"]').val();
            var name    = $form.find('[name="name"]').val();
            var status    = $form.find('[name="status"]').val();
            var capacity    = $form.find('[name="capacity"]').val();

            // The url and method might be different in your application
            $.ajax({
                url: '/host',
                method: 'PUT',
                data: {
                    "id": id,
                    "name": name,
                    "status": status,
                    "capacity": capacity
                }
            }).success(function(response) {
                // Get the cells
                var $button = $('button[data-id="' + response.id + '"]'),
                    $tr     = $button.closest('tr'),
                    $cells  = $tr.find('td');

                // Update the cell data
                $cells
                    .eq(1).html(response.name).end()
                    .eq(3).html(response.capacity).end();

                // Hide the dialog
                $form.parents('.bootbox').modal('hide');

                // You can inform the user that the data is updated successfully
                // by highlighting the row or showing a message box
                bootbox.alert('The Host config is updated');
                location.reload();
            }).error(function(response) {
                // Hide the dialog
                $form.parents('.bootbox').modal('hide');

                // You can inform the user that the data is updated successfully
                // by highlighting the row or showing a message box
                bootbox.alert('The Host config is not saved!');
                location.reload(); 
            });
        });

    $('.edit_host_button').on('click', function() {
        // Get the record's ID via attribute
        var id = $(this).attr('data-id');
        $.ajax({
            url: '/host',
            method: 'GET',
            dataType: 'json',
            data:{
                "id": id
            }
        }).success(function(response) {
            // Populate the form fields with the data returned from server
            $('#config_host_form')
                .find('[name="id"]').val(response.id).end()
                .find('[name="name"]').val(response.name).end()
                .find('[name="daemon_url"]').val(response.daemon_url).end()
                .find('[name="capacity"]').val(response.capacity).end()
                .find('[name="status"]').val(response.status).end()
                .find('[name="create_ts"]').val(response.create_ts).end()
                .find('[name="clusters"]').val(response.clusters.length).end();

            // Show the dialog
            bootbox
                .dialog({
                    title: 'Edit the Host Config',
                    message: $('#config_host_form'),
                    show: false // We will show it manually later
                })
                .on('shown.bs.modal', function() {
                    $('#config_host_form')
                        .show();
                })
                .on('hide.bs.modal', function(e) {
                    // Bootbox will remove the modal (including the body which contains the login form)
                    // after hiding the modal
                    // Therefor, we need to backup the form
                    $('#config_host_form').hide().appendTo('body');
                })
                .modal('show');
        });
    });
});
