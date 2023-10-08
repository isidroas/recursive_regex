#!/bin/bash
dir=d1
matches=$(grep -o -R 'ho.a' $dir | wc -l)
echo there are $matches matches
test $matches -gt 0 || exit 1

find  $dir -type f | xargs recursive_regex -i --dry-run 'ho.a' 'adios'
