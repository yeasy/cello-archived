$(document).ready(function() {
    function alertMsg(title, message, type) {
        $.notify({
            title: '<strong>'+title+'</strong>',
            message: message
        },{
            type: type,
            delay: 2000,
            placement: {
                align: 'center'       
            }
        });  
    }
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
                alertMsg('Success!', 'New host is created.', 'success');
                setTimeout("location.reload(true);",2000);
            },
            error: function(error) {
                console.log(error);
                alertMsg('Failed!', error.responseJSON.error, 'danger');
                setTimeout(location.reload, 2000);
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
                alertMsg('Success!', 'The host is deleted.', 'success');
                setTimeout("location.reload(true);",2000);
            },
            error: function(error) {
                console.log(error);
                alertMsg('Failed!', error.responseJSON.error, 'danger');
                setTimeout(location.reload, 2000);
            }
        });
    });
    $('#delete_host_confirm').on('click', '.btn-ok', function(e) {
        var $modalDiv = $(e.delegateTarget);
        var id = $(this).data('hostId');
        $.ajax({
            url: "/host",
            type: 'DELETE',
            dataType: 'json',
            data:{
                "id": id
            },
            success: function(response) {
                console.log(response);
                alertMsg('Success!', 'The host is deleted.', 'success');
                setTimeout("location.reload(true);",2000);
            },
            error: function(error) {
                console.log(error);
                alertMsg('Failed!', error.responseJSON.error, 'danger');
                setTimeout("location.reload(true);",2000);
            }
        });
        $modalDiv.modal('hide');
    });
    $('#delete_host_confirm').on('show.bs.modal', function(e) {
        var data = $(e.relatedTarget).data();
        $('#title', this).text(data.title);
        $('.btn-ok', this).data('hostId', data.id);
    });
    $('#save_host_button').click(function(e) {
            // Save the form data via an Ajax request
            e.preventDefault();
            var $form = $('#config_host_form');

            var id    = $form.find('[name="id"]').val();
            var name    = $form.find('[name="name"]').val();
            var status    = $form.find('[name="status"]').val();
            var capacity    = $form.find('[name="capacity"]').val();
            var type    = $form.find('[name="type"]').val();

            // The url and method might be different in your application
            $.ajax({
                url: '/host',
                method: 'PUT',
                data: {
                    "id": id,
                    "name": name,
                    "status": status,
                    "capacity": capacity,
                    "type": type
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

                //bootbox.alert('The Host config is updated');
                alertMsg('Success!', 'The host info is updated.', 'success');
                setTimeout("location.reload(true);",2000);
            }).error(function(response) {
                // Hide the dialog
                $form.parents('.bootbox').modal('hide');
                alertMsg('Failed!', error.responseJSON.error, 'danger');
                setTimeout(location.reload, 2000);
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
                .find('[name="type"]').val(response.type).end()
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
    $('#fillup_host_button').click(function() {
        // Confirm
        var id = $(this).attr('data-id');

        $.ajax({
            url: "/host_action",
            type: 'POST',
            dataType: 'json',
            data:{
                "id": id,
                "action": "fillup"
            },
            success: function(response) {
                console.log(response);
                setTimeout(function () {
                    alertMsg('Success!', 'The host is fullfilled now.', 'success');
                }, 1000);
                
                setTimeout("location.reload(true);",2000);
            },
            error: function(error) {
                console.log(error);
                alertMsg('Failed!', error.responseJSON.error, 'danger');
                setTimeout(location.reload, 2000);
            }
        });
    });
    $('#clean_host_button').click(function() {
        // Confirm
        var id = $(this).attr('data-id');

        $.ajax({
            url: "/host_action",
            type: 'POST',
            dataType: 'json',
            data:{
                "id": id,
                "action": "clean"
            },
            success: function(response) {
                console.log(response);
                alertMsg('Success!', 'The host is clean now.', 'success');
                setTimeout("location.reload(true);",2000);
            },
            error: function(error) {
                console.log(error);
                alertMsg('Failed!', error.responseJSON.error, 'danger');
                setTimeout("location.reload(true);",2000);
            }
        });
    });
    
    $('#reset_host_confirm').on('click', '.btn-ok', function(e) {
        var $modalDiv = $(e.delegateTarget);
        var id = $(this).data('hostId');
        // $.ajax({url: '/api/record/' + id, type: 'DELETE'})
        // $.post('/api/record/' + id).then()
        $.ajax({
            url: "/host_action",
            type: 'POST',
            dataType: 'json',
            data:{
                "id": id,
                "action": "reset"
            },
            success: function(response) {
                console.log(response);
                alertMsg('Success!', 'The host is reset now.', 'success');
                setTimeout("location.reload(true);",2000);
            },
            error: function(error) {
                console.log(error);
                alertMsg('Failed!', error.responseJSON.error, 'danger');
                setTimeout("location.reload(true);",2000);
            }
        });
        $modalDiv.modal('hide');
    });
    $('#reset_host_confirm').on('show.bs.modal', function(e) {
        var data = $(e.relatedTarget).data();
        $('#title', this).text(data.title);
        $('.btn-ok', this).data('hostId', data.id);
    });
    $('.create_cluster_button').click(function() {
        var form_data = $('#add_new_cluster_form').serialize();
        
        $.ajax({
            url: "/cluster",
            type: 'POST',
            dataType: 'json',
            data: form_data,
            success: function(response) {
                console.log(response);
                alertMsg('Success!', 'New cluster is created.', 'success');
                setTimeout("location.reload(true);",2000);
                //location.reload();
            },
            error: function(error) {
                console.log(error);
                alertMsg('Failed!', error.responseJSON.error, 'danger');
                setTimeout("location.reload(true);",2000);
                //location.reload();
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
                alertMsg('Success!', 'The cluster is deleted.', 'success');
                setTimeout("location.reload(true);",2000);
            },
            error: function(error) {
                console.log(error);
                alertMsg('Failed!', error.responseJSON.error, 'danger');
                setTimeout("location.reload(true);",2000);
            }
        });
    });
    //not used yet
    $('.release_cluster_button').click(function() {
        var id_data = $(this).attr('id_data');

        $.ajax({
            url: "/cluster",
            type: 'POST',
            dataType: 'json',
            data: {
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

    
    Highcharts.setOptions({
        global : {
            useUTC : false
        }
    });

    // Create the chart
    $('#container_test').highcharts({
        chart: {
            type: 'bar'
        },
        title: {
            text: 'Fruit Consumption'
        },
        xAxis: {
            categories: ['Apples', 'Bananas', 'Oranges']
        },
        yAxis: {
            title: {
                text: 'Fruit eaten'
            }
        },
        series: [{
            name: 'Jane',
            data: [1, 0, 4]
        }, {
            name: 'John',
            data: [5, 7, 3]
        }]
    });
    
    var gaugeOptions = {

        chart: {
            type: 'solidgauge'
        },

        title: null,

        pane: {
            center: ['50%', '85%'],
            size: '140%',
            startAngle: -90,
            endAngle: 90,
            background: {
                backgroundColor: (Highcharts.theme && Highcharts.theme.background2) || '#EEE',
                innerRadius: '60%',
                outerRadius: '100%',
                shape: 'arc'
            }
        },

        tooltip: {
            enabled: false
        },

        // the value axis
        yAxis: {
            stops: [
                [0.1, '#55BF3B'], // green
                [0.5, '#DDDF0D'], // yellow
                [0.9, '#DF5353'] // red
            ],
            lineWidth: 0,
            minorTickInterval: null,
            tickPixelInterval: 400,
            tickWidth: 0,
            title: {
                y: -70
            },
            labels: {
                y: 16
            }
        },

        plotOptions: {
            solidgauge: {
                dataLabels: {
                    y: 5,
                    borderWidth: 0,
                    useHTML: true
                }
            }
        }
    };

    // The speed gauge
    $('#container_host_utilization').highcharts(Highcharts.merge(gaugeOptions, {
        yAxis: {
            min: 0,
            max: 200,
            title: {
                text: 'Utilization'
            }
        },

        credits: {
            enabled: false
        },

        series: [{
            name: 'Utilization',
            data: [80],
            dataLabels: {
                format: '<div style="text-align:center"><span style="font-size:25px;color:' +
                    ((Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black') + '">{y}</span><br/>' +
                       '<span style="font-size:12px;color:silver">km/h</span></div>'
            },
            tooltip: {
                valueSuffix: ''
            }
        }]

    }));

    // The RPM gauge
    $('#container-rpm').highcharts(Highcharts.merge(gaugeOptions, {
        yAxis: {
            min: 0,
            max: 5,
            title: {
                text: 'RPM'
            }
        },

        series: [{
            name: 'RPM',
            data: [1],
            dataLabels: {
                format: '<div style="text-align:center"><span style="font-size:25px;color:' +
                    ((Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black') + '">{y:.1f}</span><br/>' +
                       '<span style="font-size:12px;color:silver">* 1000 / min</span></div>'
            },
            tooltip: {
                valueSuffix: ' revolutions/min'
            }
        }]

    }));

    
    function request_hosts() {
        $.ajax({
            url: '/_stat?res=hosts',
            type: 'GET',
            dataType: 'json',
            success: function(response) {
                // add the point
                chart_hosts_type.series[0].setData(response.type);
                chart_hosts_status.series[0].setData(response.status);

                // call it again after one second
                setTimeout(request_hosts, 30000);    
            },
            cache: false
        });
    }
    var chart_hosts_type = new Highcharts.Chart({
            chart: {
                renderTo: 'stat_hosts_type',
                defaultSeriesType: 'spline',
                plotBackgroundColor: null,
                plotBorderWidth: null,
                plotShadow: false,
                type: 'pie',
                events: {
                    load: request_hosts
                }
            },
            title: {
                text: 'Host Type'
            },
            tooltip: {
                pointFormat: '<b>{point.y}</b>'
            },
            plotOptions: {
                pie: {
                    allowPointSelect: true,
                    cursor: 'pointer',
                    dataLabels: {
                        enabled: false
                    },
                    showInLegend: true
                }
            },
            legend: {
                labelFormatter: function() {
                    return this.name + ': ' + this.y;
                },
            },
            series: [{
                name: 'Number',
                colorByPoint: true,
                data: [{
                    name: '',
                    y: 100
                }]
            }]
    });
    var chart_hosts_status = new Highcharts.Chart({
            chart: {
                renderTo: 'stat_hosts_status',
                defaultSeriesType: 'spline',
                plotBackgroundColor: null,
                plotBorderWidth: null,
                plotShadow: false,
                type: 'pie',
                events: {
                    load: request_hosts
                }
            },
            title: {
                text: 'Host Status'
            },
            tooltip: {
                pointFormat: '<b>{point.y}</b>'
            },
            plotOptions: {
                pie: {
                    allowPointSelect: true,
                    cursor: 'pointer',
                    dataLabels: {
                        enabled: false
                    },
                    showInLegend: true
                }
            },
            legend: {
                labelFormatter: function() {
                    return this.name + ': ' + this.y;
                },
            },
            series: [{
                name: 'Number',
                colorByPoint: true,
                data: [{
                    name: '',
                    y: 100
                }]
            }]
        });
    function request_clusters() {
        $.ajax({
            url: '/_stat?res=clusters',
            type: 'GET',
            dataType: 'json',
            success: function(response) {
                // add the point
                chart_clusters_type.series[0].setData(response.type);
                chart_clusters_status.series[0].setData(response.status);

                // call it again after one second
                setTimeout(request_clusters, 30000);    
            },
            cache: false
        });
    }
    var chart_clusters_type = new Highcharts.Chart({
            chart: {
                renderTo: 'stat_clusters_type',
                defaultSeriesType: 'spline',
                plotBackgroundColor: null,
                plotBorderWidth: null,
                plotShadow: false,
                type: 'pie',
                events: {
                    load: request_clusters
                }
            },
            title: {
                text: 'Cluster Type'
            },
            tooltip: {
                pointFormat: '<b>{point.y}</b>'
            },
            plotOptions: {
                pie: {
                    allowPointSelect: true,
                    cursor: 'pointer',
                    dataLabels: {
                        enabled: false
                    },
                    showInLegend: true
                }
            },
            legend: {
                labelFormatter: function() {
                    return this.name + ': ' + this.y;
                },
            },
            series: [{
                name: 'Number',
                colorByPoint: true,
                data: [{
                    name: '',
                    y: 100
                }]
            }]
    });
    var chart_clusters_status = new Highcharts.Chart({
            chart: {
                renderTo: 'stat_clusters_status',
                defaultSeriesType: 'spline',
                plotBackgroundColor: null,
                plotBorderWidth: null,
                plotShadow: false,
                type: 'pie',
                events: {
                    load: request_clusters
                }
            },
            title: {
                text: 'Cluster Status'
            },
            tooltip: {
                pointFormat: '<b>{point.y}</b>'
            },
            plotOptions: {
                pie: {
                    allowPointSelect: true,
                    cursor: 'pointer',
                    dataLabels: {
                        enabled: false
                    },
                    showInLegend: true
                }
            },
            legend: {
                labelFormatter: function() {
                    return this.name + ': ' + this.y;
                },
            },
            series: [{
                name: 'Number',
                colorByPoint: true,
                data: [{
                    name: '',
                    y: 100
                }]
            }]
        });
});
