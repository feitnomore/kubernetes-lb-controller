#!/bin/sh
# Build and Exec
# I am too tired of doing this by hand

docker rm kubernetes-lb-controller:2.0
docker rmi kubernetes-lb-controller:2.0 --force
docker build -t kubernetes-lb-controller:2.0 .

# Pushing to remote repository
export MY_REPO="feitnomore"
docker tag kubernetes-lb-controller:2.0 $MY_REPO/kubernetes-lb-controller:2.0
docker push $MY_REPO/kubernetes-lb-controller:2.0

docker tag kubernetes-lb-controller:2.0 $MY_REPO/kubernetes-lb-controller:latest
docker push $MY_REPO/kubernetes-lb-controller:latest
