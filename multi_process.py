# -*- coding: utf-8 -*-

import sys
import logging
from logging import handlers
from multiprocessing import Process

import get_snmp
import conn_db
import info_config
import agent_mod_list
from config import snmplist

if __name__ == '__main__':
    # log settings
    log_formatter = logging.Formatter('%(asctime)s\t%(levelname)s\t%(filename)s:%(lineno)s\t%(message)s')

    # handler settings
    log_handler = handlers.TimedRotatingFileHandler(filename='./log/snmp_get.log', when='midnight', interval=1,
                                                    encoding='utf-8')
    log_handler.setFormatter(log_formatter)
    log_handler.suffix = "%Y%m%d"

    # logger set
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(log_handler)

    logging.info("===========Proccess Start===========")

    # Config 읽어오기
    logging.info("===========Read Config===========")
    SERVER_INFO = info_config.read_config('./config/server.cfg')

    # Log 레벨 셋팅
    if SERVER_INFO['log_level'].lower() == 'debug':
        logger.setLevel(logging.DEBUG)
    elif SERVER_INFO['log_level'].lower() == 'info':
        logger.setLevel(logging.INFO)
    elif SERVER_INFO['log_level'].lower() == 'error':
        logger.setLevel(logging.ERROR)
    else:
        logger.setLevel(logging.INFO)
        logging.error("Unknown Log Level({level}) Default = INFO".format(level=SERVER_INFO['log_level']))

    # Config 누락값 체크
    for key, val in SERVER_INFO.items():
        logging.debug("Config Read List (ITEM = {key}, VAL = {val})".format(key=key, val=val))
        if val is '':
            logging.error("Config Value Empty (ITEM = {key})".format(key=key))
            exit(1)
    logging.info("===========Config Read Success===========")

    # DB 연결
    logging.info("===========DB Connection Start===========")
    session = conn_db.db_connect(SERVER_INFO)

    thread_num = 0
    switch_val = SERVER_INFO['agt_type'].replace(' ', '')
    # Agent Type 확인 후 시작
    for snmp_list in snmplist.SNMP_SERVER_LIST:
        if 'ALL' in SERVER_INFO['agt_type'].replace(' ', ''):
            my_process = Process(target=agent_mod_list.agt_type_all, args=(snmp_list, session, SERVER_INFO))
        elif 'MEMORY' in SERVER_INFO['agt_type'].replace(' ', ''):
            my_process = Process(target=agent_mod_list.agt_type_memory, args=(snmp_list, session, SERVER_INFO))
        elif 'TRAFFIC' in SERVER_INFO['agt_type'].replace(' ', ''):
            my_process = Process(target=agent_mod_list.agt_type_traffic, args=(snmp_list, session, SERVER_INFO))
        else:
            my_process = Process(target=agent_mod_list.agt_type_all, args=(snmp_list, session, SERVER_INFO))
        logging.info("===========Thread Start (IP:{ip} / NUM:{n})===========".format(ip=snmp_list['ip'], n=thread_num))
        logging.debug("===========SNMP Config ({con})===========".format(con=snmp_list))
        thread_num += 1
        my_process.start()
