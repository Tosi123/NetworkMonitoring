# -*- coding: utf-8 -*-

FOLDER_JSON = """{
    "schemaVersion": 16,
    "title": "title",
    "uid": "uid",
    "version": 1
}"""

BOARD_SKEL = """{
    "annotations": {
        "list": [
            {
                "builtIn": 1,
                "datasource": "-- Grafana --",
                "enable": true,
                "hide": true,
                "iconColor": "rgba(0, 211, 255, 1)",
                "name": "Annotations \u0026 Alerts",
                "type": "dashboard"
            }
        ]
    },
    "editable": true,
    "gnetId": null,
    "graphTooltip": 0,
    "hideControls": false,
    "id": null,
    "links": [
    ],
    "panels": [
      
      
      
    ],
    "schemaVersion": 16,
    "style": "dark",
    "tags": [
    ],
    "templating": {
        "list": [
        ]
    },
    "time": {
        "from": "now-6h",
        "to": "now"
    },
    "timepicker": {
        "refresh_intervals": [
            "5s",
            "10s",
            "30s",
            "1m",
            "5m",
            "15m",
            "30m",
            "1h",
            "2h",
            "1d"
        ],
        "time_options": [
            "5m",
            "15m",
            "1h",
            "6h",
            "12h",
            "24h",
            "2d",
            "7d",
            "30d"
        ]
    },
    "timezone": "",
    "title": "VARIABLE",
    "uid": "VARIABLE",
    "version": 1
}"""

BOARD_BODY = """{
    "aliasColors": {
    },
    "bars": false,
    "dashLength": 10,
    "dashes": false,
    "datasource": "InfluxDB-1",
    "fill": 0,
    "gridPos": {
        "h": 9,
        "w": 12,
        "x": "VARIABLE",
        "y": "VARIABLE"
    },
    "id": "VARIABLE",
    "legend": {
        "alignAsTable": true,
        "avg": true,
        "current": true,
        "max": true,
        "min": true,
        "show": true,
        "total": true,
        "values": true
    },
    "lines": true,
    "linewidth": 2,
    "links": [
    ],
    "nullPointMode": "null",
    "percentage": false,
    "pointradius": 5,
    "points": false,
    "renderer": "flot",
    "seriesOverrides": [
    ],
    "spaceLength": 10,
    "stack": false,
    "steppedLine": false,
    "targets": [
        {
            "tags": [
                {
                    "key": "IP",
                    "operator": "=",
                    "value": "VARIABLE"
                },
                {
                    "condition": "AND",
                    "key": "InterFace",
                    "operator": "=",
                    "value": "VARIABLE"
                }
            ],
            "groupBy": [
            ],
            "measurement": "traffic_test",
            "orderByTime": "ASC",
            "policy": "default",
            "refId": "A",
            "resultFormat": "time_series",
            "select": [
                [
                    {
                        "params": [
                            "InSpeed"
                        ],
                        "type": "field"
                    }
                ],
                [
                    {
                        "params": [
                            "OutSpeed"
                        ],
                        "type": "field"
                    }
                ]
            ]
        }

    ],
    "thresholds": [
    ],
    "timeFrom": null,
    "timeRegions": [
    ],
    "timeShift": null,
    "title": "VARIABLE",
    "tooltip": {
        "shared": true,
        "sort": 0,
        "value_type": "individual"
    },
    "type": "graph",
    "xaxis": {
        "buckets": null,
        "mode": "time",
        "name": null,
        "show": true,
        "values": [
        ]
    },
    "yaxes": [
        {
            "format": "bps",
            "label": null,
            "logBase": 1,
            "max": null,
            "min": null,
            "show": true
        },
        {
            "format": "short",
            "label": null,
            "logBase": 1,
            "max": null,
            "min": null,
            "show": true
        }
    ],
    "yaxis": {
        "align": false,
        "alignLevel": null
    }
}"""
