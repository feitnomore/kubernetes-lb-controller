#!/bin/sh
# Build and Exec
# I am too tired of doing this by hand

docker rm kubernetes-lb-controller
docker rmi kubernetes-lb-controller --force
docker build -t kubernetes-lb-controller .
