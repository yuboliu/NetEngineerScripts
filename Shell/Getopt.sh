#!/bin/bash

ARGS=`getopt -o ab:c:: --long along,blong:,clong:: -n 'Not definded' -- "$@"`
if [ $? != 0  ]
then
    echo "GetOpt internal error" >&2
    exit 1
fi
echo $ARGS
eval set -- "$ARGS"
echo $ARGS
while true
do
    case "$1" in
        -a|--along)
            echo "Option a"
            shift
            ;;
        -b|--blong)
            echo "Option b, argument $2"
            shift 2
            ;;
        -c|--clong)
            case "$2" in
                "")
                    echo "Option c, no argument"
                    shift 2
                    ;;
                *)
                    echo "Option c, argument $2"
                    shift 2
                    ;;
            esac
            ;;
        --)
            break
            ;;
        *)
            echo "Internal error!"
            exit 1
            ;;
    esac
done
