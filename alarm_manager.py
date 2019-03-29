# -*- coding: utf-8 -*-

import socket
import logging
from logging import handlers

from config import alarmlist


def traffic_compare(name, traffic):
    user_list = alarmlist.ALARM_USER_LIST
    result = None
    if name in user_list:
        kb_traffic = int(traffic / 1024)
        kb_per = int(kb_traffic / user_list[name][0] * 100)
        if kb_per >= 70:
            if len(user_list[name]) > 1:
                result = {alarmlist.ALARM_USER_LIST[name][1]: [kb_traffic, user_list[name][0], kb_per]}
                logging.info("Alarm Occurrence Change InterFace Name (old={old}, new={new})".format(old=name,
                                                                                                    new=user_list[name][
                                                                                                        1]))
                logging.debug("Alarm Result Value = ({val})".format(val=result))
            else:
                result = {name: [kb_traffic, user_list[name][0], kb_per]}
                logging.info("Alarm Occurrence InterFace = {iface}".format(iface=name))
                logging.debug("Alarm Result Value = ({val})".format(val=result))
    else:
        logging.warning("InterFace = {iface} Alarm Threshold Not Found".format(iface=name))

    return result


# TEXT 구조 ['문자내용1', '문자내용2' ]
# PHN 구조 [{'phn_id': '수신번호','call': '발신번호'}, {'phn_id': '수신번호','call': '발신번호'}]
def msg_send(text, phn):
    host = '192.168.80.1'
    port = 7777
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.settimeout(3)

    try:
        client.connect((host, port))
        for msg in text:
            for val in phn:
                send_format = "SMS\t" + val['phn_id'] + "\t" + val['call'] + "\t" + msg + "\n"
                client.send(send_format.encode('euc-kr'))
        logging.info("Alarm Send Success = ({msg})".format(msg=text))
    except Exception as e:
        logging.error("Alarm Send Socket Error = ({detail})".format(detail=e))

    client.close()
