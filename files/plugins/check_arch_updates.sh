#!/bin/bash
# Arch upgradeable packages

E_OK=0
E_WARNING=1
E_CRITICAL=2
E_UNKNOWN=3

warn=5
crit=10

if [[ -e /etc/os-release ]]
then
  . /etc/os-release
  distribution="${ID}"
fi

if [[ "${distribution}" == "arch" ]]
then

  PACMAN=$(command -v pacman)

  list=$(${PACMAN} --sync --sysupgrade --print 2> /dev/null)

  if [ "${list}" == "" ]
  then
    count=0
  else
    count=$(echo "${list}" | wc -l)
  fi

  if [[ "${count}" -eq 0 ]]
  then
    exit_code="${E_OK}"
    exit_msg="OK "

  elif [[ "${count}" -gt "${warn}" ]] && [[ "${count}" -lt "${crit}"  ]]
  then
    exit_code="${E_WARNING}"
    exit_msg="WARNING "
  else
    exit_code="${E_CRITICAL}"
    exit_msg="CRITICAL "
  fi


  echo -e "${exit_msg} ${count} packages available for upgrade\n"

  for pkg in ${list}
  do
    echo -n "  "
    echo ${pkg} | sed -e 's#.*/##g' -e 's%(.*).pkg.*$%1%'
  done

else
  echo "wrong distribution."
  exit_code="${E_UNKNOWN}"
fi

exit ${exit_code}
