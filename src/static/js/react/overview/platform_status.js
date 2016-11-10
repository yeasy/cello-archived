/**
 * Created by yuehaitao on 2016/11/1.
 */
import React from 'react'
import fetch from 'isomorphic-fetch'
import cookie from 'react-cookie'
import Urls from './constants/Urls'
var IoLoadD = require('react-icons/lib/io/load-d');
var echarts = require('echarts');

var theme = {
    color: [
        '#26B99A', '#34495E', '#BDC3C7', '#3498DB',
        '#9B59B6', '#8abb6f', '#759c6a', '#bfd3b7'
    ],

    title: {
        itemGap: 8,
        textStyle: {
            fontWeight: 'normal',
            color: '#408829'
        }
    },

    dataRange: {
        color: ['#1f610a', '#97b58d']
    },

    toolbox: {
        color: ['#408829', '#408829', '#408829', '#408829']
    },

    tooltip: {
        backgroundColor: 'rgba(0,0,0,0.5)',
        axisPointer: {
            type: 'line',
            lineStyle: {
                color: '#408829',
                type: 'dashed'
            },
            crossStyle: {
                color: '#408829'
            },
            shadowStyle: {
                color: 'rgba(200,200,200,0.3)'
            }
        }
    },

    dataZoom: {
        dataBackgroundColor: '#eee',
        fillerColor: 'rgba(64,136,41,0.2)',
        handleColor: '#408829'
    },
    grid: {
        borderWidth: 0
    },

    categoryAxis: {
        axisLine: {
            lineStyle: {
                color: '#408829'
            }
        },
        splitLine: {
            lineStyle: {
                color: ['#eee']
            }
        }
    },

    valueAxis: {
        axisLine: {
            lineStyle: {
                color: '#408829'
            }
        },
        splitArea: {
            show: true,
            areaStyle: {
                color: ['rgba(250,250,250,0.1)', 'rgba(200,200,200,0.1)']
            }
        },
        splitLine: {
            lineStyle: {
                color: ['#eee']
            }
        }
    },
    timeline: {
        lineStyle: {
            color: '#408829'
        },
        controlStyle: {
            normal: {color: '#408829'},
            emphasis: {color: '#408829'}
        }
    },

    k: {
        itemStyle: {
            normal: {
                color: '#68a54a',
                color0: '#a9cba2',
                lineStyle: {
                    width: 1,
                    color: '#408829',
                    color0: '#86b379'
                }
            }
        }
    },
    map: {
        itemStyle: {
            normal: {
                areaStyle: {
                    color: '#ddd'
                },
                label: {
                    textStyle: {
                        color: '#c12e34'
                    }
                }
            },
            emphasis: {
                areaStyle: {
                    color: '#99d2dd'
                },
                label: {
                    textStyle: {
                        color: '#c12e34'
                    }
                }
            }
        }
    },
    force: {
        itemStyle: {
            normal: {
                linkStyle: {
                    strokeColor: '#408829'
                }
            }
        }
    },
    chord: {
        padding: 4,
        itemStyle: {
            normal: {
                lineStyle: {
                    width: 1,
                    color: 'rgba(128, 128, 128, 0.5)'
                },
                chordStyle: {
                    lineStyle: {
                        width: 1,
                        color: 'rgba(128, 128, 128, 0.5)'
                    }
                }
            },
            emphasis: {
                lineStyle: {
                    width: 1,
                    color: 'rgba(128, 128, 128, 0.5)'
                },
                chordStyle: {
                    lineStyle: {
                        width: 1,
                        color: 'rgba(128, 128, 128, 0.5)'
                    }
                }
            }
        }
    },
    gauge: {
        startAngle: 225,
        endAngle: -45,
        axisLine: {
            show: true,
            lineStyle: {
                color: [[0.2, '#86b379'], [0.8, '#68a54a'], [1, '#408829']],
                width: 8
            }
        },
        axisTick: {
            splitNumber: 10,
            length: 12,
            lineStyle: {
                color: 'auto'
            }
        },
        axisLabel: {
            textStyle: {
                color: 'auto'
            }
        },
        splitLine: {
            length: 18,
            lineStyle: {
                color: 'auto'
            }
        },
        pointer: {
            length: '90%',
            color: 'auto'
        },
        title: {
            textStyle: {
                color: '#333'
            }
        },
        detail: {
            textStyle: {
                color: 'auto'
            }
        }
    },
    textStyle: {
        fontFamily: 'Arial, Verdana, sans-serif'
    }
};

