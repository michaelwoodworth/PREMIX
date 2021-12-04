#!/bin/bash

# define input variables
stem=$1         # search string for tails to print
length=$2       # line argument to pass to tail

# talk to human

if [[ ! -z $stem ]] && [[ ! -z $length ]] # test if required input parameter is empty
then

        echo "###############################################"
        echo "                    "
        echo " ___     ___     __ "
        echo "  |  /\   |  |  (_  "
        echo "  | /--\ _|_ |_ __) "
        echo "                    "
        echo "###############################################"
        echo ""

        # loop renaming
        for f in `ls ${stem}`
        do echo $f
        tail -n $length $f
        echo ''
        echo ''
        done

else
        echo ""
        echo "ERROR: Check input parameters..."
        echo "  example usage: tails.sh {stem} {length}"
        echo "  stem -  string for searching, if passing wildcards"
        echo "          make sure to pass in quotes."
        echo "          e.g. "*.log"  "*R1*""
        echo ""
        echo "  length - integer number of lines for tail command"
        echo "          e.g. 5, 20, etc."

fi
