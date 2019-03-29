# -*- coding: utf-8 -*-

import json
import logging
from logging import handlers
from datetime import datetime

import alarm_manager


def _mem2str(size):
    prefix = 'KByte'
    if (size > 1048576):
        size = size / 1048576
        prefix = 'GByte'
    elif (size > 1024):
        size = size / 1024
        prefix = 'MByte'
    return str(round(size, 1)) + ' ' + prefix


def conv_json_traffic(old, after, snmp, SERVER_INFO):
    json_result = []
    alarm_result = []
    for list_a, list_b in zip(old, after):  # 2개의 리스트를 계산해서 트래픽 사용량
        insert = {}
        if list_a['ifDescr'] == list_b['ifDescr']:
            # 큰데이터 - 작은 데이터를 해야 하므로 list_b - list_a
            diff_time = datetime.strptime(list_b['Time'], '%Y%m%d%H%M%S') - datetime.strptime(list_a['Time'],
                                                                                              '%Y%m%d%H%M%S')
            sec_time = int(diff_time.seconds)

            # KByte로 변환 / 1024
            # SNMP 트래픽 값이 최대 32bit라 넘을시 0부터 초기화 계산시 - 출력되어 아래의 방지 코드 추가 UInteger32
            if float(list_b['ifOutOctets']) < float(list_a['ifOutOctets']):
                cal_outbyte = (4294967295 - float(list_a['ifOutOctets'])) + float(list_b['ifOutOctets'])
                logging.warning("OutOctets Exceeding The Maximum Value (-) Prevention (IP:{ip})".format(ip=snmp['ip']))
            else:
                cal_outbyte = float(list_b['ifOutOctets']) - float(list_a['ifOutOctets'])

            if float(list_b['ifInOctets']) < float(list_a['ifInOctets']):
                cal_inbyte = (4294967295 - float(list_a['ifInOctets'])) + float(list_b['ifInOctets'])
                logging.warning("InOctets Exceeding The Maximum Value (-) Prevention (IP:{ip})".format(ip=snmp['ip']))
            else:
                cal_inbyte = float(list_b['ifInOctets']) - float(list_a['ifInOctets'])

            # KByte로 변환 / 1024
            in_volume = cal_inbyte / 1024
            out_volume = cal_outbyte / 1024
            # bit/s로 변환 * 8 / 시간
            in_speed = (cal_inbyte * 8) / sec_time
            out_speed = (cal_outbyte * 8) / sec_time

            insert = {
                'measurement': SERVER_INFO['traffic'],
                'tags': {
                    'InterFace': list_b['ifDescr'],
                    'IP': snmp['ip']
                },
                'fields': {
                    'Status': list_b['ifAdminStatus'],
                    'InVolume': round(in_volume, 2),
                    'OutVolume': round(out_volume, 2),
                    'InSpeed': round(in_speed, 2),
                    'OutSpeed': round(out_speed, 2),
                    'Time': sec_time
                }
            }

            # 알람 사용 여부 확인 후 초과 여부 확인
            if snmp['alarm_used'].lower() == 'y':
                device = snmp['ip'] + '@' + list_b['ifDescr']
                if in_speed >= out_speed:
                    check = alarm_manager.traffic_compare(device, in_speed)
                else:
                    check = alarm_manager.traffic_compare(device, out_speed)
                if check != None:
                    alarm_result.append(check)

        elif list_a['ifDescr'] != list_b['ifDescr']:
            logging.error("List InterFace Not Equal (IP:{ip})".format(ip=snmp['ip']))
            logging.error("List A = ({Aval})\nList B = ({Bval})".format(Aval=list_a, Bval=list_b))
        json_result.append(insert)

    try:
        json.dumps(json_result)
        logging.info("Json Conversion Success (IP:{ip})".format(ip=snmp['ip']))
        logging.debug("Json Data = ({val})".format(val=json_result))
    except Exception as e:
        logging.error("Json Conversion Fail (IP:{ip} / {detail})".format(ip=snmp['ip'], detail=e))
        logging.error("Json Data = ({val})".format(val=json_result))

    return [json_result, alarm_result]


def conv_json_performance(data, snmp, SERVER_INFO):
    result = []
    for list in data:
        real_free_mem = int(list['MemoryAvail']) + int(list['MemoryCache']) + int(list['MemoryBuffer'])
        real_free_per = int((int(real_free_mem) / int(list['MemoryTotal'])) * 100)
        insert = {
            'measurement': SERVER_INFO['performance'],
            'tags': {
                'IP': snmp['ip']
            },
            'fields': {
                'TotalMemory': _mem2str(int(list['MemoryTotal'])),
                'RealFreeMemory': _mem2str(real_free_mem),
                'RealFreePercent': str(real_free_per) + ' %',
                'FreeMemory': _mem2str(int(list['MemoryAvail'])),
            }
        }
        result.append(insert)
    try:
        json.dumps(result)
        logging.info("Json Conversion Success (IP:{ip})".format(ip=snmp['ip']))
        logging.debug("Json Data = ({val})".format(val=result))
    except Exception as e:
        logging.error("Json Conversion Fail (IP:{ip} / {detail})".format(ip=snmp['ip'], detail=e))
        logging.error("Json Data = ({val})".format(val=result))

    return result
