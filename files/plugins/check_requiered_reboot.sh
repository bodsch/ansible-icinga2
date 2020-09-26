#!/usr/bin/env bash
#
#

# exit codes
E_OK=0
E_WARNING=1
E_CRITICAL=2
E_UNKNOWN=3

NEXTLINE=0
FIND=""

for I in $(file /boot/vmlinuz*); do
  if [ ${NEXTLINE} -eq 1 ]; then
    FIND="${I}"
    NEXTLINE=0
  else
    if [ "${I}" = "version" ]; then NEXTLINE=1; fi
  fi
done

if [ ! "${FIND}" = "" ]; then
  CURRENT_KERNEL=$(uname -r)
  if [ ! "${CURRENT_KERNEL}" = "${FIND}" ]; then
    echo "reboot required (current kernel: '${CURRENT_KERNEL}' / new kernel: '${FIND}')"
    exit "${E_WARNING}"
  fi
fi

exit "${E_OK}"
