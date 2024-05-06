#!/bin/bash
# auto_check_in.sh


work_dir=$(cd "$(dirname "$0")"; pwd)
cd "${work_dir}"
source "${work_dir}/util.sh"


if [ $# -ne 1 ]; then
	echo "CMD: $0 app"
	exit 1
fi


MyProject=`get_my_project_path`
PythonUtilSrc="$MyProject/python-util/src"
export PYTHONPATH=$PYTHONPATH:$PythonUtilSrc


rand=$(( ( RANDOM % 300 ) ))
sleep ${rand}s


AutoCheckIn="$MyProject/auto-check-in"
mkdir -p ${AutoCheckIn}/log

app_file_name="$1".py
cd $AutoCheckIn/python
python3.9 ${app_file_name}


exit 0


