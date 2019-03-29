# -*- coding: utf-8 -*-

# 'IP@InterFace' : [ 임계치, '별명'],
# IP = 모니터링 서버 IP
# InterFacce = 인터페이스 snmplist 파일에서 name_conver 기능을 사용 할 경우 eth0와 같은 명칭이 아닌 고유 숫자 입력
# 임계치 = kbit 단위 이며 최대 가능 임계치 입력
# 별명 = 사용 하지 않아도 되며 IP@InterFace라고 알람이 오는걸 원하는 별명으로 변경 가능

ALARM_USER_LIST = {
    '192.168.40.1@eth0': [10240, 'ConverName'],
    '192.168.40.1@eth1': [10240, 'ConverName'],
    '192.168.40.1@eth2': [10240, 'ConverName'],
    '192.168.55.1@eth0': [10240, 'ConverName'],
    '192.168.55.1@eth1': [10240, 'ConverName'],
}