var hostsTypeChart, hostsStatusChart;
var clustersTypeChart, clustersStatusChart;

var PlatformStatus = React.createClass({
    getInitialState: function () {
        return ({
            fetchingHostsStatus: false,
            fetchingClustersStatus: false
        })
    },
    setupHostsType: function () {
        hostsTypeChart = echarts.init(document.getElementById('hosts_type'), theme);

        hostsTypeChart.setOption({
            tooltip: {
                trigger: 'item',
                formatter: "{a} <br/>{b} : {c} ({d}%)"
            },
            legend: {
                x: 'center',
                y: 'bottom',
                data: ['single', 'swarm']
            },
            toolbox: {
                show: true,
                feature: {
                    magicType: {
                        show: true,
                        type: ['pie', 'funnel'],
                        option: {
                            funnel: {
                                x: '25%',
                                width: '50%',
                                funnelAlign: 'left',
                                max: 1548
                            }
                        }
                    }
                }
            },
            calculable: true,
            series: [{
                name: 'Host Type',
                type: 'pie',
                radius: '55%',
                center: ['50%', '48%'],
            }]
        });

        hostsStatusChart = echarts.init(document.getElementById('hosts_status'), theme);

        hostsStatusChart.setOption({
            tooltip: {
                trigger: 'item',
                formatter: "{a} <br/>{b} : {c} ({d}%)"
            },
            legend: {
                x: 'center',
                y: 'bottom',
                data: ['active', 'inactive']
            },
            toolbox: {
                show: true,
                feature: {
                    magicType: {
                        show: true,
                        type: ['pie', 'funnel'],
                        option: {
                            funnel: {
                                x: '25%',
                                width: '50%',
                                funnelAlign: 'left',
                                max: 1548
                            }
                        }
                    }
                }
            },
            calculable: true,
            series: [{
                name: 'Host Status',
                type: 'pie',
                radius: '55%',
                center: ['50%', '48%'],
            }]
        });
    },
    updateHostsChart: function (status) {
        hostsTypeChart.setOption({
            series: [{
                name: 'Host Type',
                type: 'pie',
                radius: '55%',
                center: ['50%', '48%'],
                data: status.type
            }]
        });
        hostsStatusChart.setOption({
            series: [{
                name: 'Host Status',
                type: 'pie',
                radius: '55%',
                center: ['50%', '48%'],
                data: status.status
            }]
        });
        this.setState({
            fetchingHostsStatus: false
        });
    },
    setupClustersType: function () {
        clustersTypeChart = echarts.init(document.getElementById('clusters_type'), theme);

        clustersTypeChart.setOption({
            tooltip: {
                trigger: 'item',
                formatter: "{a} <br/>{b} : {c} ({d}%)"
            },
            legend: {
                x: 'center',
                y: 'bottom',
                data: ['noops', 'pbft/batch']
            },
            toolbox: {
                show: true,
                feature: {
                    magicType: {
                        show: true,
                        type: ['pie', 'funnel'],
                        option: {
                            funnel: {
                                x: '25%',
                                width: '50%',
                                funnelAlign: 'left',
                                max: 1548
                            }
                        }
                    }
                }
            },
            calculable: true,
            series: [{
                name: 'Cluster Type',
                type: 'pie',
                radius: '55%',
                center: ['50%', '48%'],
            }]
        });

        clustersStatusChart = echarts.init(document.getElementById('clusters_status'), theme);

        clustersStatusChart.setOption({
            tooltip: {
                trigger: 'item',
                formatter: "{a} <br/>{b} : {c} ({d}%)"
            },
            legend: {
                x: 'center',
                y: 'bottom',
                data: ['free', 'used']
            },
            toolbox: {
                show: true,
                feature: {
                    magicType: {
                        show: true,
                        type: ['pie', 'funnel'],
                        option: {
                            funnel: {
                                x: '25%',
                                width: '50%',
                                funnelAlign: 'left',
                                max: 1548
                            }
                        }
                    }
                }
            },
            calculable: true,
            series: [{
                name: 'Cluster Status',
                type: 'pie',
                radius: '55%',
                center: ['50%', '48%'],
            }]
        });
    },
    updateClustersChart: function (status) {
        clustersTypeChart.setOption({
            series: [{
                name: 'Cluster Type',
                type: 'pie',
                radius: '55%',
                center: ['50%', '48%'],
                data: status.type
            }]
        });
        clustersStatusChart.setOption({
            series: [{
                name: 'Cluster Status',
                type: 'pie',
                radius: '55%',
                center: ['50%', '48%'],
                data: status.status
            }]
        });
        this.setState({
            fetchingClustersStatus: false
        });
    },
    fetchStatus: function (res) {
        var _that = this;
        switch (res) {
            case 'host':
                this.setState({
                    fetchingHostsStatus: true
                });
                break;
            case 'cluster':
                this.setState({
                    fetchingClustersStatus: true
                });
                break;
            default:
                break;
        }
        fetch(Urls.StatusUrl + "?res=" + res, {
            method: "get",
            credentials: 'include',
            headers: {
                "X-CSRFToken": cookie.load("csrftoken")
            }
        }).then(response => {
            if (response.ok) {
                response.json()
                    .then(json => {
                        switch (res) {
                            case 'host':
                                _that.updateHostsChart(json);
                                break;
                            case 'cluster':
                                _that.updateClustersChart(json);
                                break;
                            default:
                                break;
                        }
                    });
            }
        });
    },
    componentDidMount: function () {
        this.setupHostsType();
        this.setupClustersType();
        this.fetchStatus('host');
        this.fetchStatus('cluster');
    },
    render: function () {
        return (
                <div className="row">
                    <div className="col-md-3 col-sm-3 col-xs-12">
                        <div className="x_panel">
                            <div className="x_title">
                                <h2>Host Type {this.state.fetchingHostsStatus && <IoLoadD className="spin"/>}</h2>
                                <div className="clearfix"></div>
                            </div>
                            <div className="x_content">

                                <div id="hosts_type" style={{height: 200, width: "100%"}}></div>

                            </div>
                        </div>
                    </div>
                    <div className="col-md-3 col-sm-3 col-xs-12">
                        <div className="x_panel">
                            <div className="x_title">
                                <h2>Host Status {this.state.fetchingHostsStatus && <IoLoadD className="spin"/>}</h2>
                                <div className="clearfix"></div>
                            </div>
                            <div className="x_content">

                                <div id="hosts_status" style={{height: 200, width: "100%"}}></div>

                            </div>
                        </div>
                    </div>
                    <div className="col-md-3 col-sm-3 col-xs-12">
                        <div className="x_panel">
                            <div className="x_title">
                                <h2>Cluster Type {this.state.fetchingClustersStatus && <IoLoadD className="spin"/>}</h2>
                                <div className="clearfix"></div>
                            </div>
                            <div className="x_content">

                                <div id="clusters_type" style={{height: 200, width: "100%"}}></div>

                            </div>
                        </div>
                    </div>
                    <div className="col-md-3 col-sm-3 col-xs-12">
                        <div className="x_panel">
                            <div className="x_title">
                                <h2>Cluster Status {this.state.fetchingClustersStatus && <IoLoadD className="spin"/>}</h2>
                                <div className="clearfix"></div>
                            </div>
                            <div className="x_content">

                                <div id="clusters_status" style={{height: 200, width: "100%"}}></div>

                            </div>
                        </div>
                    </div>
                </div>
        )
    }
});

export default PlatformStatus;
