#!/bin/bash
set -o allexport

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $DIR/..

if [ -e .env ]; then
	source .env
fi
echo $JEFF_DOCKER_IMAGE_LOCAL

docker build -t $JEFF_DOCKER_IMAGE_LOCAL:$JEFF_IMAGE_VERSION . 
