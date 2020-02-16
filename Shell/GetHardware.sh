#!/bin/bash

MemoryTotal=0

printf "CPU\n\t"
CPUName=`cat /proc/cpuinfo | grep "^model name" | uniq | awk -F ":" '{print $2}' | sed -e "s/^ *//" -e "s/ *//"`
CPUCount=`lscpu | grep ^Socket\(s\).* | awk '{print $2}'`
echo "$CPUName * $CPUCount"

printf "Memory\n"
dmidecode -t memory | grep -iP "Size|^\sType:|Speed|Serial Number:" | grep -P -A3 "^\sSize: \d.*" | grep -v "^--" | sed "/Serial Number/a\ \t-----------------------"
for var in `dmidecode -t memory | grep -iP "Size|^\sType:|Speed|Serial Number:" | grep -P -A3 "^\sSize: \d.*" | grep -v "^--" | grep Size | awk '{print $2}'`; do
    MemoryTotal=`expr $MemoryTotal + $var`
done
printf "\tTotal: %s MB" $MemoryTotal

fraqarr=(`dmidecode -t memory | grep -iP "Size|^\sType:|Speed|Serial Number:" | grep -P -A3 "^\sSize: \d.*" | grep -v "^--" | grep Speed | awk -F ": " '{print $2}' | sed 's/MHz//g' | sort | uniq`)
for fraq in ${fraqarr[@]}; do
    fraqcount=`dmidecode -t memory | grep -iP "Size|^\sType:|Speed|Serial Number:" | grep -P -A3 "^\sSize: \d.*" | grep -v "^--" | grep Speed | grep -c $fraq`
    printf "  %s*%sMhz\n" $fraqcount $fraq
done

printf "Disk:\n"
#for letter in {a..z}; do
#    hdparm -I /dev/sd${letter} 2>/dev/null | grep -P "^\sSerial Number:|^\sdevice size with M = 1000\*1000|^\sNominal Media Rotation Rate" 
#done
diskinfo=`lsblk --nodeps -o type,size,tran,serial | grep -v ^NAME | grep disk | sed "s@sas@sas/sata@g"`
echo -e "\t$diskinfo"

printf "NIC:\n"
printf "\tNetwork Interface Cards:\n"
lspci | grep -i eth | awk -F ": " '{print "\t\t"$2}'
printf "\tDBDF and Permanent address:\n"
iflist=(`ls -l /sys/class/net/ | grep -vE "virtual|^total" | awk '{print $9}'`)
for ifname in ${iflist[@]}; do
    echo -e "\t\t$(ethtool -i ${ifname} | grep ^bus-info | awk -F ": " '{print $2}') _ $(ethtool -P ${ifname} | awk -F ": " '{print $2}')"
done

