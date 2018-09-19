#!/bin/bash
if [[ "$(cat /var/scorebot/name)" == "" ]]; then
   exec 3>&1
   name=$(dialog --inputbox "Enter Your Name" 0 40 2>&1 1>&3)
   exec 3>&-
   if [[ $name != "" ]]; then
      echo $name > /var/scorebot/name
   fi
fi
