# -*- coding: utf-8 -*-

import logging
from logging import handlers

from influxdb import InfluxDBClient
from influxdb.client import InfluxDBClientError


def _influx_insert(json, session, snmp):
    try:
        session.write_points(json)
        logging.info("\tDB Insert Success (IP:{ip})".format(ip=snmp['ip']))
    except Exception as e:
        logging.error("\tDB Insert Fail (IP:{ip} / {detail})".format(ip=snmp['ip'], detail=e))


def insert(json, session, snmp, SERVER_INFO):
    if SERVER_INFO['type'].lower() == 'influxdb':
        return _influx_insert(json, session, snmp)
    else:
        logging.error("Not Support DB Insert (TYPE = {type})".format(type=SERVER_INFO['type']))
        exit(1)
