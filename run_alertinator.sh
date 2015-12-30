#/usr/bin/bash

##	RUN_ALERTINATOR:
##	This script finds error files from the log directory, and feeds them into alertinator.py [which parses them and sends alerts]
##	Author: Yameen Rasheed
##	Date: 05 March 2013

CONFIG_FILE="/mnt/example/alertinator/config.ini"
SECTION="Default"

eval `sed -e 's/[[:space:]]*\=[[:space:]]*/=/g' \
    -e 's/;.*$//' \
    -e 's/[[:space:]]*$//' \
    -e 's/^[[:space:]]*//' \
    -e "s/^\(.*\)=\([^\"']*\)$/\1=\"\2\"/" \
   < $CONFIG_FILE \
    | sed -n -e "/^\[$SECTION\]/,/^\s*\[/{/^[^;].*\=.*/p;}"`
/usr/bin/python2.7 $alert_script_directory/alertinator.py `find $log_parent_directory -name error.log | grep -v processing` 




