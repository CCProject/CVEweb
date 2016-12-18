#!/bin/bash

# assumes that docker is already installed

FILE=output22.txt
touch $FILE


#if [ $# != 2 ]
docker pull $1
cp 
docker run -i -t $1 /bin/bash -c "dpkg --get-selections | grep -v deinstall | cut -f1" > $FILE

exit 0
