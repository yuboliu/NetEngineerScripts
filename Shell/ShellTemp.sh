#!/bin/bash
IFS=$' \t\n'
export PS4='+{$LINENO:${FUNCNAME[0]}} '
trap ctrl_c INT
trap 'ErrorTrap $LINENO' ERR
set -o pipefail
set -e
set -u
#trap 'echo "[line:$LINENO]variable: abc=$abc"' DEBUG

function rs()
{
    if [ $? -eq 0 ];
    then
        echo -e "$@\033[31m .....success\033[0m"
    else
        echo -e "$@\033[32m .....error\033[0m"
    fi
}
function go()
{
    $@ >>/dev/null 2>&1
    rs $@
}
function ErrorTrap()
{
    echo -e "\033[31m[LINE:$1] Error: Command or function exited with status $?\033[0m"
}
function ctrl_c()
{
    echo -e "\n"
    exit 0
}
