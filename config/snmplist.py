# -*- coding: utf-8 -*-

# ip = 모니터링할 서버의 IP
# community = SNMP 커뮤니티
# port = SNMP 포트
# name_conver = 동일 인터페이스 명이 있을경우만 사용 디바이스 명 대신 숫자 표시 기능 (Y/N)
# alarm_used = 트래픽 알람 사용 여부 (Y/N)

SNMP_SERVER_LIST = [
    {'ip': '192.168.40.1', 'community': 'public', 'port': 161, 'name_conver': 'N', 'alarm_used': 'N'},
    {'ip': '192.168.50.1', 'community': 'public', 'port': 161, 'name_conver': 'N', 'alarm_used': 'N'},
    {'ip': '192.168.30.1', 'community': 'public', 'port': 161, 'name_conver': 'N', 'alarm_used': 'N'},
    {'ip': '192.168.30.2', 'community': 'public', 'port': 161, 'name_conver': 'N', 'alarm_used': 'N'},
    {'ip': '192.168.30.3', 'community': 'public', 'port': 161, 'name_conver': 'N', 'alarm_used': 'N'},
    {'ip': '192.168.30.4', 'community': 'public', 'port': 161, 'name_conver': 'N', 'alarm_used': 'N'},
    {'ip': '192.168.30.5', 'community': 'public', 'port': 161, 'name_conver': 'N', 'alarm_used': 'N'},
    {'ip': '192.168.60.22', 'community': 'public', 'port': 161, 'name_conver': 'N', 'alarm_used': 'N'},
]
