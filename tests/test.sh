#!/bin/bash
# TODO: copy to temp and delete

dir=$(mktemp -d /tmp/regex_test_data.XXXXX)
trap 'rm -r $dir' EXIT
cp -R d1 $dir
matches=$(grep -i -o -R 'ho.a' $dir | wc -l)
echo there are $matches matches
test $matches -gt 0 || exit 1

find  $dir -type f | xargs recursive_regex -i  'ho.a' 'adios'

test $(grep -o -R 'ho.a' $dir | wc -l) -eq 0 || exit 2

# commented because don't pass since there were 4 previous 'adios'
#test $(grep -o -R 'adios' $dir | wc -l) -eq $matches || exit 3
