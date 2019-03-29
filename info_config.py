# -*- coding: utf-8 -*-

import logging
from logging import handlers
import configparser


# 현재 지원하는 DB 타입 검사
def _supoort_check(type):
    support_db = ['influxdb', 'mysql', 'mssql', 'oracle']
    if type.lower() not in support_db:
        logging.error("Not Support DB Type (TYPE = {type})".format(type=type))
        logging.info("Support List (TYPE = {type})".format(type=support_db))
        exit(1)


def read_config(path):
    # Config 파일 가져오기
    cfg = configparser.ConfigParser()
    cfg.read(path)
    user_list = []
    SERVER_INFO = {}
    SERVER_INFO['type'] = cfg.get('DADA_DB', 'DB_TYPE')
    _supoort_check(SERVER_INFO['type'])
    SERVER_INFO['traffic'] = cfg.get('DADA_DB', 'DB_TRAFFIC_TABLE')
    SERVER_INFO['performance'] = cfg.get('DADA_DB', 'DB_PERFOMANCE_TABLE')
    SERVER_INFO['ip'] = cfg.get('DADA_DB', 'DB_IP')
    SERVER_INFO['port'] = cfg.get('DADA_DB', 'DB_PORT')
    SERVER_INFO['name'] = cfg.get('DADA_DB', 'DB_NAME')
    SERVER_INFO['user'] = cfg.get('DADA_DB', 'DB_USER')
    SERVER_INFO['passwd'] = cfg.get('DADA_DB', 'DB_PASSWD')
    SERVER_INFO['snmp_cycle'] = cfg.get('SNMP', 'SNMP_CYCLE')
    SERVER_INFO['agt_type'] = cfg.get('SNMP', 'AGENT_TYPE')
    SERVER_INFO['log_level'] = cfg.get('LOG', 'LOG_LEVEL')
    SERVER_INFO['alarm_cnt'] = cfg.get('ALARM', 'ALARM_COUNT')
    # 알람 대상 리스트 가져오기 1 ~ 10 까지
    for i in range(1, 10):
        try:
            user = {}
            phn = cfg.get('ALARM', 'PHN_ID_' + str(i))
            call = cfg.get('ALARM', 'CALLBACK_' + str(i))
            user['phn_id'] = phn
            user['call'] = call
            user_list.append(user)
        except:
            pass
    SERVER_INFO['alarm_user'] = user_list

    return SERVER_INFO
