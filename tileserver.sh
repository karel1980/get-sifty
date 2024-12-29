#!/bin/bash

docker rm -f tileserver
docker run --name tileserver --rm -d -it -v ./tiles:/data -p 8080:8080 maptiler/tileserver-gl
