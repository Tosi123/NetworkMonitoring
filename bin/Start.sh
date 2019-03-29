#!/usr/bin/env bash
LANG=ko_KR.utf8

###########################
PRO_NM="multi_process"
PYTHON_PATH="/usr/bin/python"
BIN_PATH="/path/monitor/snmp/python"
###########################
pid_chk=`ps -ef |grep "${PRO_NM}" |grep -v grep |wc -l`

if [[ ${pid_chk} -ne  0 ]]; then
echo "이미 프로세스가 실행중 입니다."
exit
else
cd ..
nohup ${PYTHON_PATH} ./multi_process.py >> ./log/snmp.out 2>> ./log/snmp.err &
fi

if [[ 0 -eq $? ]];then
sleep 3
pid=`ps -ef |grep "${PRO_NM}" |grep -v grep |awk '{print $2}'`
if [[ -n ${pid} ]];then
echo "프로세스 정상 실행 되었습니다!! (PID:${pid})"
else
echo "프로세스 실행 실패!!"
fi
else
echo "프로세스 실행 실패!!"
fi

