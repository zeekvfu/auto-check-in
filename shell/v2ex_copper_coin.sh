#!/bin/bash
# v2ex_copper_coin.sh


Random()
{
	shuf -i 5-55 -n 1
}


# 脚本所在的路径可能有需要转义的字符（eg. 空格），应该用 "$0"
work_dir=$(cd "$(dirname "$0")"; pwd)
AutoCheckIn="$work_dir/.."


sleep `Random`m

cd "$AutoCheckIn"/src
PYTHONPATH=$(pwd) python3 v2ex_copper_coin.py


exit 0


