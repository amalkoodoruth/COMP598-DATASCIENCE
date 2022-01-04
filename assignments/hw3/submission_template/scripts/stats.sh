#!/bin/bash

## saves the argument name as file
file=$1

## assigns number of lines to variable 'count'
count=$(wc -l $file | awk '{ print $1 }')

echo "$count"

if [ $count -lt 10000 ]
then
	echo "Error: There should be more than 10000 lines"
	exit 0
fi



## tail 10000, search, count, get rid of space

tail -n 10000 $file | grep -i "potus" | wc -l | awk '{ print $1 }'


tail -n +100 $file | head -n 200 | grep "(\W|^)(fake)\W" | wc -l | awk '{ print $1 }'