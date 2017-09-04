#!/usr/bin/expect

set resource [lindex $argv 0]

spawn drbdadm create-md $resource
set timeout 20
expect "yes"
send "yes\r"
expect eof
exit
