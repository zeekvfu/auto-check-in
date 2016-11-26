#!/bin/bash
# auto_check_in.sh


# 脚本所在的路径可能有需要转义的字符（eg. 空格），应该用 "$0"
work_dir=$(cd "$(dirname "$0")"; pwd)
AutoCheckIn="$work_dir/.."


cd "$AutoCheckIn"/src

# 每天 21/22/23 点，3 次尝试自动签到
while true; do
	hour=`date +'%H'`
	timestamp=`date +'%F_%T'`
	if [ "$hour" == "21" ] || [ "$hour" == "22" ] || [ "$hour" == "23" ]; then
		export PYTHONPATH=$(pwd)
		python3 v2ex_copper_coin.py > "$AutoCheckIn"/log/v2ex_copper_coin."$timestamp".log 2>&1 &
		python3 taobao_taojinbi.py > "$AutoCheckIn"/log/taobao_taojinbi."$timestamp".log 2>&1 &
		python3 jd_jingdou.py > "$AutoCheckIn"/log/jd_jingdou."$timestamp".log 2>&1 &
		sleep 1h
	else
		sleep 10m
	fi
done


exit 0


