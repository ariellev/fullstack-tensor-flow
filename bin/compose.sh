#!/bin/bash
set -e

source $(dirname "$0")/common.sh

cmd=$1

# script to start docker compose
USAGE="Usage: $(basename $0) [COMMAND] [options]"

if [ "$#" == "0" ]; then
	echo "$USAGE"
	exit 1
fi

# shift once to skip COMMAND
shift

while [[ $# -gt 1 ]]
do
key="$1"

case $key in
    -f|--file)
    compose_file="$2"
    shift # past argument
    ;;
    -r|--registry)
    registry="$2"
    shift # past argument
    ;;
    -d|--docker-ip)
    docker_ip="$2"
    shift # past argument
    ;;
    -p|--project-name)
    project_name="$2"
    shift # past argument
    ;;
    -t|--tag)
    tag="$2"
    shift # past argument
    ;;
    *)
					# unknown option
    ;;
esac
shift # past argument or value
done

# default values
if [ -z ${docker_ip} ]; then
    docker_ip=$(ifconfig | grep 'inet 192' | cut -d " " -f2)
fi

if [ -z ${project_name} ]; then
    project_name=lab
fi

if [ -z ${tag} ]; then
    tag=latest
fi

if [ -z ${registry} ]; then
    registry=localhost:5000
fi

export env_file=$(basename $compose_file | sed 's/.yml/.env/g')

echo -------------------------------------------------------
echo "docker-compose           $(bold $cmd)"
echo -------------------------------------------------------
echo "$(bold compose_file)     $compose_file"
echo "$(bold env_file)         $env_file"
echo "$(bold project)          $project_name"
echo "$(bold docker_ip)        $docker_ip"
echo "$(bold registry)         $registry"
echo "$(bold tag)              $tag"
echo -------------------------------------------------------

export docker_ip=$docker_ip
export registry=$registry
export tag=$tag

function up() {
		docker-compose -p $project_name -f $compose_file ${cmd} -d
	  echo --------------------------------------
	  echo service-ip     $(bold $docker_ip)
	  echo --------------------------------------
	  echo "done"
}

args="-d"
if [ "${cmd}" = "down" ]; then
	args=""
fi
docker-compose -p $project_name -f $compose_file ${cmd} ${args}
