# -*- coding: utf-8 -*-

import time
import logging
from logging import handlers

import get_snmp
import insert_db
import create_json
import alarm_manager


# RESULT 구조 {'name' : [사용량 , 임계치, 사용률, 횟수]}
# 리스트 두개 비교해서 없으면 입력 있을시 더큰값으로 변경
def _list_diff(stack):
    result = {}
    for low in stack:
        cnt = 1
        for key, val in low.items():
            if key in result:
                cnt = int(result[key][3]) + 1
                # 최고치 트래픽 뽑기
                if val[2] > result[key][2]:
                    result[key] = val
            else:
                result[key] = val
            result[key].insert(3, cnt)
    logging.debug("Alarm Send List Data = {val}".format(val=result))
    return result


def _msg_produce(produce_list):
    now = time.localtime()
    time_format = time.strftime("%H:%M", now)
    result = []
    for key, val in produce_list.items():
        msg_format = "(" + time_format + ") " + str(key) + " T(" + str(format(val[0], ',')) + "kb/" + str(
            format(val[1], ',')) + "kb/" + str(val[2]) + "%/" + str(format(val[3], ',')) + "번) 발생"
        result.append(msg_format)
    logging.debug("Alarm Send Msg Create = {val}".format(val=result))
    return result


def agt_type_all(snmp, session, SERVER_INFO):
    logging.debug("===========Agent Start(IP:{ip}, MOD: ALL)===========".format(ip=snmp['ip']))
    alarm_list = []
    loop_cnt = 1
    while True:
        logging.info("Check Loop (IP:{ip}/ CNT:{cnt}/ ALARM:{alarm})".format(ip=snmp['ip'], cnt=loop_cnt,
                                                                             alarm=int(SERVER_INFO['alarm_cnt'])))
        # SNMP 장비 성능 가져오기
        pfmance = get_snmp.performance_get(snmp)
        pfmance_json = create_json.conv_json_performance(pfmance, snmp, SERVER_INFO)

        # DB에 메모리 데이터 입력
        if len(pfmance_json) > 0:
            insert_db.insert(pfmance_json, session, snmp, SERVER_INFO)  # DB 입력
        else:
            logging.error("Json Memory Data Null Insert Do Not Try (IP:{ip})".format(ip=snmp['ip']))

        # SNMP 트래픽 데이터 가져오기
        old = get_snmp.net_traffic_get(snmp)
        time.sleep(int(SERVER_INFO['snmp_cycle']))
        after = get_snmp.net_traffic_get(snmp)

        # JSON 변환 및 임계치 알람 체크
        traffic_result = create_json.conv_json_traffic(old, after, snmp, SERVER_INFO)
        traffic_json = traffic_result[0]
        traffic_alarm = traffic_result[1]

        # DB에 트래픽 데이터 입력
        if len(traffic_json) > 0:
            insert_db.insert(traffic_json, session, snmp, SERVER_INFO)
        else:
            logging.error("Json Traffic Data Null Insert Do Not Try (IP:{ip})".format(ip=snmp['ip']))

        # 알람 발송 로직
        if len(traffic_alarm) > 0:
            for val in traffic_alarm:
                alarm_list.append(val)

        if loop_cnt >= int(SERVER_INFO['alarm_cnt']):
            if len(alarm_list) > 0:
                send = _list_diff(alarm_list)
                msg = _msg_produce(send)
                alarm_manager.msg_send(msg, SERVER_INFO['alarm_user'])
            # 초기화
            alarm_list = []
            loop_cnt = 0

        loop_cnt += 1
        # LOOP END


def agt_type_traffic(snmp, session, SERVER_INFO):
    logging.debug("===========Agent Start(IP:{ip}, MOD: ALL)===========".format(ip=snmp['ip']))
    alarm_list = []
    loop_cnt = 1
    while True:
        logging.info("Check Loop (IP:{ip}/ CNT:{cnt}/ ALARM:{alarm})".format(ip=snmp['ip'], cnt=loop_cnt,
                                                                             alarm=int(SERVER_INFO['alarm_cnt'])))
        # SNMP 트래픽 데이터 가져오기
        old = get_snmp.net_traffic_get(snmp)
        time.sleep(int(SERVER_INFO['snmp_cycle']))
        after = get_snmp.net_traffic_get(snmp)

        # JSON 변환 및 임계치 알람 체크
        traffic_result = create_json.conv_json_traffic(old, after, snmp, SERVER_INFO)
        traffic_json = traffic_result[0]
        traffic_alarm = traffic_result[1]

        # DB에 트래픽 데이터 입력
        if len(traffic_json) > 0:
            insert_db.insert(traffic_json, session, snmp, SERVER_INFO)
        else:
            logging.error("Json Traffic Data Null Insert Do Not Try (IP:{ip})".format(ip=snmp['ip']))

        # 알람 발송 로직
        if len(traffic_alarm) > 0:
            for val in traffic_alarm:
                alarm_list.append(val)

        if loop_cnt >= int(SERVER_INFO['alarm_cnt']):
            if len(alarm_list) > 0:
                send = _list_diff(alarm_list)
                msg = _msg_produce(send)
                alarm_manager.msg_send(msg, SERVER_INFO['alarm_user'])
            # 초기화
            alarm_list = []
            loop_cnt = 0

        loop_cnt += 1
        # LOOP END


def agt_type_memory(snmp, session, SERVER_INFO):
    logging.debug("===========Agent Start(IP:{ip}, MOD: ALL)===========".format(ip=snmp['ip']))
    loop_cnt = 1
    while True:
        logging.info("Check Loop (IP:{ip}/ CNT:{cnt}/ ALARM:{alarm})".format(ip=snmp['ip'], cnt=loop_cnt,
                                                                             alarm=int(SERVER_INFO['alarm_cnt'])))
        # SNMP 장비 성능 가져오기
        pfmance = get_snmp.performance_get(snmp)
        pfmance_json = create_json.conv_json_performance(pfmance, snmp, SERVER_INFO)

        # DB에 메모리 데이터 입력
        if len(pfmance_json) > 0:
            insert_db.insert(pfmance_json, session, snmp, SERVER_INFO)  # DB 입력
        else:
            logging.error("Json Memory Data Null Insert Do Not Try (IP:{ip})".format(ip=snmp['ip']))

        # LOOP END
