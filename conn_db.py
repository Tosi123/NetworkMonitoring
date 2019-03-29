# -*- coding: utf-8 -*-

import logging
from logging import handlers
from influxdb import InfluxDBClient
from influxdb.client import InfluxDBClientError


def _influx_db(SERVER_INFO):
    db_session = InfluxDBClient(host=SERVER_INFO['ip'], port=SERVER_INFO['port'], username=SERVER_INFO['user'],
                                password=SERVER_INFO['passwd'],
                                database=SERVER_INFO['name'], ssl=False, verify_ssl=False, timeout=None,
                                retries=5)  # DB 연결
    try:
        check = db_session.get_list_database()  # DB를 조회하여 존재 하지 않으며 프로그램 종료
        for list in check:
            if SERVER_INFO['name'] in list['name']:
                tmp = 1
                break;
        if tmp == 1:
            logging.info("DB Connection Success")
        else:
            logging.error("DB Connection Fail Not Found Database")
    except Exception as e:
        logging.error("DB Connection Fail = ({detail})".format(detail=e))
        exit(1)

    return db_session


def db_connect(SERVER_INFO):
    if SERVER_INFO['type'].lower() == 'influxdb':
        return _influx_db(SERVER_INFO)
    else:
        logging.error("Not Support DB Connection (TYPE = {type})".format(type=SERVER_INFO['type']))
        exit(1)
