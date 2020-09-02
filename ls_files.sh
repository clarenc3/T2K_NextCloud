#!/bin/bash

if [[ $# -gt 2 ]]; then
  echo "Can't take more than one argument"
  exit -1
fi

# Using instructions from https://t2k.org/asg/oagroup/gadatastorage/index_html

user="ASGReader"
#user="T2KSKReader"

folder="https://nextcloud.nms.kcl.ac.uk/remote.php/dav/files/${user}"
subfolder=$1

output="test"

#curl -u ${user} ${folder}/${account} --output ${test}

#curl -u ${user} -X PROPFIND ${folder}/${account} --output test.xml

curl -s -u ${user} -X PROPFIND ${folder}/${subfolder} | python lsdav.py
#curl -s -u ${user} -X PROPFIND ${folder}/${subfolder} --output ${output}
