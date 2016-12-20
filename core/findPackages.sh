IMAGE=$1;

docker pull $IMAGE

AAA="$(docker run -it $IMAGE dpkg --get-selections | grep -v deinstall )" || AAA="not found";
if [[ $AAA != *"not found"* ]]
then
  echo "${AAA}" | awk {'print $1'} > file.txt;
  exit;
fi

BBB="$(docker run -it $IMAGE rpm -qa)"
if [[ $BBB != *"not found"* ]]
then
  echo "${BBB}" > file.txt;
  exit;
else
 echo "No supported package manager found on image" > file.txt;
fi
