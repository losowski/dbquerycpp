#!/bin/sh
# SUDO this script
#Magic Script to create an LDCONFIG link to here
echo "$PWD/lib" >> /etc/ld.so.conf.d/dbquery.conf
ldconfig
