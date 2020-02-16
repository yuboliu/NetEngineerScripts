#!/bin/bash

source ./ShellTemp.sh
Username=root
Password=centos
DeviceIP=192.168.239.7
IP=$1
Netmask=$2

/usr/bin/expect <<-EOF
    set timeout 30
    spawn ssh "$Username\@$DeviceIP"

    expect_before "yes/no" { send "yes\r" ; sleep 1 }
    expect_after "not found" { send_user "\nAn error has occurred\n\n" ; close }

    expect "*assword*"
    send "$Password\r"
# 常规写法

    #expect {
        #"*yes/no)?" { send "yes\r"; exp_continue [-continue_timer] }
        #"*assword:" { send "$Password\r" }
    #}
# 多分支写法
    expect "*#" { send "set address Untrust $IP/$Netmask $IP/$Netmask\r" }
# 一行写法
    expect "*#"
    send "save\r"
    send "quit\r"
# 一个expect搭配多个send
    expect eof
EOF
