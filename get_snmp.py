# -*- coding: utf-8 -*-

import time
import logging
from logging import handlers
from pysnmp.hlapi import *


def _exception_check(msg):
    except_msg = ['no more variables left in this mib view']
    if msg.lower() in except_msg:
        return 0
    else:
        return 1


# 네트워크 모든 인터페이스 트래픽 가져오기
def net_traffic_get(snmp):
    snmp_data = []
    index_dict = {}

    try:
        for (error_indication,
             error_status,
             error_index,
             var_binds) in nextCmd(SnmpEngine(),
                                   CommunityData(snmp['community'], mpModel=0),
                                   UdpTransportTarget((snmp['ip'], snmp['port']),
                                                      timeout=2,
                                                      retries=1
                                                      ),
                                   ContextData(),
                                   ObjectType(ObjectIdentity('IF-MIB', 'ifDescr')),  # 인터페이스명
                                   ObjectType(ObjectIdentity('IF-MIB', 'ifAdminStatus')),  # 인터페이스 up, down 상태
                                   ObjectType(ObjectIdentity('IF-MIB', 'ifOutOctets')),  # out 트래픽 (1 octet = 1 byte)
                                   ObjectType(ObjectIdentity('IF-MIB', 'ifInOctets')),  # in 트래픽 (1 octet = 1 byte)
                                   lexicographicMode=False):

            if error_indication:
                logging.error("\tTraffic Snmp Data Error (IP:{ip} / {err})".format(err=error_indication, ip=snmp['ip']))
                break
            elif error_status:
                logging.error("\tTraffic Snmp Data Error (IP:{ip} / {err})".format(err=error_status, ip=snmp['ip']))
                break
            else:
                for var_bind in var_binds:
                    var_tmp = [x.prettyPrint() for x in var_bind]
                    var_tmp2 = var_tmp[0].replace('IF-MIB::', '').split('.')
                    if var_tmp2[1] in index_dict:
                        key = index_dict.get(var_tmp2[1])
                        if var_tmp2[0] == 'ifDescr' and snmp['name_conver'].lower() == 'y':
                            snmp_data[key][var_tmp2[0]] = var_tmp2[1]
                        else:
                            snmp_data[key][var_tmp2[0]] = var_tmp[1]
                    else:
                        if var_tmp2[0] == 'ifDescr' and snmp['name_conver'].lower() == 'y':
                            item_dict = {var_tmp2[0]: var_tmp2[1]}
                        else:
                            item_dict = {var_tmp2[0]: var_tmp[1]}
                        time_dict = {'Time': time.strftime('%Y%m%d%H%M%S')}  # 인터페이스 마다 트래픽 계산용 시간 넣기
                        item_dict = {**item_dict, **time_dict}
                        snmp_data.append(item_dict)
                        index_dict[var_tmp2[1]] = snmp_data.index(item_dict)
                logging.info("\tTraffic Snmp Data Get Success (IP:{ip})".format(ip=snmp['ip']))
        logging.debug("\tTraffic Snmp Data (IP:{ip}) = ({snmp})".format(snmp=snmp_data, ip=snmp['ip']))
    except Exception as e:
        logging.error("\tTraffic Snmp Data Get Fail (IP:{ip} / {detail})".format(ip=snmp['ip'], detail=e))
    return snmp_data


# 장비 CPU,RAM 등 성능 가져오기
def performance_get(snmp):
    snmp_data = []
    try:
        for (error_indication,
             error_status,
             error_index,
             var_binds) in nextCmd(SnmpEngine(),
                                   CommunityData(snmp['community'], mpModel=0),
                                   UdpTransportTarget((snmp['ip'], snmp['port']),
                                                      timeout=2,
                                                      retries=1
                                                      ),
                                   ContextData(),
                                   ObjectType(ObjectIdentity('1.3.6.1.4.1.2021.4.5')),  # 총 RAM
                                   ObjectType(ObjectIdentity('1.3.6.1.4.1.2021.4.6')),  # 총 RAM 사용 가능
                                   ObjectType(ObjectIdentity('1.3.6.1.4.1.2021.4.14')),  # 총 RAM 버퍼
                                   ObjectType(ObjectIdentity('1.3.6.1.4.1.2021.4.15')),  # 총 RAM 캐시
                                   lexicographicMode=False):

            if error_indication:
                logging.error(
                    "\tPerformance Snmp Data Error (IP:{ip} / {err})".format(err=error_indication, ip=snmp['ip']))
                break
            elif error_status:
                logging.error("\tPerformance Snmp Data Error (IP:{ip} / {err})".format(err=error_status, ip=snmp['ip']))
                break
            else:
                device_dict = {}
                for var_bind in var_binds:
                    var_tmp = [x.prettyPrint() for x in var_bind]
                    if var_tmp[0] in 'SNMPv2-SMI::enterprises.2021.4.5.0':
                        item_dict = {'MemoryTotal': var_tmp[1]}
                    elif var_tmp[0] in 'SNMPv2-SMI::enterprises.2021.4.6.0':
                        item_dict = {'MemoryAvail': var_tmp[1]}
                    elif var_tmp[0] in 'SNMPv2-SMI::enterprises.2021.4.14.0':
                        item_dict = {'MemoryBuffer': var_tmp[1]}
                    elif var_tmp[0] in 'SNMPv2-SMI::enterprises.2021.4.15.0':
                        item_dict = {'MemoryCache': var_tmp[1]}
                    else:
                        item_dict = {var_tmp[0]: var_tmp[1]}
                    device_dict = {**device_dict, **item_dict}
                snmp_data.append(device_dict)
                logging.info("\tPerformance Snmp Data Get Success (IP:{ip})".format(ip=snmp['ip']))
        logging.debug("\tPerformance Snmp Data (IP:{ip}) = ({snmp})".format(snmp=snmp_data, ip=snmp['ip']))
    except Exception as e:
        logging.error("\tPerformance Snmp Data Get Fail (IP:{ip} / {detail})".format(ip=snmp['ip'], detail=e))
    return snmp_data
