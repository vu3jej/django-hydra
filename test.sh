#!/bin/bash
set -e
original=$(pwd)
keepenv=false
circle=false

while getopts "k" opt; do
    case ${opt} in
        k)
            echo "Keeping the old env"
            keepenv=true
            ;;
        \?)
            echo "Invalid option: -$OPTARG" >&2
            ;;
    esac
done

tmpfolder=""
appname=sampleapp
appdir=../$appname

unset DJANGO_SETTINGS_MODULE

if [ "$keepenv" = true ]; then
    export POETRY_VIRTUALENVS_IN_PROJECT=false
fi


echo "Removing old app"
if [[ -d "../$appname" ]]
then
    set +e
    rm -rf ../$appname
    dropdb test_sampleapp
    dropdb sampleapp
    set -e
fi

echo "Creating App"
cookiecutter . --default-config --no-input project_name=$appname -o ../


echo "Running tests"
cd ../$appname/

eval "$(direnv export bash)"
npm run build
pre-commit run --all-files
poetry run pytest


RV=$?
rm -rf static/
cd $original
exit $RV
