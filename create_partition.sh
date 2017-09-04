#!/usr/bin/expect
set device [lindex $argv 0]
spawn fdisk $device
expect  "Command*"
send "n\r"
expect "Select*"
send "\r"
expect "Partition num*"
send "\r"
expect "First*"
send "\r"
expect "Last*"
send "\r"
expect  "Command*"
send "w\r"