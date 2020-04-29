#!/bin/sh
# Build a single import file
for file in $(ls -1 *.sql); do cat $file > procedures.sqlx ;done
